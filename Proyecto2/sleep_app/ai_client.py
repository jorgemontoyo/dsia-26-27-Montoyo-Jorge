"""Cliente de resúmenes con modo local mock y proveedor Hugging Face."""

import os
from dataclasses import asdict, dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"


@dataclass(frozen=True)
class AIResponse:
    """Respuesta normalizada para que el pipeline no dependa del SDK."""

    provider: str
    task: str
    model: str | None
    text: str

    def to_dict(self) -> dict[str, str | None]:
        """Convierte la respuesta en un objeto listo para guardar como JSON."""
        return asdict(self)


class AIClientError(RuntimeError):
    """Error de configuración o de llamada al proveedor de IA."""


def _mock_summary(summary: dict) -> str:
    counts = summary["predictions_by_category"]
    most_common, count = max(counts.items(), key=lambda item: (item[1], item[0]))
    return (
        f"Resumen simulado de {summary['rows_predicted']} predicciones. "
        f"La categoría más frecuente es {most_common} ({count} casos). "
        "El modo mock no realiza una llamada a un modelo de IA."
    )


def summarize_predictions(
    summary: dict,
    provider: str = "mock",
    model: str | None = None,
) -> AIResponse:
    """Resume los recuentos de predicción sin enviar datos fila a fila."""
    provider = provider.strip().lower()
    if provider == "mock":
        return AIResponse(
            provider="mock",
            task="summary",
            model=None,
            text=_mock_summary(summary),
        )

    if provider != "hf":
        raise AIClientError(f"Proveedor no soportado: {provider}")

    token = os.getenv("HF_TOKEN")
    if not token:
        raise AIClientError("Falta HF_TOKEN; configúralo en .env para usar --provider hf")

    chosen_model = model or DEFAULT_HF_MODEL
    prompt = (
        "Resume en español la distribución de estas predicciones de categorías de sueño. "
        "Describe solo los recuentos, sin inferir causalidad ni hacer diagnósticos. "
        f"Número de registros: {summary['rows_predicted']}. "
        f"Recuentos por categoría: {summary['predictions_by_category']}"
    )
    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(api_key=token, provider="auto")
        result = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model=chosen_model,
            max_tokens=256,
        )
        text = result.choices[0].message.content or ""
    except Exception as exc:
        raise AIClientError(f"Falló la llamada a Hugging Face: {exc}") from exc

    if not text.strip():
        raise AIClientError("Hugging Face devolvió una respuesta vacía")
    return AIResponse(
        provider="huggingface",
        task="chat_completion",
        model=chosen_model,
        text=text.strip(),
    )
