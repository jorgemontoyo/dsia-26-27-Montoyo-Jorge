"""Pruebas de las reglas de negocio de los partidos."""

from pathlib import Path

import pandas as pd
import pytest

from matches_app.loader import CsvMatchRepository
from matches_app.validator import MatchRecord, MatchValidator, ValidationError


def partido_valido() -> dict[str, object]:
    return {
        "Division": "F1",
        "MatchDate": "2026-01-01",
        "HomeTeam": "Equipo A",
        "AwayTeam": "Equipo B",
        "FTHome": 2,
        "FTAway": 1,
        "FTResult": "H",
    }


def test_split_acepta_resultados_h_d_a_y_normaliza_texto() -> None:
    local = partido_valido()
    local["HomeTeam"] = " Equipo A "
    empate = {**partido_valido(), "HomeTeam": "C", "AwayTeam": "D", "FTHome": 0, "FTAway": 0, "FTResult": "D"}
    visitante = {**partido_valido(), "HomeTeam": "E", "AwayTeam": "F", "FTHome": 1, "FTAway": 3, "FTResult": "A"}

    records, invalid = MatchValidator().split(pd.DataFrame([local, empate, visitante]))

    assert len(invalid) == 0
    assert [record.result for record in records] == ["H", "D", "A"]
    assert records[0] == MatchRecord("F1", "2026-01-01", "Equipo A", "Equipo B", 2, 1, "H")


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("Division", " "),
        ("MatchDate", "fecha inválida"),
        ("HomeTeam", None),
        ("AwayTeam", "Equipo A"),
        ("FTHome", -1),
        ("FTHome", 1.5),
        ("FTAway", None),
        ("FTResult", "X"),
        ("FTResult", "A"),
    ],
)
def test_split_rechaza_datos_invalidos(column: str, value: object) -> None:
    row = partido_valido()
    row[column] = value

    records, invalid = MatchValidator().split(pd.DataFrame([row]))

    assert records == []
    assert len(invalid) == 1


def test_split_no_muta_el_dataframe_original() -> None:
    frame = pd.DataFrame([{**partido_valido(), "HomeTeam": " Equipo A "}])
    original = frame.copy(deep=True)

    MatchValidator().split(frame)

    pd.testing.assert_frame_equal(frame, original)


def test_split_falla_si_falta_una_columna_obligatoria() -> None:
    frame = pd.DataFrame([partido_valido()]).drop(columns="FTResult")

    with pytest.raises(ValidationError, match="FTResult"):
        MatchValidator().split(frame)


def test_match_record_es_inmutable() -> None:
    record = MatchRecord("F1", "2026-01-01", "A", "B", 2, 1, "H")

    with pytest.raises(AttributeError):
        record.home_goals = 99


def test_split_con_csv_real_del_proyecto() -> None:
    path = Path(__file__).resolve().parents[2] / "Datos" / "Matches.csv"
    frame = CsvMatchRepository(path).load()

    records, invalid = MatchValidator().split(frame)

    assert len(frame) == 238858
    assert len(records) == 238854
    assert len(invalid) == 4
