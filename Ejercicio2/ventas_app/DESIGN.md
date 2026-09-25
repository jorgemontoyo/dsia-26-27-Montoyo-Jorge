# Diseño

- SRP — `SalesValidator` en `validator.py` se encarga únicamente
  de validar los registros y no realiza lectura ni escritura de ficheros.

- OCP — `SalesMetrics` en `metrics.py` permite añadir nuevas métricas
  sin modificar la lógica de carga o validación.

- DIP — `SalesRepository` en `loader.py` define el contrato de lectura,
  permitiendo sustituir el repositorio CSV por otra implementación.