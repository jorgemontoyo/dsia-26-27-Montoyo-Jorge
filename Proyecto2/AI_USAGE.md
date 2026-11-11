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
