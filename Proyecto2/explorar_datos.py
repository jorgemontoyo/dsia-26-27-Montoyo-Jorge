"""Comprueba la estructura básica del CSV antes de entrenar un modelo."""

import csv
from collections import Counter
from pathlib import Path


DATA_PATH = Path(__file__).with_name("Datos.csv")
TARGET = "sleep_debt_category"


def main() -> None:
    with DATA_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        rows = list(reader)

    if not rows or TARGET not in columns or "user_id" not in columns:
        raise ValueError("El CSV está vacío o le faltan columnas esenciales")

    empty_cells = sum(
        value is None or not value.strip()
        for row in rows
        for value in row.values()
    )
    ids = [row["user_id"] for row in rows]
    classes = Counter(row[TARGET] for row in rows)

    print(f"Filas: {len(rows)}")
    print(f"Columnas: {len(columns)}")
    print(f"Celdas vacías: {empty_cells}")
    print(f"user_id duplicados: {len(ids) - len(set(ids))}")
    print("Distribución de sleep_debt_category:")
    for category, count in classes.most_common():
        percentage = 100 * count / len(rows)
        print(f"  {category}: {count} ({percentage:.1f} %)")


if __name__ == "__main__":
    main()
