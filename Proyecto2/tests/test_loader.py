"""Pruebas de lectura CSV y carga de artefactos."""

import pytest

from sleep_app.loader import DataLoadError, ModelLoadError, load_data, load_model


def test_load_data_lee_csv_temporal(tmp_path):
    path = tmp_path / "entrada.csv"
    path.write_text("age,gender\n24,Female\n", encoding="utf-8")
    frame = load_data(path)
    assert frame.to_dict(orient="records") == [{"age": 24, "gender": "Female"}]


def test_load_data_path_ausente_da_error_de_dominio(tmp_path):
    with pytest.raises(DataLoadError, match="No existe"):
        load_data(tmp_path / "ausente.csv")


def test_load_model_path_ausente_da_error_de_dominio(tmp_path):
    with pytest.raises(ModelLoadError, match="No existe"):
        load_model(tmp_path / "ausente.joblib")
