"""Tests de SalesMetrics (Proyecto I - Parte A)."""

import pytest

from ventas_app.metrics import SalesMetrics
from ventas_app.validator import SalesRecord


@pytest.fixture
def records() -> list[SalesRecord]:
    return [
        SalesRecord(region="Norte", product="A", units=2, unit_price=10.0),  # 20.0
        SalesRecord(region="Sur", product="B", units=1, unit_price=5.0),  # 5.0
        SalesRecord(region="Norte", product="A", units=3, unit_price=10.0),  # 30.0
    ]


@pytest.fixture
def metrics() -> SalesMetrics:
    return SalesMetrics()


def test_total_by_region_agrupa_y_suma(metrics, records):
    totals = metrics.total_by_region(records)
    assert totals["Norte"] == 50.0
    assert totals["Sur"] == 5.0


def test_total_by_region_ordena_de_mayor_a_menor(metrics, records):
    totals = metrics.total_by_region(records)
    assert list(totals.keys())[0] == "Norte"  # 50.0 > 5.0


def test_total_by_region_incluye_todas_las_regiones(metrics, records):
    totals = metrics.total_by_region(records)
    assert totals == {"Norte": 50.0, "Sur": 5.0}


def test_total_by_region_con_lista_vacia_no_falla(metrics):
    assert metrics.total_by_region([]) == {}
