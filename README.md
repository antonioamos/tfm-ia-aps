# TFM IA APS

Repositorio del Trabajo Fin de Máster centrado en la construcción y comparación de algoritmos de planificación avanzada de producción, APS (*Advanced Planning and Scheduling*), para un entorno industrial tipo Asprova.

El proyecto utiliza datos de órdenes, rutas de fabricación, recursos y tiempos de operación para generar cronogramas de producción y comparar distintas estrategias de planificación basadas en inteligencia artificial y optimización combinatoria.

## Objetivo del proyecto

El objetivo principal es evaluar diferentes enfoques para resolver un problema de *scheduling* industrial con recursos limitados, operaciones encadenadas, fechas de entrega y tiempos de proceso variables.

Se comparan principalmente tres familias de algoritmos:

- **Algoritmo genético**, usado como optimizador principal de secuencias de fabricación.
- **Modelo ensemble / XGBoost**, usado para generar reglas de prioridad y apoyar la planificación.
- **Modelo neuronal MLP/GNN**, entrenado para aprender políticas de planificación a partir de resultados del algoritmo genético.

Además, el repositorio incluye una comparativa global de resultados para analizar qué enfoque se comporta mejor según diferentes criterios: cumplimiento de fechas, *makespan*, carga planificada en fecha, número de órdenes tarde y función de fitness.

## Estructura del repositorio

```text
tfm-ia-aps-master/
├── algoritmos/
│   ├── aps_genetico.ipynb
│   ├── aps_ensemble.ipynb
│   ├── aps_neuronal.ipynb
│   ├── comparativa_algoritmos_aps.ipynb
│   └── output/
│       ├── ga_*.csv / ga_*.json / ga_*.png
│       ├── ens_*.csv / ens_*.json / ens_*.png
│       ├── nn_*.csv / nn_*.json / nn_*.png
│       └── comparativa_algoritmos/
├── datos_ofuscados/
│   ├── CCP.csv
│   ├── LPA_GAM.csv
│   ├── LPA_GSM.csv
│   └── PLAN.csv
├── informes/
│   └── informe_algoritmos.txt
├── ofuscar.py
└── .gitignore
```

## Descripción de carpetas

### `algoritmos/`

Contiene los notebooks principales del proyecto.

| Notebook | Descripción |
| --- | --- |
| `aps_genetico.ipynb` | Implementa el algoritmo genético para construir secuencias de planificación. Evalúa fitness, cumplimiento de fechas, utilización de recursos y genera salidas tipo plan APS. |
| `aps_ensemble.ipynb` | Implementa una aproximación basada en reglas de prioridad y XGBoost/ensemble para generar secuencias de planificación comparables. |
| `aps_neuronal.ipynb` | Implementa modelos neuronales MLP/GNN supervisados por el algoritmo genético para aprender políticas de priorización. |
| `comparativa_algoritmos_aps.ipynb` | Consolida resultados de GA, ensemble y red neuronal. Genera tablas y gráficos comparativos para el informe final. |

### `algoritmos/output/`

Contiene los resultados generados por los notebooks:

- Planificaciones exportadas en CSV.
- Métricas por algoritmo.
- Métricas por orden y por recurso.
- Validaciones de restricciones duras.
- Gráficos de Gantt.
- Gráficos de convergencia y comparativas.
- Resúmenes trazables en JSON.

Ejemplos de archivos relevantes:

```text
ga_resultados.csv
ga_resumen_experimento_aps.json
ga_validacion_schedule.json
ens_resultados.csv
ens_xgboost_metricas.csv
nn_resultados.csv
nn_modelo_prioridad_ga_metricas.csv
comparativa_algoritmos/comparativa_algoritmos_resumen.csv
comparativa_algoritmos/ganadores_por_criterio.csv
```

### `datos/`

Contiene los datos originales de entrada:

| Archivo | Descripción |
| --- | --- |
| `PLAN.csv` | Órdenes de fabricación, cantidades, centros, fechas de proveedor, fechas de entrega y cliente. |
| `CCP.csv` | Datos de operaciones por `PARTNUMBER`: operación, recurso, tecnología, tiempos fijos, tiempos variables y OEE. |
| `LPA_GAM.csv` | Planificación histórica o base para la planta GAM. |
| `LPA_GSM.csv` | Planificación histórica o base para la planta GSM. |

### `datos_ofuscados/`

Contiene una versión anonimizada/ofuscada de los datos originales. Los notebooks están preparados para localizar preferentemente esta carpeta cuando existe.

Esta carpeta permite ejecutar y validar el proyecto sin exponer identificadores sensibles como órdenes, clientes, partnumbers, recursos o centros reales.

### `tipos_datos/`

Incluye metadatos de columnas y tipos de datos procedentes de las tablas originales. Se usa especialmente para identificar campos de texto que deben ofuscarse.

### `reglas_ofuscacion/`

Incluye `REGLA_OFUSCACION.csv`, con la relación entre valor original y valor ofuscado.

> Este archivo puede contener información sensible, porque permite revertir o interpretar la ofuscación. No debería compartirse públicamente si los datos reales son confidenciales.

