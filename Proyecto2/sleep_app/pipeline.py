"""Inferencia por lotes y escritura de resultados."""

import json
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline

from .validator import validate_input


def run_pipeline(frame: pd.DataFrame, model: Pipeline) -> tuple[pd.DataFrame, dict]:
    """Predice una categoría por fila y devuelve resultados y resumen."""
    features = validate_input(frame)
    try:
        predictions = model.predict(features)
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError(f"El modelo no pudo generar predicciones: {exc}") from exc

    results = frame.copy()
    results["predicted_sleep_debt_category"] = predictions
    summary = {
        "rows_in": int(len(frame)),
        "rows_predicted": int(len(predictions)),
        "predictions_by_category": {
            str(category): int(count)
            for category, count in sorted(Counter(predictions).items())
        },
    }
    return results, summary


def save_results(
    results: pd.DataFrame,
    summary: dict,
    output_dir: Path,
    ai_summary: dict | None = None,
) -> tuple[Path, Path]:
    """Escribe las predicciones, métricas y, si se da, el resumen de IA."""
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = output_dir / "predicciones.csv"
    summary_path = output_dir / "metrics.json"
    results.to_csv(predictions_path, index=False)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if ai_summary is not None:
        (output_dir / "ai_summary.json").write_text(
            json.dumps(ai_summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return predictions_path, summary_path
