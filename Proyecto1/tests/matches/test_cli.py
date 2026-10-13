"""Pruebas de la CLI de matches_app."""

from pathlib import Path

import pandas as pd
import pytest

from matches_app import cli
from matches_app.validator import REQUIRED_COLUMNS


@pytest.fixture
def csv_mini(tmp_path: Path) -> Path:
    path = tmp_path / "matches_mini.csv"
    path.write_text(
        "Division,MatchDate,HomeTeam,AwayTeam,FTHome,FTAway,FTResult\n"
        "F1,2026-01-01, A ,B,2,1,H\n"
        "F1,2026-01-02,C,D,0,0,D\n"
        "F1,2026-01-03,E,F,1,2,H\n",
        encoding="utf-8",
    )
    return path


def test_main_exporta_solo_los_partidos_validos(csv_mini: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "matches_limpios.csv"

    cli.main(["--input", str(csv_mini), "--output", str(output_path)])

    clean = pd.read_csv(output_path)
    assert len(clean) == 2
    assert list(clean.columns) == list(REQUIRED_COLUMNS)
    assert clean["HomeTeam"].tolist() == ["A", "C"]
    assert clean["FTResult"].tolist() == ["H", "D"]


def test_main_imprime_resumen(csv_mini: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    cli.main(["--input", str(csv_mini), "--output", str(tmp_path / "salida.csv")])

    stdout = capsys.readouterr().out
    assert "Partidos válidos: 2 | inválidos: 1" in stdout
    assert "F1: 2, 1, 1, 0, 2/1" in stdout


def test_main_sin_partidos_validos_conserva_cabecera(tmp_path: Path) -> None:
    input_path = tmp_path / "invalidos.csv"
    output_path = tmp_path / "salida.csv"
    input_path.write_text(
        "Division,MatchDate,HomeTeam,AwayTeam,FTHome,FTAway,FTResult\n"
        "F1,2026-01-01,A,B,2,1,D\n",
        encoding="utf-8",
    )

    cli.main(["--input", str(input_path), "--output", str(output_path)])

    clean = pd.read_csv(output_path)
    assert clean.empty
    assert list(clean.columns) == list(REQUIRED_COLUMNS)