### `informes/`

Incluye documentación técnica del análisis de algoritmos, justificación del enfoque y recomendaciones.

### `ofuscar.py`

Script para generar los datos ofuscados a partir de los CSV originales. Sustituye valores textuales por identificadores genéricos del tipo:

```text
PARTNUMBER_0
ORDEN_15
CLIENTE_3
RECURSO_21
```

El script conserva la relación entre valores iguales en diferentes archivos cuando comparten nombre de columna.

## Datos de entrada

Los notebooks trabajan con cuatro fuentes principales:

| Dataset | Registros aproximados | Uso |
| --- | ---: | --- |
| `CCP.csv` | 35.789 | Rutas, operaciones, tecnologías, recursos, tiempos y OEE. |
| `PLAN.csv` | 14.983 | Órdenes planificables y fechas objetivo. |
| `LPA_GAM.csv` | 6.770 | Planificación/base histórica de la planta GAM. |
| `LPA_GSM.csv` | 6.059 | Planificación/base histórica de la planta GSM. |

Los CSV utilizan `;` como separador.

## Requisitos

Proyecto desarrollado en Python usando notebooks de Jupyter.

Versión recomendada:

- Python 3.10 o superior.
- Jupyter Notebook o JupyterLab.
- Entorno virtual de Python.

Dependencias principales inferidas del proyecto:

```text
pandas
numpy
matplotlib
scikit-learn
xgboost
torch
jupyter
ipykernel
```

Dependencias opcionales para ampliaciones o experimentación:

```text
lightgbm
catboost
seaborn
```

> Actualmente el repositorio no incluye `requirements.txt`. Se recomienda añadirlo para facilitar la reproducibilidad.

## Instalación

Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd tfm-ia-aps-master
```

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Linux/macOS:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install --upgrade pip
pip install pandas numpy matplotlib scikit-learn xgboost torch jupyter ipykernel
```

Registrar el kernel de Jupyter:

```bash
python -m ipykernel install --user --name tfm-ia-aps --display-name "Python (TFM IA APS)"
```

Abrir Jupyter:

```bash
jupyter lab
```

O bien:

```bash
jupyter notebook
```

## Ejecución recomendada

El orden recomendado de ejecución es:

```text
1. algoritmos/aps_genetico.ipynb
2. algoritmos/aps_ensemble.ipynb
3. algoritmos/aps_neuronal.ipynb
4. algoritmos/comparativa_algoritmos_aps.ipynb
```

Se recomienda ejecutar primero el algoritmo genético porque el notebook neuronal utiliza resultados del GA como referencia o supervisión en determinados escenarios.

## Funcionamiento general

Los notebooks siguen una lógica común:

1. Localización automática de rutas del proyecto.
2. Carga de `PLAN.csv`, `CCP.csv`, `LPA_GAM.csv` y `LPA_GSM.csv`.
3. Limpieza de órdenes no planificables o sin datos CCP suficientes.
4. Generación de recursos disponibles a partir de LPA.
5. Inferencia de grupos de recurso para operaciones CCP.
6. Construcción de rutas de fabricación por `PARTNUMBER`.
7. Construcción de operaciones planificables desde `PLAN.csv`.
8. Decodificación de secuencias en un calendario de producción.
9. Evaluación de métricas.
10. Exportación de resultados y validaciones.

## Parámetros principales

Los notebooks incluyen parámetros ajustables en sus primeras secciones.

Algunos de los más importantes son:

| Parámetro | Descripción |
| --- | --- |
| `RANDOM_SEED` | Semilla de aleatoriedad para reproducibilidad. |
| `MODO_PLANIFICACION_ORDENES` | Modo de selección de órdenes. En los notebooks aparece como `SOLO_LPA`. |
| `MAX_ORDENES` | Límite opcional de órdenes para pruebas rápidas. Si es `None`, se ejecuta con todas las órdenes planificables. |
| `PESO_FECHA` | Peso del cumplimiento de fechas en la función objetivo. |
| `POP_SIZE` | Tamaño de población en el algoritmo genético. |
| `MAX_GEN` | Número máximo de generaciones del algoritmo genético. |
| `CX_PB` | Probabilidad de cruce. |
| `MUT_PB` | Probabilidad de mutación. |
| `ELITE_SIZE` | Número de individuos élite conservados por generación. |

En los experimentos principales aparece `PESO_FECHA = 0.85`, dando prioridad al cumplimiento de fechas frente a la minimización pura del *makespan*.

## Métricas utilizadas

Los algoritmos se comparan mediante métricas como:

| Métrica | Significado |
| --- | --- |
| `fitness` | Valor objetivo global usado para comparar soluciones. Menor es mejor. |
| `makespan_days` | Duración total del plan en días. Menor es mejor. |
| `tardy_orders` | Número de órdenes entregadas tarde. Menor es mejor. |
| `on_time_rate` | Porcentaje de órdenes entregadas en fecha. Mayor es mejor. |
| `workload_hours` | Carga total planificada en horas. |
| `on_time_workload_rate` | Porcentaje de carga entregada en fecha. Mayor es mejor. |
| `total_late_days` | Suma total de días de retraso. Menor es mejor. |
| `max_late_days` | Máximo retraso individual. Menor es mejor. |
| `utilization` | Utilización aproximada de los recursos. Mayor suele ser mejor, aunque depende del objetivo. |
| `missing_ops` | Operaciones no planificadas. Debe ser 0 en una planificación válida. |

