# Diseño de `matches_app`

La aplicación sigue la estructura de `ventas_app`:

- `loader.py` lee el CSV mediante el contrato `MatchRepository`.
- `validator.py` separa partidos válidos e inválidos. Exige división, fecha,
  equipos distintos, goles enteros no negativos y un resultado (`H`, `D`, `A`)
  coherente con el marcador.
- `metrics.py` calcula partidos, resultados y goles por división.
- `cli.py` guarda un CSV limpio con los siete campos esenciales y muestra
  el resumen. Las otras columnas de `Matches.csv` son opcionales y no se
  incluyen en el CSV limpio.

Desde `Proyecto1`:

```powershell
python -m matches_app.cli --input Datos/Matches.csv --output Datos/matches_limpios.csv
```
