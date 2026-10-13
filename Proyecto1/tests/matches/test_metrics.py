"""Pruebas del resumen por división."""

from matches_app.metrics import MatchMetrics
from matches_app.validator import MatchRecord


def test_summary_by_division_cuenta_resultados_y_goles() -> None:
    records = [
        MatchRecord("F1", "2026-01-01", "A", "B", 2, 1, "H"),
        MatchRecord("F1", "2026-01-02", "C", "D", 0, 0, "D"),
        MatchRecord("F1", "2026-01-03", "E", "F", 1, 3, "A"),
        MatchRecord("E1", "2026-01-04", "G", "H", 4, 2, "H"),
    ]

    summary = MatchMetrics().summary_by_division(records)

    assert list(summary) == ["F1", "E1"]
    assert summary["F1"] == {
        "partidos": 3,
        "victorias_local": 1,
        "empates": 1,
        "victorias_visitante": 1,
        "goles_local": 3,
        "goles_visitante": 4,
    }
    assert summary["E1"] == {
        "partidos": 1,
        "victorias_local": 1,
        "empates": 0,
        "victorias_visitante": 0,
        "goles_local": 4,
        "goles_visitante": 2,
    }


def test_summary_by_division_sin_partidos() -> None:
    assert MatchMetrics().summary_by_division([]) == {}
