# Dashboard de Monitoreo Comercial Sector Retail

## 1. Descripción General

Esta es una aplicación web interactiva construida con Dash y Plotly en Python, diseñada para el análisis de datos comerciales de retail. La aplicación permite a los usuarios cargar datos de ventas y arrendamientos para visualizar y explorar el rendimiento a través de una serie de indicadores clave (KPIs), gráficos dinámicos y análisis de segmentación.

El objetivo principal de este dashboard es proporcionar una herramienta flexible para:
* Monitorear la salud general del negocio a través de KPIs clave.
* Comparar el rendimiento año a año (Year-over-Year) de diferentes métricas.
* Analizar la eficiencia de las marcas y ubicaciones.
* Realizar comparaciones directas entre diferentes escenarios (periodos, grupos de tiendas/marcas).
* Permitir un análisis exploratorio libre por parte del usuario.

## 2. Archivos de Datos Requeridos

La aplicación requiere dos archivos Excel en la misma carpeta que el script de Python:

**1. `VENTAS_ALL_BRANDS.xlsx`**
   * Contiene los datos transaccionales o de ventas diarias.
   * **Columnas requeridas:** `UBICACION`, `CIUDAD`, `FECHA`, `MARCA`, `VENTA`, `UNIDADES`, `TICKETS`.

**2. `ARRENDAMIENTOS.xlsx`**
   * Contiene la información de los espacios físicos y sus costos de alquiler.
   * **Columnas requeridas:** `UBICACION`, `MARCA`, `CANON FIJO`, `Mt2`.
   * **Granularidad de los Datos (MUY IMPORTANTE):**
     * Cada fila en este archivo debe representar una combinación única de `UBICACION` y `MARCA`.
     * El script espera encontrar un solo valor de `Mt2` y un solo valor de `Canon_Fijo` (mensual) para cada tienda específica.

## 3. Cómo Ejecutar la Aplicación

1.  Asegúrate de tener todos los archivos (`tu_script.py`, `VENTAS_ALL_BRANDS.xlsx`, `ARRENDAMIENTOS.xlsx`) en la misma carpeta.
2.  Instala las librerías necesarias: `pip install dash dash-bootstrap-components pandas numpy plotly openpyxl`
3.  Abre una terminal o "Anaconda Prompt".
4.  Navega a la carpeta del proyecto usando el comando `cd`.
5.  Ejecuta el comando: `python tu_script_app.py`
6.  Abre la dirección en tu navegador web.
"""
