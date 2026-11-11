"""Entrena y evalúa un clasificador inicial de deuda de sueño."""

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


PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "Datos.csv"
ARTIFACTS_DIR = PROJECT_DIR / "artifacts"
TARGET = "sleep_debt_category"

CATEGORICAL_FEATURES = [
    "gender",
    "occupation_type",
    "chronotype",
    "primary_bedtime_app",
]
NUMERIC_FEATURES = [
    "age",
    "bedtime_phone_minutes",
    "screen_brightness_pct",
    "blue_light_filter_active",
    "caffeine_post_5pm_mg",
    "physical_activity_min",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def build_model() -> Pipeline:
    """Guarda el preprocesado y el clasificador en un único objeto."""
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


def main() -> None:
    data = pd.read_csv(DATA_PATH)
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

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, ARTIFACTS_DIR / "modelo.joblib", compress=3)
    (ARTIFACTS_DIR / "metricas.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Entrenamiento: {len(x_train)} filas; prueba: {len(x_test)} filas")
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
