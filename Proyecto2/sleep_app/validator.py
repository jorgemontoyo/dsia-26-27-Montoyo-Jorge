"""Validación del contrato de entrada del modelo de sueño."""

import pandas as pd

from .config import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES


class InputValidationError(Exception):
    """Los datos no cumplen el contrato necesario para predecir."""


def validate_input(frame: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia con las columnas del modelo o explica el problema."""
    if frame.empty:
        raise InputValidationError("El CSV no contiene filas para predecir")

    missing = sorted(set(FEATURES) - set(frame.columns))
    if missing:
        raise InputValidationError(f"Faltan columnas del modelo: {missing}")

    features = frame.loc[:, FEATURES].copy()
    empty = features.columns[features.isna().any()].tolist()
    if empty:
        raise InputValidationError(f"Hay valores vacíos en las columnas: {empty}")

    for column in NUMERIC_FEATURES:
        values = pd.to_numeric(features[column], errors="coerce")
        if values.isna().any():
            raise InputValidationError(f"La columna {column} debe contener números")
        features[column] = values

    for column in CATEGORICAL_FEATURES:
        if features[column].astype("string").str.strip().eq("").any():
            raise InputValidationError(f"La columna {column} contiene texto vacío")

    non_negative = ["age", "bedtime_phone_minutes", "caffeine_post_5pm_mg", "physical_activity_min"]
    for column in non_negative:
        if (features[column] < 0).any():
            raise InputValidationError(f"La columna {column} no admite valores negativos")
    if (~features["screen_brightness_pct"].between(0, 100)).any():
        raise InputValidationError("screen_brightness_pct debe estar entre 0 y 100")
    if not features["blue_light_filter_active"].isin([0, 1, False, True]).all():
        raise InputValidationError("blue_light_filter_active debe ser 0/1 o False/True")

    return features
