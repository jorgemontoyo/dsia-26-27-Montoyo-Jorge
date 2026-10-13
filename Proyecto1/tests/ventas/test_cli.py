"""Pruebas de la CLI real de ventas_app."""

from pathlib import Path

import pandas as pd
import pytest

from ventas_app import cli


@pytest.fixture
def csv_mini(tmp_path: Path) -> Path:
    path = tmp_path / "ventas_mini.csv"
    path.write_text(
        "region,producto,unidades,precio_unitario\n"
        "Norte,A,2,10\n"
        "Sur,B,1,5\n"
        "Norte,A,0,10\n",  # fila inválida: 0 unidades
        encoding="utf-8",
    )
    return path


def ejecutar_cli(monkeypatch: pytest.MonkeyPatch, entrada: Path, salida: Path) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", "--input", str(entrada), "--output", str(salida)],
    )
    cli.main()


def test_main_exporta_solo_los_registros_validos(
    csv_mini: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_path = tmp_path / "salida.csv"

    ejecutar_cli(monkeypatch, csv_mini, output_path)

    exportado = pd.read_csv(output_path)
    assert len(exportado) == 2
    assert list(exportado.columns) == ["region", "producto", "unidades", "precio_unitario"]
    assert exportado["unidades"].tolist() == [2.0, 1.0]


def test_main_imprime_el_resumen_por_consola(
    csv_mini: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    ejecutar_cli(monkeypatch, csv_mini, tmp_path / "salida.csv")

    salida = capsys.readouterr().out
    assert "Registros válidos: 2 | inválidos: 1" in salida
    assert "Importe por región:" in salida
    assert "Norte: 20.00" in salida
    assert "Sur: 5.00" in salida


def test_main_con_csv_real_del_proyecto(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = Path(__file__).resolve().parents[2] / "Datos" / "ventas.csv"
    output_path = tmp_path / "ventas_validas.csv"

    ejecutar_cli(monkeypatch, input_path, output_path)

    exportado = pd.read_csv(output_path)
    assert len(exportado) == 8


def test_main_con_todas_las_filas_invalidas_conserva_la_cabecera(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "ventas_invalidas.csv"
    output_path = tmp_path / "salida.csv"
    input_path.write_text(
        "region,producto,unidades,precio_unitario\nNorte,A,0,10\n",
        encoding="utf-8",
    )

    ejecutar_cli(monkeypatch, input_path, output_path)

    exportado = pd.read_csv(output_path)
    assert exportado.empty
    assert list(exportado.columns) == ["region", "producto", "unidades", "precio_unitario"]