## Resultados principales

La carpeta `algoritmos/output/` contiene resultados ya generados para los tres enfoques.

La comparativa final se encuentra en:

```text
algoritmos/output/comparativa_algoritmos/
```

Archivos destacados:

| Archivo | Descripción |
| --- | --- |
| `comparativa_algoritmos_resumen.csv` | Tabla consolidada con métricas por algoritmo y escenario. |
| `ganadores_por_criterio.csv` | Ganador por escenario y criterio de evaluación. |
| `fitness_por_algoritmo.png` | Comparación visual del fitness. |
| `makespan_por_algoritmo.png` | Comparación visual de duración total del plan. |
| `porcentaje_ordenes_en_fecha.png` | Comparación del cumplimiento de fechas. |
| `frontera_makespan_vs_cumplimiento.png` | Frontera de compromiso entre duración y cumplimiento. |

Según los resultados consolidados, el algoritmo genético funciona como una de las soluciones más sólidas para el problema, especialmente como optimizador base. Los modelos neuronales pueden mejorar algunos criterios concretos de cumplimiento en determinados escenarios, mientras que el enfoque ensemble/XGBoost resulta útil como comparación y como apoyo para reglas de prioridad.

## Validación de restricciones

Cada notebook genera un archivo de validación, por ejemplo:

```text
ga_validacion_schedule.json
ens_validacion_schedule.json
nn_validacion_schedule.json
```

Estos archivos permiten comprobar que la planificación respeta restricciones básicas como:

- Operaciones esperadas frente a operaciones planificadas.
- Operaciones faltantes.
- Solapes o inconsistencias de planificación.
- Uso de recursos disponibles.

## Ofuscación de datos

Para generar los datos ofuscados se utiliza:

```bash
python ofuscar.py
```

Importante: el script contiene rutas absolutas configuradas para un entorno concreto:

```python
DATA_DIR = "/workspace/projects/tfm/datos"
OUT_DIR = "/workspace/projects/tfm/datos_ofuscados"
RULES_DIR = "/workspace/projects/tfm/reglas_ofuscacion"
```

Antes de ejecutarlo en otro equipo, conviene adaptar esas rutas o modificar el script para calcularlas de forma relativa al directorio del repositorio.

## Reproducibilidad

Para mejorar la reproducibilidad del proyecto se recomienda:

1. Añadir un `requirements.txt` con versiones cerradas de dependencias.
2. Documentar la versión exacta de Python usada.
3. Mantener los datos ofuscados como fuente de ejecución por defecto.
4. Evitar subir datos originales sensibles si el repositorio va a compartirse.
5. Ejecutar los notebooks en el orden recomendado.
6. Conservar los JSON de resumen para trazabilidad de cada experimento.

Ejemplo de `requirements.txt` recomendado:

```text
pandas
numpy
matplotlib
scikit-learn
xgboost
torch
jupyter
ipykernel
```

## Problemas frecuentes

### `FileNotFoundError: No se encontraron PLAN.csv y CCP.csv`

Comprueba que la estructura del proyecto conserva alguna de estas rutas:

```text
datos_ofuscados/PLAN.csv
datos_ofuscados/CCP.csv
datos/PLAN.csv
datos/CCP.csv
```

Los notebooks buscan primero datos ofuscados y después otras rutas conocidas.

### Error al importar `xgboost`

Instalar la dependencia:

```bash
pip install xgboost
```

### Error al importar `torch`

Instalar PyTorch:

```bash
pip install torch
```

En equipos con GPU, consultar la instalación específica recomendada por PyTorch para la versión de CUDA correspondiente.

### Resultados distintos entre ejecuciones

Aunque se usa `RANDOM_SEED = 42`, algunos procesos pueden variar ligeramente según versiones de librerías, sistema operativo o backend de ejecución. Para resultados totalmente reproducibles, fijar versiones exactas en `requirements.txt`.

## Posibles mejoras futuras

- Crear scripts `.py` reutilizables a partir de los notebooks.
- Añadir `requirements.txt` o `pyproject.toml`.
- Añadir pruebas automáticas para validación de restricciones del schedule.
- Parametrizar rutas y escenarios mediante argumentos o archivo YAML.
- Añadir documentación específica de cada métrica.
- Integrar un pipeline reproducible de ejecución completa.
- Explorar modelos GNN/RL más avanzados para scheduling dinámico.
- Añadir exportación directa a formatos compatibles con herramientas APS externas.

## Licencia

Proyecto académico desarrollado como parte de un Trabajo Fin de Máster.

Los datos originales están ofuscados para no incumplir con políticas de NDA.

## Autoría

Trabajo Fin de Máster sobre aplicación de inteligencia artificial a planificación avanzada de producción APS.

