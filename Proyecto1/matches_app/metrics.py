from .validator import MatchRecord


class MatchMetrics:
    def summary_by_division(self, records: list[MatchRecord]) -> dict[str, dict[str, int]]:
        summary: dict[str, dict[str, int]] = {}

        for record in records:
            stats = summary.setdefault(
                record.division,
                {
                    "partidos": 0,
                    "victorias_local": 0,
                    "empates": 0,
                    "victorias_visitante": 0,
                    "goles_local": 0,
                    "goles_visitante": 0,
                },
            )
            stats["partidos"] += 1
            stats["goles_local"] += record.home_goals
            stats["goles_visitante"] += record.away_goals

            result_key = {
                "H": "victorias_local",
                "D": "empates",
                "A": "victorias_visitante",
            }[record.result]
            stats[result_key] += 1

        return dict(sorted(summary.items(), key=lambda item: item[1]["partidos"], reverse=True))
