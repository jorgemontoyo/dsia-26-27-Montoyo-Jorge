from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = (
    "Division", "MatchDate", "HomeTeam", "AwayTeam",
    "FTHome", "FTAway", "FTResult",
)


class ValidationError(Exception):
    """El CSV no tiene la estructura necesaria para procesar partidos."""


@dataclass(frozen=True)
class MatchRecord:
    division: str
    match_date: str
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    result: str


class MatchValidator:
    def split(self, frame: pd.DataFrame) -> tuple[list[MatchRecord], pd.DataFrame]:
        missing = set(REQUIRED_COLUMNS) - set(frame.columns)
        if missing:
            raise ValidationError(f"Faltan columnas obligatorias: {', '.join(sorted(missing))}")

        work = frame.loc[:, REQUIRED_COLUMNS].copy()
        for column in ("Division", "HomeTeam", "AwayTeam", "FTResult"):
            work[column] = work[column].astype("string").str.strip()

        dates = pd.to_datetime(work["MatchDate"], format="%Y-%m-%d", errors="coerce")
        home_goals = pd.to_numeric(work["FTHome"], errors="coerce")
        away_goals = pd.to_numeric(work["FTAway"], errors="coerce")

        expected_result = pd.Series("D", index=work.index)
        expected_result.loc[home_goals > away_goals] = "H"
        expected_result.loc[home_goals < away_goals] = "A"

        valid_mask = (
            dates.notna()
            & work["Division"].notna() & work["Division"].ne("")
            & work["HomeTeam"].notna() & work["HomeTeam"].ne("")
            & work["AwayTeam"].notna() & work["AwayTeam"].ne("")
            & work["HomeTeam"].ne(work["AwayTeam"])
            & home_goals.notna() & away_goals.notna()
            & home_goals.ge(0) & away_goals.ge(0)
            & home_goals.mod(1).eq(0) & away_goals.mod(1).eq(0)
            & work["FTResult"].isin(("H", "D", "A"))
            & work["FTResult"].eq(expected_result)
        ).fillna(False)

        records = [
            MatchRecord(
                division=str(work.at[index, "Division"]),
                match_date=dates.at[index].date().isoformat(),
                home_team=str(work.at[index, "HomeTeam"]),
                away_team=str(work.at[index, "AwayTeam"]),
                home_goals=int(home_goals.at[index]),
                away_goals=int(away_goals.at[index]),
                result=str(work.at[index, "FTResult"]),
            )
            for index in work.index[valid_mask]
        ]
        return records, frame.loc[~valid_mask].copy()
