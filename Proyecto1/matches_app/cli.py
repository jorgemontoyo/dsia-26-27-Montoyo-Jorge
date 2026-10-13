import argparse
from pathlib import Path

import pandas as pd

from .loader import CsvMatchRepository
from .metrics import MatchMetrics
from .validator import MatchValidator, REQUIRED_COLUMNS


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Procesamiento de partidos")
    parser.add_argument("--input", required=True, help="CSV de entrada")
    parser.add_argument("--output", required=True, help="CSV limpio de salida")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    frame = CsvMatchRepository(Path(args.input)).load()
    records, invalid_rows = MatchValidator().split(frame)
    summary = MatchMetrics().summary_by_division(records)

    clean_frame = pd.DataFrame(
        [
            {
                "Division": record.division,
                "MatchDate": record.match_date,
                "HomeTeam": record.home_team,
                "AwayTeam": record.away_team,
                "FTHome": record.home_goals,
                "FTAway": record.away_goals,
                "FTResult": record.result,
            }
            for record in records
        ],
        columns=REQUIRED_COLUMNS,
    )
    clean_frame.to_csv(Path(args.output), index=False)

    print(f"Partidos válidos: {len(records)} | inválidos: {len(invalid_rows)}")
    print("Resumen por división (partidos, local, empates, visitante, goles local/visitante):")
    for division, stats in summary.items():
        print(
            f"  {division}: {stats['partidos']}, {stats['victorias_local']}, "
            f"{stats['empates']}, {stats['victorias_visitante']}, "
            f"{stats['goles_local']}/{stats['goles_visitante']}"
        )


if __name__ == "__main__":
    main()
