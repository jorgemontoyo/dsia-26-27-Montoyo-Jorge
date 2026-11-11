"""Lectura de datos y carga del modelo serializado."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline


class DataLoadError(Exception):
    """No se pudieron leer los datos de entrada."""


class ModelLoadError(Exception):
    """No se pudo cargar el modelo entrenado."""


def load_data(path: Path) -> pd.DataFrame:
    """Lee un CSV y normaliza errores de lectura a DataLoadError."""
    if not path.is_file():
        raise DataLoadError(f"No existe el CSV de entrada: {path}")
    try:
        return pd.read_csv(path)
    except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise DataLoadError(f"No se pudo leer el CSV {path}: {exc}") from exc


def load_model(path: Path) -> Pipeline:
    """Carga el pipeline de scikit-learn generado por entrenar_modelo.py."""
    if not path.is_file():
        raise ModelLoadError(f"No existe el modelo entrenado: {path}")
    try:
        model = joblib.load(path)
    except (OSError, ValueError, EOFError, ImportError) as exc:
        raise ModelLoadError(f"No se pudo cargar el modelo {path}: {exc}") from exc
    if not hasattr(model, "predict"):
        raise ModelLoadError(f"El artefacto no ofrece el método predict(): {path}")
    return model
