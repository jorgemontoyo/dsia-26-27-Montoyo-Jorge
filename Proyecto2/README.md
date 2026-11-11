# Proyecto II: hábitos nocturnos y categoría de deuda de sueño

## Problema

Predecir `sleep_debt_category` a partir de datos conocidos antes de dormir. Es un problema de **clasificación multiclase**: el modelo elegirá una de las cuatro categorías presentes en `Datos.csv`.

Este proyecto es un ejercicio educativo. La etiqueta del dataset no equivale a un diagnóstico médico y una predicción no demuestra que un hábito cause un resultado de sueño.

## Datos

- Archivo local: `Datos.csv`.
- Tamaño: 8.500 filas y 18 columnas.
- Calidad observada: sin celdas vacías y sin `user_id` duplicados.
- Fuente confirmada por el autor del proyecto: [Sleep Debt & Screen Time: Late Night Phone Habits, de Samar Talwar, en Kaggle](https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits).
- Licencia del **dataset**: pendiente de verificar en la ficha original. La licencia de un notebook que use estos datos no determina la licencia del CSV.

La variable objetivo está distribuida así:

| Categoría | Filas | Porcentaje |
| --- | ---: | ---: |
| Moderate Debt | 4.462 | 52,5 % |
| Mild Deficit | 2.004 | 23,6 % |
| Optimal Recovery | 1.387 | 16,3 % |
| Severe Sleep Debt | 647 | 7,6 % |

## Variables para la primera versión del modelo

Usaremos `age`, `gender`, `occupation_type`, `chronotype`, `bedtime_phone_minutes`, `primary_bedtime_app`, `screen_brightness_pct`, `blue_light_filter_active`, `caffeine_post_5pm_mg` y `physical_activity_min`.

`user_id` identifica registros y no es una característica predictiva. Excluiremos `sleep_latency_min`, `total_sleep_hours`, `deep_sleep_pct`, `rem_sleep_pct`, `morning_alarm_snoozes` y `next_day_fatigue_score`, porque se conocen durante o después de la noche. Usarlas en una predicción previa al sueño produciría fuga de información.

## Repetir la exploración inicial

Desde esta carpeta:

```powershell
python explorar_datos.py
```

El script imprime dimensiones, celdas vacías, identificadores duplicados y distribución de la variable objetivo. Solo usa la biblioteca estándar de Python.

## Preparar el entorno y entrenar el modelo base

Se usó Python 3.14.7. Desde esta carpeta, en PowerShell:

```powershell
python -m venv --without-pip .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe entrenar_modelo.py
```

El Python 3.14 instalado en este equipo no completó la instalación de `pip` dentro del entorno; por eso usamos `--without-pip` y el instalador `uv`, que ya está disponible. El entorno `.venv` contiene las dependencias y está excluido de Git. `requirements.txt` fija las versiones usadas en esta primera ejecución. En otro equipo donde `pip` funcione normalmente, también puedes usar `python -m venv .venv` y `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.

`entrenar_modelo.py` separa el 80 % de los registros para entrenar y el 20 % para probar, conservando la proporción de las cuatro clases (`stratify`). Primero calcula una referencia que siempre predice la clase mayoritaria. Luego entrena un `RandomForestClassifier`. Las categorías se codifican con `OneHotEncoder` dentro de un `Pipeline`; así, el preprocesado se aprende únicamente con el conjunto de entrenamiento y queda guardado junto al modelo.

Los resultados se escriben en `artifacts/metricas.json` y el modelo completo en `artifacts/modelo.joblib`. Ambos se pueden regenerar con el comando anterior. La métrica F1 macro da el mismo peso a cada clase, incluidas las minoritarias.

### Primera evaluación

| Método | Accuracy | F1 macro |
| --- | ---: | ---: |
| Predecir siempre la clase mayoritaria | 0,525 | 0,172 |
| Random Forest | 0,719 | 0,653 |

La clase `Severe Sleep Debt` obtuvo **recall 0,45**: el modelo detectó menos de la mitad de sus casos en el conjunto de prueba. Por eso no basta con mirar solo el accuracy. El detalle de las cuatro clases está en `artifacts/metricas.json`.

## Próximas etapas

1. Analizar las métricas por categoría y comprobar errores frecuentes.
2. Integrar la carga e inferencia del modelo en un pipeline con CLI y logs.
3. Añadir un cliente de IA por API con modo `mock`, pruebas, configuración y documentación de uso de IA.

La estructura se ampliará en el Proyecto III con una API o aplicación y despliegue.
