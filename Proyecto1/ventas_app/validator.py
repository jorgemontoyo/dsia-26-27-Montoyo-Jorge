from dataclasses import dataclass

import pandas as pd


MIN_UNITS = 0
MIN_UNIT_PRICE = 0


class ValidationError(Exception):
    """Datos que no cumplen las reglas de negocio."""


@dataclass(frozen=True)
class SalesRecord:
    region: str
    product: str
    units: float
    unit_price: float

    @property
    def amount(self) -> float:
        return self.units * self.unit_price


class SalesValidator:
    def split(
        self,
        frame: pd.DataFrame,
    ) -> tuple[list[SalesRecord], pd.DataFrame]:

        work = frame.copy()

        work["unidades"] = pd.to_numeric(
            work["unidades"],
            errors="coerce",
        )

        work["precio_unitario"] = pd.to_numeric(
            work["precio_unitario"],
            errors="coerce",
        )

        valid_mask = (
            work["unidades"].notna()
            & (work["unidades"] > MIN_UNITS)
            & (work["precio_unitario"] > MIN_UNIT_PRICE)
        )

        valid_records = [
            SalesRecord(
                region=str(row.region),
                product=str(row.producto),
                units=float(row.unidades),
                unit_price=float(row.precio_unitario),
            )
            for row in work.loc[valid_mask].itertuples(index=False)
        ]

        invalid_rows = work.loc[~valid_mask]

        return valid_records, invalid_rows