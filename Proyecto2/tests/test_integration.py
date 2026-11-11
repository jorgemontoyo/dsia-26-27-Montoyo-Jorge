"""Prueba marcada de la inferencia con el artefacto entrenado del proyecto."""

from pathlib import Path

import pandas as pd
import pytest

from sleep_app.ai_client import summarize_predictions
from sleep_app.loader import load_data, load_model
from sleep_app.pipeline import run_pipeline


PROJECT_DIR = Path(__file__).resolve().parents[1]


@pytest.mark.integration
def test_carga_modelo_real_predice_csv_y_resume_en_mock():
    data = load_data(PROJECT_DIR / "Datos.csv").head(12)
    model = load_model(PROJECT_DIR / "artifacts" / "modelo.joblib")

    predictions, summary = run_pipeline(data, model)
    response = summarize_predictions(summary, provider="mock")

    assert len(predictions) == 12
    assert predictions["predicted_sleep_debt_category"].notna().all()
    assert summary["rows_predicted"] == 12
    assert response.provider == "mock"


def test_modelo_y_datos_existen_en_el_repo():
    assert (PROJECT_DIR / "Datos.csv").is_file()
    assert (PROJECT_DIR / "artifacts" / "modelo.joblib").is_file()
