"""Configuración compartida por entrenamiento, validación e inferencia."""

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
