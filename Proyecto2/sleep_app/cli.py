"""Interfaz de línea de comandos del pipeline de predicción."""

import argparse
import logging
from pathlib import Path

from .ai_client import AIClientError, summarize_predictions
from .loader import DataLoadError, ModelLoadError, load_data, load_model
from .pipeline import run_pipeline, save_results
from .validator import InputValidationError


def configure_logging(log_path: Path) -> None:
    """Configura mensajes simultáneos en consola y en run.log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
        force=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera predicciones de deuda de sueño desde un CSV."
    )
    parser.add_argument("--input", type=Path, required=True, help="CSV con las variables previas al sueño")
    parser.add_argument("--model", type=Path, default=Path("artifacts/modelo.joblib"), help="Modelo joblib entrenado")
    parser.add_argument("--output-dir", type=Path, default=Path("salida"), help="Carpeta para predicciones, métricas y log")
    parser.add_argument("--provider", choices=("mock", "hf"), default="mock", help="Proveedor para resumir las predicciones")
    parser.add_argument("--ai-model", default=None, help="Id de un modelo chat del Hub de Hugging Face")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.output_dir / "run.log")
    logger = logging.getLogger("sleep_app")
    logger.info("Inicio del pipeline: input=%s model=%s", args.input, args.model)

    try:
        frame = load_data(args.input)
        model = load_model(args.model)
        results, summary = run_pipeline(frame, model)
        ai_response = summarize_predictions(summary, args.provider, args.ai_model)
        predictions_path, summary_path = save_results(
            results, summary, args.output_dir, ai_response.to_dict()
        )
    except (DataLoadError, ModelLoadError, InputValidationError, AIClientError, ValueError) as exc:
        logger.error("Pipeline interrumpido: %s", exc)
        return 1
    except OSError as exc:
        logger.error("No se pudieron escribir los resultados: %s", exc)
        return 1

    logger.info(
        "Pipeline completado: filas=%d categorías=%s provider=%s csv=%s metrics=%s ai_summary=%s",
        summary["rows_predicted"],
        summary["predictions_by_category"],
        ai_response.provider,
        predictions_path,
        summary_path,
        args.output_dir / "ai_summary.json",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
