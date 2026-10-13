# E1 — Procesamiento de datos con pandas (30 min)

**Sesión:** 14 sep 2026  
**Dataset:** `../Datos/ventas.csv`

## Preparación (antes de arrancar)

```bash
cd 1_programacion_avanzada_python
# opcional: trabaja en el notebook 02_pandas_datos.ipynb
# o en un script propio ejercicios/solucion_e1.py
```

## Parte 1 — Diagnóstico (8 min)

1. Carga el CSV con `pathlib.Path` (sin rutas absolutas hardcodeadas).
2. Imprime `shape`, `dtypes` y `isna().sum()`.
3. Lista por escrito (comentario o markdown) **qué filas parecen inválidas** y por qué.
en ventas.csv la fila con unidades nulas es el quinto resgistro 
y la fila con el precio unitario negativo es el noveno registro 


## Parte 2 — Validación (10 min)

Implementa:

```python
import pandas as pd

def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Copiamos los datos para no modificar el DataFrame original.
    datos = frame.copy()

    # Convertimos ambas columnas a números.
    # Los valores vacíos o que no se puedan convertir pasan a NaN.
    datos["unidades"] = pd.to_numeric(datos["unidades"], errors="coerce")
    datos["precio_unitario"] = pd.to_numeric(
        datos["precio_unitario"], errors="coerce"
    )

    # Ambas condiciones deben cumplirse para que la fila sea válida.
    es_valida = (
        (datos["unidades"] > 0)
        & (datos["precio_unitario"] > 0)
    )

    validos = datos[es_valida].copy()
    errores = datos[~es_valida].copy()

    # Calculamos el importe solo para las ventas válidas.
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]

    return validos, errores
```

Reglas mínimas:

- `unidades` numérica y `> 0`
- `precio_unitario` numérico y `> 0`
- columnas derivadas: `importe = unidades * precio_unitario` solo en válidos

Devuelve `(validos, errores)`.

**Checkpoint:** con el CSV del curso debes obtener **8 válidas** y **2 inválidas**.

## Parte 3 — Agregaciones (8 min)

Sobre `validos`:

1. Importe total por `region` (ordenado desc).

importe_por_region = (
    validos.groupby("region")["importe"]
    .sum()
    .sort_values(ascending=False)
)
print(importe_por_region)

2. Top 3 `producto` por importe.

top_productos = (
    validos.groupby("producto")["importe"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)
print(top_productos)

3. `cliente_id` con más de una compra.

compras_por_cliente = validos["cliente_id"].value_counts()
clientes_repetidos = compras_por_cliente[compras_por_cliente > 1]

print(clientes_repetidos)

## Parte 4 — Exportación (4 min)

Escribe:

- `Datos/ventas_limpias.csv`
- `Datos/calidad_datos.json` con:
  - `filas_totales`, `filas_validas`, `filas_invalidas`, `importe_total`


from pathlib import Path
import json

# Ruta de la carpeta donde guardar los archivos.
carpeta = Path("Datos")
carpeta.mkdir(parents=True, exist_ok=True)

# Guardar las ventas válidas sin el índice de pandas.
validos.to_csv(carpeta / "ventas_limpias.csv", index=False)

# Preparar el resumen.
resumen = {
    "filas_totales": len(validos) + len(errores),
    "filas_validas": len(validos),
    "filas_invalidas": len(errores),
    "importe_total": float(validos["importe"].sum())
}

# Guardar el resumen en formato JSON.
with (carpeta / "calidad_datos.json").open("w", encoding="utf-8") as archivo:
    json.dump(resumen, archivo, indent=4, ensure_ascii=False)

  

## Extensión si terminas pronto

- Añade `fecha` como `datetime` y un agregado por semana.
- Refactoriza en funciones `cargar` / `validar` / `agregar` / `exportar` (adelanto sesión 22).

## Entrega orientativa

Código en tu repo del Proyecto I + captura o commit donde se vea el JSON de calidad.
