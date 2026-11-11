"""Pruebas del cliente IA sin realizar llamadas de red."""

import pytest

from sleep_app.ai_client import AIClientError, summarize_predictions


def test_mock_resume_recuentos_sin_modelo_ni_red():
    response = summarize_predictions(
        {
            "rows_predicted": 8,
            "predictions_by_category": {"Mild Deficit": 3, "Moderate Debt": 5},
        }
    )

    assert response.provider == "mock"
    assert response.task == "summary"
    assert response.model is None
    assert "Moderate Debt (5 casos)" in response.text


def test_proveedor_desconocido_falla_con_error_del_cliente():
    with pytest.raises(AIClientError, match="Proveedor no soportado"):
        summarize_predictions({"rows_predicted": 1, "predictions_by_category": {}}, "otro")


def test_hugging_face_sin_token_falla_sin_intentar_red(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    with pytest.raises(AIClientError, match="Falta HF_TOKEN"):
        summarize_predictions(
            {"rows_predicted": 1, "predictions_by_category": {"Mild Deficit": 1}},
            "hf",
        )
