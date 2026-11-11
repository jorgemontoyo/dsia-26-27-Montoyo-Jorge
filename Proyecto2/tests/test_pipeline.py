"""Pruebas de predicción y escritura de artefactos."""

import json

from sleep_app.pipeline import run_pipeline, save_results


class FixedModel:
    def predict(self, features):
        return ["Mild Deficit", "Moderate Debt"][: len(features)]


def test_pipeline_anade_predicciones_y_resumen(valid_features):
    results, summary = run_pipeline(valid_features, FixedModel())
    assert results["predicted_sleep_debt_category"].tolist() == [
        "Mild Deficit",
        "Moderate Debt",
    ]
    assert summary["rows_predicted"] == 2
    assert summary["predictions_by_category"] == {
        "Mild Deficit": 1,
        "Moderate Debt": 1,
    }


def test_save_results_escribe_predicciones_metricas_y_resumen_ia(tmp_path, valid_features):
    results, metrics = run_pipeline(valid_features, FixedModel())
    ai_summary = {"provider": "mock", "task": "summary", "model": None, "text": "resumen"}

    csv_path, metrics_path = save_results(results, metrics, tmp_path, ai_summary)

    assert csv_path.is_file()
    assert json.loads(metrics_path.read_text(encoding="utf-8")) == metrics
    assert json.loads((tmp_path / "ai_summary.json").read_text(encoding="utf-8")) == ai_summary
