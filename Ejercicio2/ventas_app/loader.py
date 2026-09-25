from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoadError(Exception):
    """Error al cargar datos de origen."""


class SalesRepository(Protocol):
    def load(self) -> pd.DataFrame:
        ...


class CsvSalesRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> pd.DataFrame:
        if not self._path.exists():
            raise DataLoadError(f"No existe el fichero: {self._path}")

        return pd.read_csv(self._path)