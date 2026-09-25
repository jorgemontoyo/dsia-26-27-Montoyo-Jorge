import argparse
from pathlib import Path

import pandas as pd

from .loader import CsvSalesRepository
from .metrics import SalesMetrics
from .validator import SalesValidator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Procesamiento de ventas"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="CSV de entrada",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="CSV limpio de salida",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    repository = CsvSalesRepository(input_path)
    validator = SalesValidator()
    metrics = SalesMetrics()

    frame = repository.load()

    valid_records, invalid_rows = validator.split(frame)

    totals = metrics.total_by_region(valid_records)

    clean_frame = pd.DataFrame(
        [
            {
                "region": record.region,
                "producto": record.product,
                "unidades": record.units,
                "precio_unitario": record.unit_price,
            }
            for record in valid_records
        ]
    )

    clean_frame.to_csv(output_path, index=False)

    print(
        f"Registros válidos: {len(valid_records)} | "
        f"inválidos: {len(invalid_rows)}"
    )

    print("Importe por región:")

    for region, total in totals.items():
        print(f"  {region}: {total:.2f}")


if __name__ == "__main__":
    main()