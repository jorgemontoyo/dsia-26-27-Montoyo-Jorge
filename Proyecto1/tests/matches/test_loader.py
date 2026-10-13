"""Pruebas de CsvMatchRepository."""

from pathlib import Path

import pytest

from matches_app.loader import CsvMatchRepository, DataLoadError


def test_load_path_inexistente_lanza_error(tmp_path: Path) -> None:
    with pytest.raises(DataLoadError, match="No existe el fichero"):
        CsvMatchRepository(tmp_path / "no_existe.csv").load()


def test_load_csv_devuelve_las_columnas_y_filas(tmp_path: Path) -> None:
    csv_path = tmp_path / "mini.csv"
    csv_path.write_text(
        "Division,MatchDate,HomeTeam,AwayTeam,FTHome,FTAway,FTResult\n"
        "F1,2026-01-01,Equipo A,Equipo B,2,1,H\n",
        encoding="utf-8",
    )

    frame = CsvMatchRepository(csv_path).load()

    assert len(frame) == 1
    assert frame.loc[0, "Division"] == "F1"
    assert frame.loc[0, "HomeTeam"] == "Equipo A"
