"""Fixtures comunes para las pruebas del Proyecto II."""

import pandas as pd
import pytest


@pytest.fixture
def valid_features() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "gender": ["Female", "Male"],
            "occupation_type": ["Student", "Remote Tech"],
            "chronotype": ["Night Owl", "Intermediate"],
            "primary_bedtime_app": ["YouTube", "Instagram / Reddit"],
            "age": [24, 38],
            "bedtime_phone_minutes": [45, 90],
            "screen_brightness_pct": [40, 80],
            "blue_light_filter_active": [1, 0],
            "caffeine_post_5pm_mg": [0, 50],
            "physical_activity_min": [30, 60],
        }
    )
