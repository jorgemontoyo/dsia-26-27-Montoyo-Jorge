"""Entrenamiento reproducible del clasificador de deuda de sueño."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES, TARGET


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "Datos.csv"
ARTIFACTS_DIR = PROJECT_DIR / "artifacts"


def build_model() -> Pipeline:
    """Crea el preprocesado y clasificador como un pipeline único."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numericas", "passthrough", NUMERIC_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocesado", preprocessor),
            (
                "clasificador",
                RandomForestClassifier(
                    n_estimators=200,
                    min_samples_leaf=3,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def train_model(
    data_path: Path = DATA_PATH,
    artifacts_dir: Path = ARTIFACTS_DIR,
) -> dict:
    """Entrena, evalúa y guarda el modelo y sus métricas; devuelve el informe."""
    if not data_path.is_file():
        raise FileNotFoundError(f"No existe el CSV de entrenamiento: {data_path}")

    data = pd.read_csv(data_path)
    required = set(FEATURES + [TARGET])
    missing_columns = required - set(data.columns)
    if missing_columns:
        raise ValueError(f"Faltan columnas: {sorted(missing_columns)}")
    if data[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Hay valores vacíos en las variables del modelo")

    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES],
        data[TARGET],
        test_size=0.20,
        stratify=data[TARGET],
        random_state=42,
    )

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(x_train, y_train)
    baseline_predictions = baseline.predict(x_test)

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "random_state": 42,
        "baseline_majority": {
            "accuracy": accuracy_score(y_test, baseline_predictions),
            "f1_macro": f1_score(y_test, baseline_predictions, average="macro"),
        },
        "random_forest": {
            "accuracy": accuracy_score(y_test, predictions),
            "f1_macro": f1_score(y_test, predictions, average="macro"),
            "report_by_class": classification_report(
                y_test, predictions, output_dict=True, zero_division=0
            ),
        },
    }

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifacts_dir / "modelo.joblib", compress=3)
    (artifacts_dir / "metricas.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return metrics


def main() -> None:
    """Punto de entrada para `python -m sleep_app.train`."""
    metrics = train_model()
    print(f"Entrenamiento: {metrics['train_rows']} filas; prueba: {metrics['test_rows']} filas")
    print(
        "Referencia (clase mayoritaria): "
        f"accuracy={metrics['baseline_majority']['accuracy']:.3f}, "
        f"F1 macro={metrics['baseline_majority']['f1_macro']:.3f}"
    )
    print(
        "Random Forest: "
        f"accuracy={metrics['random_forest']['accuracy']:.3f}, "
        f"F1 macro={metrics['random_forest']['f1_macro']:.3f}"
    )
    print(f"Modelo y métricas guardados en {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
