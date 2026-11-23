# Uso de IA

- Cliente del proyecto: Hugging Face Inference Providers.
- Tarea: `chat_completion`, para resumir los recuentos agregados de predicciones.
- Modelo configurado por defecto: `mistralai/Mistral-7B-Instruct-v0.3`.
- Modo para desarrollo y pruebas: `mock`; no usa red ni token.
- Asistente de desarrollo: OpenAI Codex.
- Aportación: estructura inicial del cliente mock/Hugging Face, argumentos CLI e integración del resumen en los artefactos del pipeline.
- Revisión pendiente del estudiante: revisar el código, ejecutar el pipeline en modo mock y comprobar que puede explicar los cambios antes de entregar.
- Comando local de evidencia: `python -m sleep_app.cli --input Datos.csv --model artifacts/modelo.joblib --output-dir salida --provider mock`.
- Llamada real: `python -m sleep_app.cli --input Datos.csv --model artifacts/modelo.joblib --output-dir salida-hf --provider hf` (requiere `HF_TOKEN` y puede consumir cuota del proveedor).

## Ayuda durante el desarrollo

Utilicé OpenAI Codex para ayudarme con el cliente de IA
mock/Hugging Face, los argumentos de la CLI y la integración
del resumen en las salidas del pipeline.

Incorporé las propuestas relativas a esas partes.
[Completar con las modificaciones o propuestas rechazadas,
si las hubo.]

## Verificación

Codex ejecutó los 18 tests, que pasaron, y comprobó el
pipeline en modo mock con las 8.500 filas del dataset.

Mi revisión personal del código: He evaluado mi modelo utilizando classification_report de sklearn.metrics (scikit-learn) para analizar la precisión, el recall y la puntuación F1 de cada categoría y valorar la calidad de sus predicciones.