"""Pruebas de contrato y reglas de entrada del modelo."""

import pytest

from sleep_app.validator import InputValidationError, validate_input


def test_acepta_variables_sin_necesitar_la_etiqueta(valid_features):
    result = validate_input(valid_features)
    assert len(result) == 2
    assert "sleep_debt_category" not in result.columns


def test_rechaza_columna_del_modelo_ausente(valid_features):
    with pytest.raises(InputValidationError, match="age"):
        validate_input(valid_features.drop(columns="age"))


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("age", -1),
        ("screen_brightness_pct", 101),
        ("blue_light_filter_active", 2),
        ("bedtime_phone_minutes", None),
        ("gender", "  "),
    ],
)
def test_rechaza_valores_invalidos(valid_features, column, value):
    invalid = valid_features.copy()
    invalid.loc[0, column] = value
    with pytest.raises(InputValidationError):
        validate_input(invalid)


def test_convierte_columnas_numericas_textuales(valid_features):
    data = valid_features.copy()
    data["age"] = data["age"].astype(str)
    assert validate_input(data)["age"].tolist() == [24, 38]
