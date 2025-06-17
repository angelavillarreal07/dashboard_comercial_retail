import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import dash_auth



# --- 1. DEFINICIÓN DE ESTILOS Y COORDENADAS ---
STYLE_FONT_FAMILY = "Arial, Helvetica, sans-serif"
COLOR_FONDO_APP = '#f8f9fa'
COLOR_FONDO_GRAFICO = '#FFFFFF'
COLOR_PRIMARIO_AZUL = '#0D6EFD'
COLOR_TEXTO_OSCURO = '#343a40'
COLOR_TEXTO_SECUNDARIO = '#6c757d'
TAB_STYLE = {'backgroundColor': '#f8f9fa', 'color': COLOR_TEXTO_SECUNDARIO, 'borderBottom': '1px solid #dee2e6', 'padding': '6px', 'fontFamily': STYLE_FONT_FAMILY}
TAB_SELECTED_STYLE = {'backgroundColor': COLOR_FONDO_GRAFICO, 'color': COLOR_PRIMARIO_AZUL, 'borderTop': f'2px solid {COLOR_PRIMARIO_AZUL}', 'fontWeight': 'bold', 'padding': '6px', 'fontFamily': STYLE_FONT_FAMILY}
PALETA_COLORES = px.colors.qualitative.Plotly

CITY_COORDS = {
    'BARQUISIMETO': {'lat': 10.0710, 'lon': -69.3220},
    'MARACAIBO': {'lat': 10.6420, 'lon': -71.6090},
    'MAIQUETIA': {'lat': 10.6032, 'lon': -66.9698},
    'CARACAS': {'lat': 10.4806, 'lon': -66.9036},
    'CIUDAD GUAYANA': {'lat': 8.3530, 'lon': -62.6424},
    'MARGARITA': {'lat': 10.9577, 'lon': -63.8724},
    'PUERTO CABELLO': {'lat': 10.4800, 'lon': -68.0125},
    'SAN CRISTOBAL': {'lat': 7.7669, 'lon': -72.2250},
    'VALENCIA': {'lat': 10.1620, 'lon': -68.0077},
    'TOLON': {'lat': 10.4806, 'lon': -66.9036},
    'LIDER': {'lat': 10.4984, 'lon': -66.8524},
    'SAMBIL CHACAO': {'lat': 10.4990, 'lon': -66.8500},
    'PAMPATAR': {'lat': 10.9579, 'lon': -63.8732},
    'LOS TEQUES': {'lat': 10.3446, 'lon': -67.0422},
    'LA GUAIRA': {'lat': 10.6000, 'lon': -66.9333},
    'MARACAY': {'lat': 10.2469, 'lon': -67.5958},
    
    # Sambil específicos
    'SAMBIL CARACAS': {'lat': 10.4989, 'lon': -66.8500},
    'SAMBIL VALENCIA': {'lat': 10.1708, 'lon': -68.0046},
    'SAMBIL MARACAIBO': {'lat': 10.6541, 'lon': -71.6372},
    'SAMBIL MARGARITA': {'lat': 10.9991, 'lon': -63.8212},
    'SAMBIL BARQUISIMETO': {'lat': 10.0801, 'lon': -69.3450},
    'SAMBIL SAN CRISTOBAL': {'lat': 7.7686, 'lon': -72.2239},
    'SAMBIL LA CANDELARIA': {'lat': 10.5043, 'lon': -66.9042}
}
# Texto del archivo README para la descarga
README_TEXT = """
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
# --- 2. FUNCIÓN DE CARGA Y PREPARACIÓN DE DATOS ---
def cargar_y_preparar_datos():
    try:
        # Intenta cargar los archivos reales
        df_ventas_full = pd.read_excel('VENTAS_ALL_BRANDS.xlsx')
        df_arrendamientos_full = pd.read_excel('ARRENDAMIENTOS.xlsx')
        print("✅ Archivos de datos reales cargados correctamente.")
        
        # Eliminar duplicados de los archivos reales
        df_ventas_full.drop_duplicates(inplace=True)
        df_arrendamientos_full.drop_duplicates(inplace=True)

    except FileNotFoundError:
        # Si los archivos no se encuentran, genera datos de ejemplo avanzados
        print("ADVERTENCIA: Archivos Excel no encontrados. Generando datos de ejemplo para demostración pública.")
        
        np.random.seed(42) # Para que los datos aleatorios sean siempre los mismos

        # --- Perfiles de Marcas para Segmentación ---
        brand_profiles = [
            {'MARCA': 'AURA', 'tipo': 'Lujo', 'precio_promedio': 250, 'factor_volumen': 0.6},
            {'MARCA': 'LUMIN', 'tipo': 'Fast Fashion', 'precio_promedio': 40, 'factor_volumen': 1.8},
            {'MARCA': 'ZIRCON', 'tipo': 'Equilibrado', 'precio_promedio': 90, 'factor_volumen': 1.1},
            {'MARCA': 'ONYX', 'tipo': 'Bajo Rendimiento', 'precio_promedio': 35, 'factor_volumen': 0.5},
            {'MARCA': 'SOLARA', 'tipo': 'Premium', 'precio_promedio': 180, 'factor_volumen': 0.8},
            {'MARCA': 'NOCTIS', 'tipo': 'Alto Tráfico', 'precio_promedio': 50, 'factor_volumen': 1.5},
        ]
        marcas_ejemplo = [p['MARCA'] for p in brand_profiles]
        
        ubicaciones_por_ciudad = {
            'CARACAS': ['SAMBIL LA CANDELARIA', 'TOLON', 'LIDER', 'SAMBIL CHACAO'],
            'VALENCIA': ['SAMBIL VALENCIA'],
            'MARACAIBO': ['SAMBIL MARACAIBO'],
            'BARQUISIMETO': ['SAMBIL BARQUISIMETO'],
        }

        # --- Crear DataFrames Ficticios Basados en Perfiles ---
        arrend_data = []
        for ciudad, ubicaciones in ubicaciones_por_ciudad.items():
            for ubicacion in ubicaciones:
                # Asignar marcas aleatorias a cada ubicación
                marcas_en_ubicacion = np.random.choice(marcas_ejemplo, size=np.random.randint(3, len(marcas_ejemplo)), replace=False)
                for marca_nombre in marcas_en_ubicacion:
                    arrend_data.append({
                        'UBICACION': ubicacion, 'MARCA': marca_nombre, 'CIUDAD': ciudad,
                        'Mt2': np.random.randint(80, 250),
                        'CANON FIJO': np.random.randint(1500, 8000) * (1.5 if ciudad == 'CARACAS' else 1) # Canon más caro en Caracas
                    })
        df_arrendamientos_full = pd.DataFrame(arrend_data)

        ventas_data = []
        fechas_ejemplo = pd.to_datetime(pd.date_range(start='2023-01-01', end='2025-12-31', freq='D'))
        
        # Crear un mapa de perfiles para búsqueda rápida
        perfiles_map = {p['MARCA']: p for p in brand_profiles}

        for index, store in df_arrendamientos_full.iterrows():
            perfil = perfiles_map[store['MARCA']]
            for fecha in fechas_ejemplo:
                if np.random.rand() > 0.3: # 70% de probabilidad de tener ventas
                    
                    # Generar tickets basados en el perfil de la marca
                    base_tickets = np.random.randint(5, 50)
                    tickets = max(1, int(base_tickets * perfil['factor_volumen']))

                    # Generar unidades y ventas basados en los tickets y el precio promedio
                    unidades = max(tickets, int(tickets * np.random.uniform(1.1, 2.5)))
                    venta = unidades * perfil['precio_promedio'] * np.random.uniform(0.85, 1.15) # Pequeña variación de precio
                    
                    ventas_data.append({
                        'FECHA': fecha, 'MARCA': store['MARCA'], 'UBICACION': store['UBICACION'],
                        'CIUDAD': store['CIUDAD'], 'VENTA': venta, 'UNIDADES': unidades, 'TICKETS': tickets
                    })
        df_ventas_full = pd.DataFrame(ventas_data)


    # --- Procesamiento de datos 
    df_ventas = df_ventas_full.copy()
    df_ventas.columns = [str(col).strip().upper() for col in df_ventas.columns]
    df_ventas.rename(columns={'VENTA': 'VENTAS', 'UNIDADES': 'UNIDADES', 'TICKETS': 'TICKETS'}, inplace=True, errors='ignore')
    if 'FECHA' in df_ventas.columns: df_ventas.rename(columns={'FECHA': 'FECHA_DATETIME'}, inplace=True)
    
    # ... 
   
    
    df_ventas['MARCA'] = df_ventas['MARCA'].astype(str).str.strip() 
    df_ventas['UBICACION'] = df_ventas['UBICACION'].astype(str).str.strip()
    df_ventas['CIUDAD'] = df_ventas['CIUDAD'].astype(str).str.strip().str.upper()
    for col in ['VENTAS', 'UNIDADES', 'TICKETS']: df_ventas[col] = pd.to_numeric(df_ventas[col], errors='coerce')
    df_ventas.dropna(subset=['VENTAS', 'UNIDADES', 'TICKETS', 'FECHA_DATETIME', 'MARCA', 'UBICACION', 'CIUDAD'], inplace=True)
    df_ventas['FECHA_DATETIME'] = pd.to_datetime(df_ventas['FECHA_DATETIME'], dayfirst=True, errors='coerce')
    df_ventas.dropna(subset=['FECHA_DATETIME'], inplace=True)
    df_ventas['AÑO'] = df_ventas['FECHA_DATETIME'].dt.year

    df_arrendamientos = df_arrendamientos_full.copy()
    df_arrendamientos.columns = [str(col).strip().lower().replace(" ", "_") for col in df_arrendamientos.columns]
    arrend_rename_map = {'canon_fijo': 'Canon_Fijo', 'mt2': 'Metros_Cuadrados', 'marca': 'MARCA', 'ubicacion': 'UBICACION'}
    df_arrendamientos.rename(columns=arrend_rename_map, inplace=True)
    df_arrendamientos['MARCA'] = df_arrendamientos['MARCA'].astype(str).str.strip().str.upper()
    df_arrendamientos['UBICACION'] = df_arrendamientos['UBICACION'].astype(str).str.strip().str.upper()
    if 'Metros_Cuadrados' in df_arrendamientos.columns: df_arrendamientos['Metros_Cuadrados'] = pd.to_numeric(df_arrendamientos['Metros_Cuadrados'], errors='coerce')
    if 'Canon_Fijo' in df_arrendamientos.columns: df_arrendamientos['Canon_Fijo'] = pd.to_numeric(df_arrendamientos['Canon_Fijo'], errors='coerce')
    df_arrendamientos.dropna(subset=['UBICACION', 'MARCA', 'Metros_Cuadrados', 'Canon_Fijo'], inplace=True)
    df_arrendamientos_unicos = df_arrendamientos.drop_duplicates(subset=['UBICACION', 'MARCA'], keep='first')

    df_completo = pd.merge(df_ventas, df_arrendamientos_unicos, on=['UBICACION', 'MARCA'], how='left')
    
    return df_completo

df_global_completo = cargar_y_preparar_datos()

# --- 3. Inicialización de la App Dash ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP]) # <-- AÑADIR dbc.icons.BOOTSTRAP
server = app.server

opciones_ubicacion = [{'label': i, 'value': i} for i in sorted(df_global_completo['UBICACION'].unique())] if not df_global_completo.empty else []
opciones_marca = [{'label': i, 'value': i} for i in sorted(df_global_completo['MARCA'].unique())] if not df_global_completo.empty else []

# Definición de los paneles de filtros por separado
panel_filtros_general = html.Div(
    id='contenedor-filtros-general', 
    style={'display': 'block'}, # Empieza visible
    children=[
        html.H4("Menú de Navegación"), html.Hr(),
        dbc.Card(dbc.CardBody([
            dbc.Label("Rango de Fechas:"),
            dcc.DatePickerRange(id='filtro-fecha', min_date_allowed=df_global_completo['FECHA_DATETIME'].min().date() if not df_global_completo.empty else None, max_date_allowed=df_global_completo['FECHA_DATETIME'].max().date() if not df_global_completo.empty else None, start_date=df_global_completo['FECHA_DATETIME'].min().date() if not df_global_completo.empty else None, end_date=df_global_completo['FECHA_DATETIME'].max().date() if not df_global_completo.empty else None, className="w-100"),
            html.Br(), html.Br(), dbc.Label("Ubicación(es):"),
            dcc.Dropdown(id='filtro-ubicacion', multi=True, placeholder="Todas", options=opciones_ubicacion),
            html.Br(), dbc.Label("Marca(s):"),
            dcc.Dropdown(id='filtro-marca', multi=True, placeholder="Todas", options=opciones_marca),
            html.Br(), html.Br(),
            dbc.Button("Descargar Documentación", id="btn-descargar-readme", color="secondary", outline=True, size="sm", className="w-100"),
        ]), color="light")
    ]
)

panel_filtros_comparativo = html.Div(
    id='contenedor-filtros-comparativo', 
    style={'display': 'none'}, # Empieza oculto
    children=[
        html.H4("Menú Comparativo"), html.Hr(),
        dbc.Card(dbc.CardBody([
            html.H6("Selección 1", className="card-title text-primary"),
            dbc.Label("Fechas 1:"), dcc.DatePickerRange(id='filtro-fecha-1', start_date='2024-01-01', end_date='2024-12-31', className="w-100", display_format='DD/MM/YYYY'),
            dbc.Label("Ubicación(es) 1:", className="mt-2"), dcc.Dropdown(id='filtro-ubicacion-1', multi=True, placeholder="Todas", options=opciones_ubicacion),
            dbc.Label("Marca(s) 1:", className="mt-2"), dcc.Dropdown(id='filtro-marca-1', multi=True, placeholder="Todas", options=opciones_marca),
        ]), color="light", className="mb-3"),
        dbc.Card(dbc.CardBody([
            html.H6("Selección 2", className="card-title text-danger"),
            dbc.Label("Fechas 2:"), dcc.DatePickerRange(id='filtro-fecha-2', start_date='2025-01-01', end_date='2025-12-31', className="w-100", display_format='DD/MM/YYYY'),
            dbc.Label("Ubicación(es) 2:", className="mt-2"), dcc.Dropdown(id='filtro-ubicacion-2', multi=True, placeholder="Todas", options=opciones_ubicacion),
            dbc.Label("Marca(s) 2:", className="mt-2"), dcc.Dropdown(id='filtro-marca-2', multi=True, placeholder="Todas", options=opciones_marca),
        ]), color="light")
    ]
)

app.layout = html.Div(style={'backgroundColor': COLOR_FONDO_APP, 'padding': '20px', 'fontFamily': STYLE_FONT_FAMILY}, children=[
    dcc.Store(id='memoria-ciudad-clickeada'),
    dcc.Download(id="descarga-readme"),
    dbc.Container([
        html.Div(id='kpi-container', children=[
            dbc.Row([
                dbc.Col(html.H2("Monitoreo Comercial en Retail"), width=12, lg=4, className="my-auto"),
                dbc.Col(dbc.Row(id='kpi-cards-container'), width=12, lg=8)
            ], className="mb-4 align-items-center")
        ]),
        html.Hr(),
        dbc.Row([
            # La columna de la izquierda ahora contiene ambos paneles definidos arriba
            dbc.Col([panel_filtros_general, panel_filtros_comparativo], width=12, lg=3),
            
            dbc.Col([
                dcc.Tabs(id="tabs-analisis", value='tab-general', children=[
                    dcc.Tab(label='Análisis General', value='tab-general', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Segmentación de Marcas', value='tab-segmentacion', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Análisis Comparativo', value='tab-comparativo', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Análisis Exploratorio', value='tab-exploratorio', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                ]),
                html.Div(id='tabs-content', className="mt-3")
            ], width=12, lg=9)
        ])
    ], fluid=True)
])

# --- 5. Callbacks (Interactividad) ---


# Callback para cambiar el panel de filtros según la pestaña seleccionada
@app.callback(
    Output('panel-izquierdo-filtros', 'children'),
    Input('tabs-analisis', 'value')
)
def render_filter_panel(tab):
    # Estas opciones se usan en ambos paneles
    opciones_ubicacion = [{'label': i, 'value': i} for i in sorted(df_global_completo['UBICACION'].unique())] if not df_global_completo.empty else []
    opciones_marca = [{'label': i, 'value': i} for i in sorted(df_global_completo['MARCA'].unique())] if not df_global_completo.empty else []
    
    if tab == 'tab-comparativo':
        # Si la pestaña es "Análisis Comparativo", devuelve el layout con el doble juego de filtros
        return html.Div([
            html.H4("Menú Comparativo"), html.Hr(),
            dbc.Card(dbc.CardBody([
                html.H6("Selección 1", className="card-title text-primary"),
                dbc.Label("Fechas 1:"),
                dcc.DatePickerRange(id='filtro-fecha-1', start_date='2024-01-01', end_date='2024-12-31', className="w-100", display_format='DD/MM/YYYY'),
                html.Br(), html.Br(), dbc.Label("Ubicación(es) 1:"),
                dcc.Dropdown(id='filtro-ubicacion-1', multi=True, placeholder="Todas", options=opciones_ubicacion),
                html.Br(), dbc.Label("Marca(s) 1:"),
                dcc.Dropdown(id='filtro-marca-1', multi=True, placeholder="Todas", options=opciones_marca),
            ]), color="light", className="mb-3"),
            dbc.Card(dbc.CardBody([
                html.H6("Selección 2", className="card-title text-danger"),
                dbc.Label("Fechas 2:"),
                dcc.DatePickerRange(id='filtro-fecha-2', start_date='2025-01-01', end_date='2025-12-31', className="w-100", display_format='DD/MM/YYYY'),
                html.Br(), html.Br(), dbc.Label("Ubicación(es) 2:"),
                dcc.Dropdown(id='filtro-ubicacion-2', multi=True, placeholder="Todas", options=opciones_ubicacion),
                html.Br(), dbc.Label("Marca(s) 2:"),
                dcc.Dropdown(id='filtro-marca-2', multi=True, placeholder="Todas", options=opciones_marca),
            ]), color="light")
        ])
    else:
        # Para cualquier otra pestaña, devuelve el layout con un solo juego de filtros
        return html.Div([
            html.H4("Menú de Navegación"), html.Hr(),
            dbc.Card(dbc.CardBody([
                dbc.Label("Rango de Fechas:"),
                dcc.DatePickerRange(id='filtro-fecha', min_date_allowed=df_global_completo['FECHA_DATETIME'].min().date() if not df_global_completo.empty else None, max_date_allowed=df_global_completo['FECHA_DATETIME'].max().date() if not df_global_completo.empty else None, start_date=df_global_completo['FECHA_DATETIME'].min().date() if not df_global_completo.empty else None, end_date=df_global_completo['FECHA_DATETIME'].max().date() if not df_global_completo.empty else None, className="w-100"),
                html.Br(), html.Br(), dbc.Label("Ubicación(es):"),
                dcc.Dropdown(id='filtro-ubicacion', multi=True, placeholder="Todas", options=opciones_ubicacion),
                html.Br(), dbc.Label("Marca(s):"),
                dcc.Dropdown(id='filtro-marca', multi=True, placeholder="Todas", options=opciones_marca),
            ]), color="light")
        ])

# Callback para renderizar el contenido de la pestaña activa

@app.callback(Output('tabs-content', 'children'), Input('tabs-analisis', 'value'))
def render_tab_content(tab):
    if tab == 'tab-general':
        return html.Div([
            dbc.Alert(
                [
                    html.H4("Análisis de Rendimiento Anual según Rendimiento Diario", className="alert-heading"),
                    html.P(
                        "Esta sección muestra el desempeño de ventas y los principales KPI del retail con base en el comportamiento diario. El modelo de datos parte de registros de ventas diarios, que se agrupan por marca, ubicación y año. Estas se comparan con variables fijas como los metros cuadrados (Mt2) y el Canon Fijo, ajustando estas últimas proporcionalmente al período seleccionado."
                    ),
                    html.Hr(),
                    html.P(
                        "Este enfoque permite mantener la variable 'Fecha' como continua, facilitando análisis por día, mes, año o rango personalizado. Así, se pueden comparar métricas heterogéneas como ventas acumuladas y Canon mensual, transformando este último en un Canon total equivalente para el período seleccionado. Esto garantiza una base de comparación justa entre variables con diferentes niveles de granularidad.",
                        className="mb-0",
                    ),
                ],
                color="light", className="border"
            ),
            html.Hr(className="my-3"),
            dbc.Card(dbc.CardBody([
                html.H5("Rendimiento Geográfico por Ciudad", className="text-center"),
                dcc.Graph(id='mapa-ventas', style={'height': '60vh'})
            ])),
            html.Div(id='detalle-ciudad-container', className="mt-3"),
            html.Hr(className="my-4"),
            
            # a petición de Uldarico-
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Dinámico Anual de KPIs por Transacción", className="card-title"),
                dcc.RadioItems(
                    id='kpi-transaccion-radio',
                    options=[
                        {'label': 'Unidades / Ticket (UPT)', 'value': 'UPT'},
                        {'label': 'Ventas / Ticket (ATV)', 'value': 'ATV'},
                        {'label': 'Ventas / Unidad (ASP)', 'value': 'ASP'}
                    ],
                    value='UPT', 
                    inline=True, 
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-kpi-dinamico')
            ])),
            html.Br(),
            # 
            
            # Tarjeta de Ventas
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Dinámico de Ventas Anuales según Rendimiento Diario", className="card-title"),
                dcc.RadioItems(
                    id='ventas-radio',
                    options=[
                        {'label': 'Ventas Totales', 'value': 'VENTAS'},
                        {'label': 'Ventas / Mt2', 'value': 'Ventas_por_MT2'},
                        {'label': 'Ventas / Canon Fijo', 'value': 'Relacion_Ventas_Canon'},
                        {'label': 'Ventas / Ticket (ATV)', 'value': 'ATV'},
                        {'label': 'Ventas / Unidad (ASP)', 'value': 'ASP'}
                    ],
                    value='VENTAS',
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-ventas-dinamico')
            ])),
        html.Br(),
        # Tarjeta de Unidades
        dbc.Card(dbc.CardBody([
            html.H5("Análisis Dinámico de Unidades Anuales según Rendimiento Diario", className="card-title"),
            dcc.RadioItems(
                id='unidades-radio',
                options=[
                    {'label': 'Unidades Totales', 'value': 'UNIDADES'},
                    {'label': 'Unidades / Ticket (UPT)', 'value': 'UPT'},
                    {'label': 'Unidades / Mt2', 'value': 'Unidades_por_MT2'},
                    {'label': 'Unidades / Canon Fijo', 'value': 'Unidades_por_Canon'}
                ],
                value='UNIDADES',
                inline=True,
                labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                style={'margin-bottom': '10px'}
            ),
            dcc.Graph(id='grafico-unidades-dinamico')
        ])),

            html.Br(),

            # Tarjeta de Tickets
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Dinámico de Tickets Anuales según Rendimiento Diario", className="card-title"),
                dcc.RadioItems(
                    id='tickets-radio',
                    options=[
                    {'label': 'Tickets Totales', 'value': 'TICKETS'},
                    {'label': 'Tickets / Mt2', 'value': 'Tickets_por_MT2'},
                    {'label': 'Tickets / Canon Fijo', 'value': 'Tickets_por_Canon'}
                    ],
                    value='TICKETS',
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-tickets-dinamico')
            ]))

        ])
    elif tab == 'tab-segmentacion':
        return html.Div([
            dbc.Alert(
                [
                    html.H4("Segmentación de Marcas", className="alert-heading"),
                    html.P("Esta sección permite evaluar el rendimiento de ventas de cada marca con relación a dos variables espaciales clave del retail: los metros cuadrados ocupados (Mt2) y el Canon Fijo mensual."),
                    html.P("El objetivo es analizar:"),
                    html.Ul([
                        html.Li("Productividad del espacio: cuánto vende una marca por cada metro cuadrado ocupado."),
                        html.Li("Rentabilidad comercial: cuánta venta genera una marca por cada unidad monetaria pagada en Canon.")
                    ]),
                    html.P("Estas métricas permiten identificar marcas de alto rendimiento, oportunidades de mejora, y apoyar decisiones estratégicas sobre asignación de espacio o condiciones comerciales.", className="mb-0")
                ],
                color="light", className="border"
            ),
            html.Hr(className="my-3"),
            dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([html.H5("Segmentación por Eficiencia de Metros Cuadrados"), dcc.Graph(id='grafico-segmentacion-mt2', style={'height': '70vh'})])))]),
            html.Br(),
            dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([html.H5("Segmentación por Eficiencia de Canon Fijo"), dcc.Graph(id='grafico-segmentacion-canon', style={'height': '70vh'})])))])
        ])
    elif tab == 'tab-comparativo':
        return html.Div([
            dbc.Alert(
                [
                    html.H4("Análisis Comparativo", className="alert-heading"),
                    html.P("Esta sección permite comparar el desempeño entre dos segmentos —por ejemplo, distintas marcas, ubicaciones o periodos de tiempo— utilizando las mismas métricas estandarizadas del análisis general."),
                    html.Hr(),
                    html.P("El cálculo homogéneo de los indicadores (ajustando Canon por período y sumando ventas diarias) garantiza comparaciones justas entre segmentos con diferentes estructuras de datos o niveles de agregación. Esta herramienta es útil para entender brechas, tendencias o cambios interanuales.", className="mb-0"),
                ],
                color="light", className="border"
            ),
            html.Hr(className="my-3"),
            # a petición de Uldarico
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Comparativo de KPIs por Transacción", className="card-title"),
                dcc.RadioItems(
                    id='kpi-transaccion-radio-comp',
                    options=[
                        {'label': 'Unidades / Ticket (UPT)', 'value': 'UPT'},
                        {'label': 'Ventas / Ticket (ATV)', 'value': 'ATV'},
                        {'label': 'Ventas / Unidad (ASP)', 'value': 'ASP'}
                    ], value='UPT', 
                    inline=True, 
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-kpi-comparativo')
            ])),
            html.Br(),
            
            # Paneles interactivos para la comparación
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Comparativo de Ventas Anuales según Rendimiento Diario", className="card-title"),
                dcc.RadioItems(
                    id='ventas-radio-comp',
                    options=[
                        {'label': 'Ventas Totales', 'value': 'VENTAS'}, {'label': 'Ventas / Mt2', 'value': 'Ventas_por_MT2'},
                        {'label': 'Ventas / Canon Fijo', 'value': 'Relacion_Ventas_Canon'},
                        {'label': 'Ventas / Ticket (ATV)', 'value': 'ATV'},
                        {'label': 'Ventas / Unidad (ASP)', 'value': 'ASP'}
                    ], 
                    value='VENTAS',
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-ventas-comparativo')
            ])),
            html.Br(),
                        dbc.Card(dbc.CardBody([
                html.H5("Análisis Comparativo de Unidades Anuales según Rendimiento Diario", className="card-title"),
                dcc.RadioItems(
                    id='unidades-radio-comp',
                    options=[
                        {'label': 'Unidades Totales', 'value': 'UNIDADES'}, {'label': 'Unidades / Ticket (UPT)', 'value': 'UPT'},
                        {'label': 'Unidades / Mt2', 'value': 'Unidades_por_MT2'}, {'label': 'Unidades / Canon Fijo', 'value': 'Unidades_por_Canon'}
                    ], 
                    value='UNIDADES',
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-unidades-comparativo')
            ])),
            html.Br(),
            dbc.Card(dbc.CardBody([
                html.H5("Análisis Comparativo de Tickets Anuales según Rendimiento Diario", className="card-title"),
                dcc.RadioItems(
                    id='tickets-radio-comp',
                    options=[
                        {'label': 'Tickets Totales', 'value': 'TICKETS'}, {'label': 'Tickets / Mt2', 'value': 'Tickets_por_MT2'},
                        {'label': 'Tickets / Canon Fijo', 'value': 'Tickets_por_Canon'}
                    ], 
                    value='TICKETS',
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                    style={'margin-bottom': '10px'}
                ),
                dcc.Graph(id='grafico-tickets-comparativo')
            ]))
        ])

    elif tab == 'tab-exploratorio':
        # Opciones completas para los dropdowns del análisis exploratorio
        opciones_exploratorio = [
            {'label': 'Ventas Totales', 'value': 'VENTAS'},
            {'label': 'Unidades Totales', 'value': 'UNIDADES'},
            {'label': 'Tickets Totales', 'value': 'TICKETS'},
            {'label': 'Metros Cuadrados', 'value': 'Metros_Cuadrados'},
            {'label': 'Canon Fijo Mensual', 'value': 'Canon_Fijo'},
            {'label': 'Ventas / Mt2', 'value': 'Ventas_por_MT2'},
            {'label': 'Unidades / Mt2', 'value': 'Unidades_por_MT2'},
            {'label': 'Tickets / Mt2', 'value': 'Tickets_por_MT2'},
            {'label': 'Ventas / Canon', 'value': 'Ventas_por_Canon'},
            {'label': 'Unidades / Canon', 'value': 'Unidades_por_Canon'},
            {'label': 'Tickets / Canon', 'value': 'Tickets_por_Canon'},
            {'label': 'Ventas / Ticket (ATV)', 'value': 'ATV'},
            {'label': 'Unidades / Ticket (UPT)', 'value': 'UPT'},
            {'label': 'Ventas / Unidad (ASP)', 'value': 'ASP'}
        ]
        return html.Div([
            dbc.Alert(
                [
                    html.H4("Análisis Exploratorio", className="alert-heading"),
                    html.P("Esta sección permite explorar libremente el comportamiento de las variables de interés..."), # Texto completo aquí
                ], color="light", className="border"
            ),
            html.Hr(className="my-3"),
            dbc.Card(dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Variable para Eje X:"),
                        dcc.Dropdown(id='exploratorio-eje-x', options=opciones_exploratorio, value='Ventas_por_MT2')
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Variable para Eje Y:"),
                        dcc.Dropdown(id='exploratorio-eje-y', options=opciones_exploratorio, value='Tickets_por_MT2')
                    ], width=6)
                ]),
            ])),
            dcc.Graph(id='grafico-exploratorio', style={'height': '70vh'})
        ])
    
    return html.P("Selecciona una pestaña")

# --- 5. CALLBACKS Y FUNCIONES AUXILIARES ---

# --- Funciones Auxiliares (Helpers) ---
def filter_dataframe(df, selected_ubicaciones, selected_marcas, start_date, end_date):
    """Filtra el dataframe principal según las selecciones del usuario."""
    if not start_date or not end_date or df is None or df.empty:
        return pd.DataFrame()
    
    try:
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
    except Exception:
        return pd.DataFrame()

    df_filtrado = df.copy()
    if selected_ubicaciones: # Si la lista no está vacía
        df_filtrado = df_filtrado[df_filtrado['UBICACION'].isin(selected_ubicaciones)]
    if selected_marcas: # Si la lista no está vacía
        df_filtrado = df_filtrado[df_filtrado['MARCA'].isin(selected_marcas)]
    
    df_filtrado = df_filtrado[
        (df_filtrado['FECHA_DATETIME'] >= start_date_dt) & 
        (df_filtrado['FECHA_DATETIME'] <= end_date_dt)
    ]
    return df_filtrado

def create_empty_figure(message="Selecciona filtros para ver datos"):
    """Crea una figura vacía con un mensaje."""
    return {"layout": {"paper_bgcolor": COLOR_FONDO_GRAFICO, "plot_bgcolor": COLOR_FONDO_GRAFICO, "font": {"color": COLOR_TEXTO_OSCURO}, "annotations": [{"text": message, "showarrow": False, "font": {"size": 16}}]}}





# --- Callbacks ---


# Callback para cambiar el panel de filtros y los KPIs según la pestaña seleccionada
@app.callback(
    [Output('contenedor-filtros-general', 'style'),
     Output('contenedor-filtros-comparativo', 'style')],
    [Input('tabs-analisis', 'value')]
)
def toggle_filter_visibility(tab):
    """Muestra/oculta los paneles de filtros según la pestaña activa."""
    if tab == 'tab-comparativo':
        # Muestra filtros comparativos y oculta los generales
        return {'display': 'none'}, {'display': 'block'}
    else:
        # Muestra filtros generales y oculta los comparativos
        return {'display': 'block'}, {'display': 'none'}

# --- Callbacks para el Contenido de las Pestañas ---
@app.callback(
    Output('kpi-cards-container', 'children'),
    [Input('tabs-analisis', 'value'),
     # Inputs para el tab General
     Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date'),
     # Inputs para el tab Comparativo
     Input('filtro-ubicacion-1', 'value'), Input('filtro-marca-1', 'value'),
     Input('filtro-fecha-1', 'start_date'), Input('filtro-fecha-1', 'end_date'),
     Input('filtro-ubicacion-2', 'value'), Input('filtro-marca-2', 'value'),
     Input('filtro-fecha-2', 'start_date'), Input('filtro-fecha-2', 'end_date')]
)
def update_kpis(active_tab, 
                ub_gral, m_gral, sd_gral, ed_gral,
                u1, m1, s1, e1, u2, m2, s2, e2):

    # Previene que el callback se ejecute al inicio si los inputs no están listos
    triggered_id = dash.ctx.triggered_id
    if not triggered_id and active_tab != 'tab-general':
        return []
    
    if active_tab == 'tab-comparativo':
        # --- LÓGICA PARA KPIs COMPARATIVOS (CON 9 KPIs) ---
        if not all([s1, e1, s2, e2]): return []

        df1 = filter_dataframe(df_global_completo, u1, m1, s1, e1)
        df2 = filter_dataframe(df_global_completo, u2, m2, s2, e2)
        
        def calc_pct_change(new_val, old_val):
            if old_val > 0:
                return ((new_val - old_val) / old_val) * 100
            elif new_val > 0:
                return float('inf')
            return 0.0

        # --- Calcular para Selección 1 ---
        v1 = df1['VENTAS'].sum(); u1_total = df1['UNIDADES'].sum(); t1 = df1['TICKETS'].sum()
        m2_1 = df1.drop_duplicates(subset=['UBICACION', 'MARCA'])['Metros_Cuadrados'].sum()
        kpi_raw_1 = {
            "Total Ventas": v1, "Total Mt2": m2_1, "Total Tickets": t1, "Total Unidades": u1_total,
            "Ventas/Mt2": (v1 / m2_1) if m2_1 > 0 else 0,
            "Unidades/Ticket (UPT)": (u1_total / t1) if t1 > 0 else 0,
            "Ventas/Ticket (ATV)": (v1 / t1) if t1 > 0 else 0,
            "Artículo Prom. (ASP)": (v1 / u1_total) if u1_total > 0 else 0,
            #"Unidades/Mt2": (u1_total / m2_1) if m2_1 > 0 else 0
        }

        # --- Calcular para Selección 2 ---
        v2 = df2['VENTAS'].sum(); u2_total = df2['UNIDADES'].sum(); t2 = df2['TICKETS'].sum()
        m2_2 = df2.drop_duplicates(subset=['UBICACION', 'MARCA'])['Metros_Cuadrados'].sum()
        kpi_raw_2 = {
            "Total Ventas": v2, "Total Mt2": m2_2, "Total Tickets": t2, "Total Unidades": u2_total,
            "Ventas/Mt2": (v2 / m2_2) if m2_2 > 0 else 0,
            "Unidades/Ticket (UPT)": (u2_total / t2) if t2 > 0 else 0,
            "Ventas/Ticket (ATV)": (v2 / t2) if t2 > 0 else 0,
            "Artículo Prom. (ASP)": (v2 / u2_total) if u2_total > 0 else 0,
            #"Unidades/Mt2": (u2_total / m2_2) if m2_2 > 0 else 0
        }

        kpi_formats = {
            "Total Ventas": "${:,.0f}", "Total Unidades": "{:,.0f}", "Total Tickets": "{:,.0f}", "Total Mt2": "{:,.0f}",
            "Ventas/Mt2": "${:,.2f}", "Unidades/Ticket (UPT)": "{:,.2f}", "Ventas/Ticket (ATV)": "${:,.2f}",
            "Artículo Prom. (ASP)": "${:,.2f}", #"Unidades/Mt2": "{:,.2f}"
        }
        
        def generar_indicador_cambio(change_pct):
            if change_pct == float('inf'): return dbc.Row([dbc.Col(html.I(className="bi bi-rocket-takeoff-fill me-2"), width="auto"), dbc.Col(html.H6("Nuevo", className="mb-0"))], className="text-success", align="center")
            if change_pct > 0.1: return dbc.Row([dbc.Col(html.I(className="bi bi-arrow-up-circle-fill me-2"), width="auto"), dbc.Col(html.H6(f"+{change_pct:.1f}%", className="mb-0"))], className="text-success", align="center")
            elif change_pct < -0.1: return dbc.Row([dbc.Col(html.I(className="bi bi-arrow-down-circle-fill me-2"), width="auto"), dbc.Col(html.H6(f"{change_pct:.1f}%", className="mb-0"))], className="text-danger", align="center")
            else: return html.P("-", className="text-muted text-center fw-bold mb-0")

        # --- Lista completa de 9 KPIs a mostrar (comenté el último) ---
        kpi_defs = ["Total Ventas", "Total Mt2", "Total Tickets", "Total Unidades", "Ventas/Mt2", "Ventas/Ticket (ATV)", "Unidades/Ticket (UPT)", "Artículo Prom. (ASP)"]
        
        cards = []
        for kpi_name in kpi_defs:
            val1 = kpi_raw_1.get(kpi_name, 0)
            val2 = kpi_raw_2.get(kpi_name, 0)
            change = calc_pct_change(val2, val1)
            indicator_component = generar_indicador_cambio(change)
            
            card = dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.P(kpi_name, className="card-title font-weight-bold text-center small"),
                    html.Hr(className="my-2"),
                    dbc.Row([
                        dbc.Col(html.P("Sel 1:", className="text-primary small mb-1 font-weight-bold"), width="auto"),
                        dbc.Col(html.H6(kpi_formats.get(kpi_name, "{:,.2f}").format(val1), className="text-primary text-end")),
                    ], align="center"),
                    dbc.Row([
                        dbc.Col(html.P("Sel 2:", className="text-danger small mb-1 font-weight-bold"), width="auto"),
                        dbc.Col(html.H6(kpi_formats.get(kpi_name, "{:,.2f}").format(val2), className="text-danger text-end")),
                    ]),
                    html.Hr(className="my-1"),
                    indicator_component
                ])),
                width=6, sm=4, md=4, lg=3, xl=3, className="mb-3"
            )
            cards.append(card)
        
        num_cols_por_fila = 4
        kpi_rows = [dbc.Row(cards[i:i + num_cols_por_fila]) for i in range(0, len(cards), num_cols_por_fila)]
        return kpi_rows

    else: # Lógica para KPIs generales (acá están los básicos en retail)
        df_filtrado = filter_dataframe(df_global_completo, ub_gral, m_gral, sd_gral, ed_gral)
        if df_filtrado.empty: return [dbc.Col(dbc.Card(dbc.CardBody("Sin Datos")), md=12)]
        
        total_ventas = df_filtrado['VENTAS'].sum(); total_unidades = df_filtrado['UNIDADES'].sum(); total_tickets = df_filtrado['TICKETS'].sum()
        total_mt2 = df_filtrado.drop_duplicates(subset=['UBICACION', 'MARCA'])['Metros_Cuadrados'].sum()

        kpi_definitions = [
            {"label": "Total Ventas", "value": f"${total_ventas:,.0f}"},{"label": "Total Mt2", "value": f"{total_mt2:,.0f}"},
            {"label": "Total Tickets", "value": f"{total_tickets:,.0f}"},{"label": "Total Unidades", "value": f"{total_unidades:,.0f}"},
            {"label": "Ventas/Mt2", "value": f"${(total_ventas/total_mt2 if total_mt2 > 0 else 0):,.2f}"},
            {"label": "Unidades/Ticket (UPT)", "value": f"{(total_unidades/total_tickets if total_tickets > 0 else 0):,.2f}"},
            {"label": "Ventas/Ticket (ATV)", "value": f"${(total_ventas/total_tickets if total_tickets > 0 else 0):,.2f}"},
            {"label": "Artículo Prom. (ASP)", "value": f"${(total_ventas/total_unidades if total_unidades > 0 else 0):,.2f}"},
            #{"label": "Unidades/Mt2", "value": f"{(total_unidades/total_mt2 if total_mt2 > 0 else 0):,.2f}"}
        ]
        
        kpi_cards = [dbc.Col(dbc.Card(dbc.CardBody([html.P(kpi["label"], className="text-muted mb-0 small"), html.H4(kpi["value"], className="text-secondary")])), md=4, lg=3, className="mb-2") for kpi in kpi_definitions]
        
        num_cols_por_fila = 4
        kpi_rows = [dbc.Row(kpi_cards[i:i + num_cols_por_fila]) for i in range(0, len(kpi_cards), num_cols_por_fila)]
        return kpi_rows

        
# Callback para el mapa
@app.callback(
    Output('mapa-ventas', 'figure'),
    [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date')]
)
def update_map_chart(selected_ubicaciones, selected_marcas, start_date, end_date):
    if start_date is None: return dash.no_update
        
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    if df_filtrado.empty: 
        return create_empty_figure("Sin datos para el mapa")
    
    # --- Lógica de Conteo y Agregación ---
    
    # 1. Calcular totales para la selección completa
    total_ventas_seleccion = df_filtrado['VENTAS'].sum()
    total_tiendas_seleccion = len(df_filtrado.drop_duplicates(subset=['UBICACION', 'MARCA']))
    
    if total_ventas_seleccion == 0:
        return create_empty_figure("Las ventas totales son cero en esta selección")

    # 2. Contar tiendas y agregar ventas/unidades por CIUDAD
    stores_per_city = df_filtrado.drop_duplicates(subset=['CIUDAD', 'UBICACION', 'MARCA']).groupby('CIUDAD').size().reset_index(name='Numero_Tiendas')
    sales_units_per_city = df_filtrado.groupby('CIUDAD', as_index=False).agg(
        Total_Ventas=('VENTAS', 'sum'), 
        Total_Unidades=('UNIDADES', 'sum')
    )
    
    # 3. Unir los dataframes para tener toda la información por ciudad
    df_mapa_data = pd.merge(sales_units_per_city, stores_per_city, on='CIUDAD', how='left')
    df_mapa_data['Total_Unidades'] = df_mapa_data['Total_Unidades'].astype(int)
    
    # 4. Calcular la columna de porcentaje de ventas
    df_mapa_data['Porc_Ventas'] = (df_mapa_data['Total_Ventas'] / total_ventas_seleccion)

    # Unir con coordenadas
    city_coords_df = pd.DataFrame.from_dict(CITY_COORDS, orient='index')
    df_mapa_data['CIUDAD'] = df_mapa_data['CIUDAD'].str.strip().str.upper()
    df_mapa_data = pd.merge(df_mapa_data, city_coords_df, left_on='CIUDAD', right_index=True, how='left').dropna(subset=['lat', 'lon'])
    
    if df_mapa_data.empty: 
        return create_empty_figure("Ninguna de las ciudades filtradas tiene coordenadas definidas")
    
    fig = px.scatter_mapbox(
        df_mapa_data,
        lat="lat", lon="lon",
        size="Total_Ventas",
        color="Total_Unidades",
        hover_name="CIUDAD",
        hover_data={
            "Porc_Ventas": ":.2%",
            "Numero_Tiendas": ":, .0f", 
            "Total_Unidades": ":, .0f",
            "lat": False,
            "lon": False,
            "Total_Ventas": False
        },
        labels={'Numero_Tiendas': 'N° de Tiendas', 'Porc_Ventas': '% de Ventas', 'Total_Unidades': 'Total Unidades'},
        color_continuous_scale=px.colors.sequential.Bluered,
        size_max=50,
        zoom=5,
        mapbox_style="carto-positron",
        center={"lat": 9.5, "lon": -67.5}
    )

    
    
    texto_anotacion = f"Tamaño de burbuja: Total de Ventas<br>Total Tiendas en Selección: {total_tiendas_seleccion}"
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, 
        legend_title="Total Unidades",
        annotations=[
            go.layout.Annotation(
                text=texto_anotacion,
                align='left', showarrow=False,
                xref='paper', yref='paper',
                x=0.01, y=0.98,
                bgcolor="rgba(255,255,255,0.7)",
                font=dict(color=COLOR_TEXTO_OSCURO)
            )
        ]
    )
    return fig

# Callbacks para el drill-down del mapa
@app.callback(Output('memoria-ciudad-clickeada', 'data'), Input('mapa-ventas', 'clickData'), prevent_initial_call=True)
def store_clicked_city(clickData):
    if not clickData: return dash.no_update
    return clickData['points'][0]['hovertext']

@app.callback(Output('detalle-ciudad-container', 'children'), [Input('memoria-ciudad-clickeada', 'data')], [State('filtro-ubicacion', 'value'), State('filtro-marca', 'value'), State('filtro-fecha', 'start_date'), State('filtro-fecha', 'end_date')])
def update_city_detail_view(clicked_city, selected_ubicaciones, selected_marcas, start_date, end_date):
    if not clicked_city: return dbc.Alert("Haz clic en una ciudad en el mapa para ver el detalle de sus ubicaciones.", color="info", className="mt-3 text-center")
    
    df_filtrado_general = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    df_ciudad_filtrada = df_filtrado_general[df_filtrado_general['CIUDAD'] == clicked_city]
    if df_ciudad_filtrada.empty: return html.Div(f"No hay datos para '{clicked_city}' en la selección actual.")
    df_detalle_ubicacion = df_ciudad_filtrada.groupby('UBICACION', as_index=False).agg(Total_Ventas=('VENTAS', 'sum')).sort_values(by='Total_Ventas', ascending=False)
    
    fig_detalle = px.bar(df_detalle_ubicacion, x='UBICACION', y='Total_Ventas', text='Total_Ventas', title=f"Ventas por Ubicación en: {clicked_city}")
    fig_detalle.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_detalle.update_layout(xaxis_title=None, yaxis_title="Ventas Totales ($)", paper_bgcolor=COLOR_FONDO_GRAFICO, plot_bgcolor=COLOR_FONDO_GRAFICO, font_color=COLOR_TEXTO_OSCURO, yaxis=dict(gridcolor='#dee2e6'))
    return dbc.Card(dbc.CardBody(dcc.Graph(figure=fig_detalle)))

# Callbacks para los 3 gráficos dinámicos de la pestaña general
@app.callback(Output('grafico-ventas-dinamico', 'figure'), [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'), Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date'), Input('ventas-radio', 'value')])
def update_sales_dynamic_chart(selected_ubicaciones, selected_marcas, start_date, end_date, selected_metric):
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    metric_map = {'VENTAS': {'label':'Ventas Totales','value':'VENTAS','formatter':'$%{text:,.0f}'}, 'Ventas_por_MT2': {'label':'Ventas / Mt2','value':'Ventas_por_MT2','formatter':'$%{text:,.2f}'}, 'Relacion_Ventas_Canon': {'label':'Ventas / Canon Periodo','value':'Relacion_Ventas_Canon','formatter':'%{text:,.2f}x'}, 'ATV': {'label':'Ventas / Ticket (ATV)','value':'ATV','formatter':'$%{text:,.2f}'}, 'ASP': {'label':'Ventas / Unidad (ASP)','value':'ASP','formatter':'$%{text:,.2f}'}}
    return create_interactive_yoy_chart(df_filtrado, selected_marcas, metric_map[selected_metric])

@app.callback(Output('grafico-unidades-dinamico', 'figure'), [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'), Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date'), Input('unidades-radio', 'value')])
def update_units_dynamic_chart(selected_ubicaciones, selected_marcas, start_date, end_date, selected_metric):
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    metric_map = {'UNIDADES': {'label':'Unidades Totales','value':'UNIDADES','formatter':'%{text:,.0f}'}, 'UPT': {'label':'Unidades / Ticket (UPT)','value':'UPT','formatter':'%{text:,.2f}'}, 'Unidades_por_MT2': {'label':'Unidades / Mt2','value':'Unidades_por_MT2','formatter':'%{text:,.2f}'}, 'Unidades_por_Canon': {'label':'Unidades / Canon Periodo','value':'Unidades_por_Canon','formatter':'%{text:,.2f}'}}
    return create_interactive_yoy_chart(df_filtrado, selected_marcas, metric_map[selected_metric])

@app.callback(Output('grafico-tickets-dinamico', 'figure'), [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'), Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date'), Input('tickets-radio', 'value')])
def update_tickets_dynamic_chart(selected_ubicaciones, selected_marcas, start_date, end_date, selected_metric):
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    metric_map = {'TICKETS': {'label':'Tickets Totales','value':'TICKETS','formatter':'%{text:,.0f}'}, 'Tickets_por_MT2': {'label':'Tickets / Mt2','value':'Tickets_por_MT2','formatter':'%{text:,.2f}'}, 'Tickets_por_Canon': {'label':'Tickets / Canon Periodo','value':'Tickets_por_Canon','formatter':'%{text:,.2f}'}}
    return create_interactive_yoy_chart(df_filtrado, selected_marcas, metric_map[selected_metric])




# --- Función Auxiliar para crear el gráfico de segmentación ---

def create_segmentation_chart(df_agg, x_col, y_col, color_col, size_col, text_col, title, xaxis_title, yaxis_title):
    if df_agg.empty or df_agg.shape[0] < 2:
        return create_empty_figure("No hay suficientes datos para segmentar")
        
    median_x = df_agg[x_col].median()
    median_y = df_agg[y_col].median()
    
    # --- Construir una plantilla de hover explícita ---
    # Determinamos el formato para cada eje basándonos en si es monetario
    x_format = '$,.2f' if '$' in xaxis_title else ',.2f'
    y_format = '$,.2f' if '$' in yaxis_title else ',.2f'
    size_format = '$,.0f' # Asumimos que el tamaño siempre son ventas totales

    # Creamos la plantilla de texto
    hovertemplate = (
        f"<b>%{{hovertext}}</b><br><br>"
        f"{xaxis_title}: %{{x:{x_format}}}<br>"
        f"{yaxis_title}: %{{y:{y_format}}}<br>"
        f"Ventas Totales: %{{customdata[0]:{size_format}}}"
        "<extra></extra>" # Oculta información extra de la traza
    )
    
    fig = px.scatter(
        df_agg, x=x_col, y=y_col, 
        color=color_col, 
        size=size_col, 
        hover_name=text_col, 
        text=text_col, 
        color_discrete_sequence=PALETA_COLORES,
        custom_data=[size_col] # Pase la columna del tamaño para usarla en el hover
    )
    
    # --- CAMBIO 2: Aplicar la plantilla de hover ---
    fig.update_traces(
        textposition='top center', 
        textfont=dict(size=9, color=COLOR_TEXTO_OSCURO),
        hovertemplate=hovertemplate # Aplicamos la nueva plantilla
    )
    
    fig.update_layout(
        title={'text': title, 'x': 0.5},
        paper_bgcolor=COLOR_FONDO_GRAFICO, 
        plot_bgcolor=COLOR_FONDO_GRAFICO, 
        font=dict(family=STYLE_FONT_FAMILY, color=COLOR_TEXTO_OSCURO), 
        xaxis_title=xaxis_title, 
        yaxis_title=yaxis_title, 
        legend_title_text='Segmento',
        xaxis=dict(gridcolor='#dee2e6', tickformat=x_format), 
        yaxis=dict(gridcolor='#dee2e6', tickformat=y_format)
    )
    
    fig.add_vline(x=median_x, line_width=1, line_dash="dash", line_color=COLOR_PRIMARIO_AZUL)
    fig.add_hline(y=median_y, line_width=1, line_dash="dash", line_color=COLOR_PRIMARIO_AZUL)
    
    # Formato para las anotaciones de las medianas
    median_y_text = f"Mediana Y: ${median_y:,.2f}" if '$' in yaxis_title else f"Mediana Y: {median_y:,.2f}"
    fig.add_annotation(y=median_y, x=df_agg[x_col].max(), text=median_y_text, showarrow=False, xshift=10, xanchor="left", font=dict(color=COLOR_PRIMARIO_AZUL, size=10))

    median_x_text = f"Mediana X: ${median_x:,.2f}" if '$' in xaxis_title else f"Mediana X: {median_x:.2f}"
    fig.add_annotation(x=median_x, y=df_agg[y_col].max(), text=median_x_text, showarrow=False, yshift=10, yanchor="bottom", font=dict(color=COLOR_PRIMARIO_AZUL, size=10))
    
    return fig

# --- Callbacks para la Pestaña de Segmentación ---
@app.callback(
    Output('grafico-segmentacion-mt2', 'figure'),
    [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date')]
)
def update_mt2_scatter(selected_ubicaciones, selected_marcas, start_date, end_date):
    if start_date is None: return dash.no_update # No actualizar si este gráfico no está visible
    
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    grouping_col, title_entity = ('UBICACION', f"para: {selected_marcas[0]}") if selected_marcas and len(selected_marcas) == 1 else ('MARCA', "(Global)")
    
    df_agg = df_filtrado.groupby(grouping_col, as_index=False).agg(
        Total_Ventas=('VENTAS', 'sum'), Total_Unidades=('UNIDADES', 'sum'), 
        Metros_Cuadrados=('Metros_Cuadrados', 'sum')
    )
    df_agg.dropna(subset=['Metros_Cuadrados'], inplace=True); df_agg = df_agg[df_agg['Metros_Cuadrados'] > 0]
    if df_agg.empty or df_agg.shape[0] < 2: return create_empty_figure("No hay suficientes datos para segmentar")

    df_agg['Ventas_por_MT2'] = df_agg['Total_Ventas'] / df_agg['Metros_Cuadrados']
    df_agg['Unidades_por_MT2'] = df_agg['Total_Unidades'] / df_agg['Metros_Cuadrados']
    df_agg.replace([np.inf, -np.inf], np.nan, inplace=True); df_agg.dropna(subset=['Ventas_por_MT2', 'Unidades_por_MT2'], inplace=True)
    if df_agg.empty or df_agg.shape[0] < 2: return create_empty_figure("Datos insuficientes")

    median_ventas_mt2 = df_agg['Ventas_por_MT2'].median(); median_unidades_mt2 = df_agg['Unidades_por_MT2'].median()
    def definir_segmento_mt2(row):
        if row['Ventas_por_MT2'] >= median_ventas_mt2 and row['Unidades_por_MT2'] >= median_unidades_mt2: return 'Líder Productividad'
        if row['Ventas_por_MT2'] >= median_ventas_mt2 and row['Unidades_por_MT2'] < median_unidades_mt2: return 'Eficiente en Valor'
        if row['Ventas_por_MT2'] < median_ventas_mt2 and row['Unidades_por_MT2'] >= median_unidades_mt2: return 'Movilizador de Volumen'
        return ' Desafío de Productividad'
    df_agg['Segmento_Eficiencia'] = df_agg.apply(definir_segmento_mt2, axis=1)
    
    return create_segmentation_chart(df_agg, 'Unidades_por_MT2', 'Ventas_por_MT2', 'Segmento_Eficiencia', 'Total_Ventas', grouping_col, 
                                     f"Segmentación por Eficiencia de M² de {grouping_col.capitalize()}s {title_entity}", 'Unidades por Metro Cuadrado', 'Ventas por Metro Cuadrado ($)')

@app.callback(
    Output('grafico-segmentacion-canon', 'figure'),
    [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date')]
)
def update_canon_scatter(selected_ubicaciones, selected_marcas, start_date, end_date):
    if start_date is None: return dash.no_update
    
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date).dropna(subset=['Canon_Fijo'])
    grouping_col, title_entity = ('UBICACION', f"para: {selected_marcas[0]}") if selected_marcas and len(selected_marcas) == 1 else ('MARCA', "(Global)")
    
    df_agg = df_filtrado.groupby(grouping_col, as_index=False).agg(
        Total_Ventas=('VENTAS', 'sum'), Total_Tickets=('TICKETS', 'sum'), Canon_Fijo=('Canon_Fijo', 'sum')
    )
    df_agg = df_agg[df_agg['Canon_Fijo'] > 0]
    if df_agg.empty or df_agg.shape[0] < 2: return create_empty_figure("No hay datos de Canon Fijo para segmentar")

    df_agg['Ventas_por_Canon'] = df_agg['Total_Ventas'] / df_agg['Canon_Fijo']
    df_agg['Tickets_por_Canon'] = df_agg['Total_Tickets'] / df_agg['Canon_Fijo']
    df_agg.replace([np.inf, -np.inf], np.nan, inplace=True); df_agg.dropna(subset=['Ventas_por_Canon', 'Tickets_por_Canon'], inplace=True)
    if df_agg.empty or df_agg.shape[0] < 2: return create_empty_figure("Datos insuficientes")

    median_ventas_canon = df_agg['Ventas_por_Canon'].median(); median_tickets_canon = df_agg['Tickets_por_Canon'].median()
    
    def definir_segmento_canon(row):
        if row['Ventas_por_Canon'] >= median_ventas_canon and row['Tickets_por_Canon'] >= median_tickets_canon: return 'Líder en Rentabilidad'
        if row['Ventas_por_Canon'] >= median_ventas_canon and row['Tickets_por_Canon'] < median_tickets_canon: return 'Rentable (Bajo Tráfico)'
        if row['Ventas_por_Canon'] < median_ventas_canon and row['Tickets_por_Canon'] >= median_tickets_canon: return 'Atrae Tráfico (Baja Rent.)'
        return 'Desafío de Costos'
    df_agg['Segmento_Eficiencia'] = df_agg.apply(definir_segmento_canon, axis=1)
    
    return create_segmentation_chart(df_agg, 'Tickets_por_Canon', 'Ventas_por_Canon', 'Segmento_Eficiencia', 'Total_Ventas', grouping_col,
                                     f"Segmentación por Eficiencia de Canon de {grouping_col.capitalize()}s {title_entity}", 'Tickets por $ de Canon', 'Ventas por $ de Canon')


# --- ME EQUIVOQUE Y ESTOS CALLBACKS ESTAN DESORDENADOS ES DECIR NO ESTAN ESCRITOS POR ORDEN DE APARICION PERO FUNCIONA PORQUE EL ORDEN ESTA EN EL LAYOUT PERO PARA QUIEN LEA... NO ESTAN POR ORDEN DE APARICIÓN---

# --- Función Auxiliar para los Gráficos Comparativos (CON ORDENAMIENTO) ---
def create_comparative_chart(df_filtrado1, df_filtrado2, metric_details):
    value_col = metric_details['value']
    
    if df_filtrado1.empty or df_filtrado2.empty:
        return create_empty_figure("Una o ambas selecciones no tienen datos.")
    
    # La comparación siempre se hará por MARCA
    grouping_col = 'MARCA'
    
    # Procesar Selección 1
    df_agg1 = df_filtrado1.groupby(grouping_col, as_index=False).agg(Total_Ventas=('VENTAS', 'sum'), Total_Tickets=('TICKETS', 'sum'), Total_Unidades=('UNIDADES', 'sum'), Metros_Cuadrados=('Metros_Cuadrados', 'sum'), Canon_Fijo=('Canon_Fijo', 'sum'))
    df_agg1['Comparación'] = 'Selección 1'

    # Procesar Selección 2
    df_agg2 = df_filtrado2.groupby(grouping_col, as_index=False).agg(Total_Ventas=('VENTAS', 'sum'), Total_Tickets=('TICKETS', 'sum'), Total_Unidades=('UNIDADES', 'sum'), Metros_Cuadrados=('Metros_Cuadrados', 'sum'), Canon_Fijo=('Canon_Fijo', 'sum'))
    df_agg2['Comparación'] = 'Selección 2'

    df_comparativo = pd.concat([df_agg1, df_agg2], ignore_index=True)
    df_comparativo.replace(0, np.nan, inplace=True)

    # Calcular dinámicamente la métrica
    y_col_to_plot = value_col
    with np.errstate(divide='ignore', invalid='ignore'):
        if y_col_to_plot == 'VENTAS': df_comparativo[y_col_to_plot] = df_comparativo['Total_Ventas']
        elif y_col_to_plot == 'UNIDADES': df_comparativo[y_col_to_plot] = df_comparativo['Total_Unidades']
        elif y_col_to_plot == 'TICKETS': df_comparativo[y_col_to_plot] = df_comparativo['Total_Tickets']
        elif y_col_to_plot == 'Ventas_por_MT2': df_comparativo[y_col_to_plot] = df_comparativo['Total_Ventas'] / df_comparativo['Metros_Cuadrados']
        elif y_col_to_plot == 'Relacion_Ventas_Canon': df_comparativo[y_col_to_plot] = df_comparativo['Total_Ventas'] / df_comparativo['Canon_Fijo']
        elif y_col_to_plot == 'ATV': df_comparativo[y_col_to_plot] = df_comparativo['Total_Ventas'] / df_comparativo['Total_Tickets']
        elif y_col_to_plot == 'ASP': df_comparativo[y_col_to_plot] = df_comparativo['Total_Ventas'] / df_comparativo['Total_Unidades']
        elif y_col_to_plot == 'UPT': df_comparativo[y_col_to_plot] = df_comparativo['Total_Unidades'] / df_comparativo['Total_Tickets']
        elif y_col_to_plot == 'Unidades_por_MT2': df_comparativo[y_col_to_plot] = df_comparativo['Total_Unidades'] / df_comparativo['Metros_Cuadrados']
        elif y_col_to_plot == 'Unidades_por_Canon': df_comparativo[y_col_to_plot] = df_comparativo['Total_Unidades'] / df_comparativo['Canon_Fijo']
        elif y_col_to_plot == 'Tickets_por_MT2': df_comparativo[y_col_to_plot] = df_comparativo['Total_Tickets'] / df_comparativo['Metros_Cuadrados']
        elif y_col_to_plot == 'Tickets_por_Canon': df_comparativo[y_col_to_plot] = df_comparativo['Total_Tickets'] / df_comparativo['Canon_Fijo']

    df_comparativo[y_col_to_plot] = df_comparativo[y_col_to_plot].round(2)
    df_comparativo.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_comparativo.dropna(subset=[y_col_to_plot], inplace=True)

    if df_comparativo.empty:
        return create_empty_figure("No hay datos para esta métrica con las selecciones actuales.")

    
    # 1. Calcular el valor total (suma de ambas selecciones) para ordenar
    sorting_order_df = df_comparativo.groupby(grouping_col)[y_col_to_plot].sum().reset_index()
    # 2. Crear la lista ordenada
    sorted_categories = sorting_order_df.sort_values(by=y_col_to_plot, ascending=False)[grouping_col].tolist()
    # ------------------------------------

    fig = px.bar(
        df_comparativo, x=grouping_col, y=y_col_to_plot, color='Comparación',
        barmode='group', text=y_col_to_plot,
        #title=f"Comparativa de {metric_details['label']}",
        color_discrete_map={'Selección 1': COLOR_PRIMARIO_AZUL, 'Selección 2': '#DC3545'},
        category_orders={grouping_col: sorted_categories} # <-- 3. APLICAR EL ORDEN
    )
    
    hover_template = (f"<b>Marca:</b> %{{x}}<br>"
                      "<b>%{fullData.name}</b><br>"
                      f"<b>{metric_details['label']}:</b> {metric_details['formatter'].replace('text', 'y')}"
                      "<extra></extra>")

    fig.update_traces(
        texttemplate=metric_details['formatter'], 
        textposition='outside',
        hovertemplate=hover_template
    )
    
    y_axis_prefix = '$' if '$' in metric_details['formatter'] else ''
    fig.update_layout(
        paper_bgcolor=COLOR_FONDO_GRAFICO, plot_bgcolor=COLOR_FONDO_GRAFICO, font_color=COLOR_TEXTO_OSCURO,
        xaxis_title="Marca", yaxis_title=metric_details['label'], legend_title_text='Comparación',
        yaxis=dict(gridcolor='#dee2e6', tickprefix=y_axis_prefix, tickformat=",.2f")
    )
    return fig


# --- Función Auxiliar para crear los gráficos de barras YoY (CON ORDENAMIENTO) ---
def create_interactive_yoy_chart(df_filtrado, selected_marcas, metric_details):
    value_col = metric_details['value']
    
    if df_filtrado.empty: return create_empty_figure("No hay datos para esta selección")
    if value_col in ['Relacion_Ventas_Canon', 'Unidades_por_Canon', 'Tickets_por_Canon'] and 'Canon_Fijo' not in df_filtrado.columns:
        return create_empty_figure("Datos de Canon Fijo no disponibles")
    
    grouping_col, title_entity = ('UBICACION', f"para: {selected_marcas[0]}") if selected_marcas and len(selected_marcas) == 1 else ('MARCA', "(Global)")
    
    df_agg = df_filtrado.groupby([grouping_col, 'AÑO'], as_index=False).agg(
        Total_Ventas=('VENTAS', 'sum'), Total_Tickets=('TICKETS', 'sum'),
        Total_Unidades=('UNIDADES', 'sum'), Metros_Cuadrados=('Metros_Cuadrados', 'sum'),
        Canon_Fijo=('Canon_Fijo', 'first')
    )
    df_agg.replace(0, np.nan, inplace=True)
    
    y_col_to_plot = value_col
    with np.errstate(divide='ignore', invalid='ignore'):
        if y_col_to_plot == 'VENTAS': df_agg[y_col_to_plot] = df_agg['Total_Ventas']
        elif y_col_to_plot == 'UNIDADES': df_agg[y_col_to_plot] = df_agg['Total_Unidades']
        elif y_col_to_plot == 'TICKETS': df_agg[y_col_to_plot] = df_agg['Total_Tickets']
        elif y_col_to_plot == 'Ventas_por_MT2': df_agg[y_col_to_plot] = df_agg['Total_Ventas'] / df_agg['Metros_Cuadrados']
        elif y_col_to_plot == 'Relacion_Ventas_Canon':
            num_months = df_filtrado['FECHA_DATETIME'].dt.to_period('M').nunique()
            df_agg['Canon_Total_Periodo'] = df_agg['Canon_Fijo'] * num_months
            df_agg[y_col_to_plot] = df_agg['Total_Ventas'] / df_agg['Canon_Total_Periodo']
        elif y_col_to_plot == 'ATV': df_agg[y_col_to_plot] = df_agg['Total_Ventas'] / df_agg['Total_Tickets']
        elif y_col_to_plot == 'ASP': df_agg[y_col_to_plot] = df_agg['Total_Ventas'] / df_agg['Total_Unidades']
        elif y_col_to_plot == 'UPT': df_agg[y_col_to_plot] = df_agg['Total_Unidades'] / df_agg['Total_Tickets']
        elif y_col_to_plot == 'Unidades_por_MT2': df_agg[y_col_to_plot] = df_agg['Total_Unidades'] / df_agg['Metros_Cuadrados']
        elif y_col_to_plot == 'Tickets_por_MT2': df_agg[y_col_to_plot] = df_agg['Total_Tickets'] / df_agg['Metros_Cuadrados']
        elif y_col_to_plot == 'Unidades_por_Canon':
            num_months = df_filtrado['FECHA_DATETIME'].dt.to_period('M').nunique()
            df_agg['Canon_Total_Periodo'] = df_agg['Canon_Fijo'] * num_months
            df_agg[y_col_to_plot] = df_agg['Total_Unidades'] / df_agg['Canon_Total_Periodo']
        elif y_col_to_plot == 'Tickets_por_Canon':
            num_months = df_filtrado['FECHA_DATETIME'].dt.to_period('M').nunique()
            df_agg['Canon_Total_Periodo'] = df_agg['Canon_Fijo'] * num_months
            df_agg[y_col_to_plot] = df_agg['Total_Tickets'] / df_agg['Canon_Total_Periodo']

    df_agg[y_col_to_plot] = df_agg[y_col_to_plot].round(2)
    df_agg.replace([np.inf, -np.inf], np.nan, inplace=True); df_agg.dropna(subset=[y_col_to_plot], inplace=True)
    if df_agg.empty: return create_empty_figure("No hay datos para esta métrica")
    df_agg['AÑO'] = df_agg['AÑO'].astype(str)


    # 1. Calcular el valor total de la métrica por entidad para poder ordenar
    sorting_order_df = df_agg.groupby(grouping_col)[y_col_to_plot].sum().reset_index()
    # 2. Crear la lista ordenada de categorías (de mayor a menor)
    sorted_categories = sorting_order_df.sort_values(by=y_col_to_plot, ascending=False)[grouping_col].tolist()
    # ------------------------------------

    fig = px.bar(
        df_agg, x=grouping_col, y=y_col_to_plot, color='AÑO', 
        barmode='group', text=y_col_to_plot,
        #title=f'Comparativa YoY de {metric_details["label"]} por {grouping_col.capitalize()}',
        color_discrete_sequence=PALETA_COLORES,
        category_orders={grouping_col: sorted_categories} # ORDEN
    )
    
    hover_template = (f"<b>{grouping_col}:</b> %{{x}}<br>"
                      "<b>Año:</b> %{fullData.name}<br>"
                      f"<b>{metric_details['label']}:</b> {metric_details['formatter'].replace('text', 'y')}"
                      "<extra></extra>")
    
    fig.update_traces(
        texttemplate=metric_details['formatter'], 
        textposition="outside", 
        textangle=0, 
        textfont=dict(size=12, family="Arial"),
        hovertemplate=hover_template
    )
    
    y_axis_prefix = '$' if '$' in metric_details['formatter'] else ''
    fig.update_layout(
        paper_bgcolor=COLOR_FONDO_GRAFICO, plot_bgcolor=COLOR_FONDO_GRAFICO, font_color=COLOR_TEXTO_OSCURO,
        xaxis_title=None, 
        yaxis_title=metric_details['label'], 
        legend_title_text='Año',
        yaxis=dict(gridcolor='#dee2e6', tickprefix=y_axis_prefix, tickformat=",.2f"),
        xaxis=dict(gridcolor='#e9ecef'),
        xaxis_tickangle=-45
    )
    return fig
    
# --- Callback para la Descarga del README ---
@app.callback(
    Output("descarga-readme", "data"),
    Input("btn-descargar-readme", "n_clicks"),
    prevent_initial_call=True,
)
def func_descargar_readme(n_clicks):
    return dcc.send_string(README_TEXT, "README.md")
    
# --- Callbacks para la Pestaña de Análisis Comparativo ---
@app.callback(Output('grafico-ventas-comparativo', 'figure'),
              [Input('filtro-ubicacion-1', 'value'), Input('filtro-marca-1', 'value'), Input('filtro-fecha-1', 'start_date'), Input('filtro-fecha-1', 'end_date'),
               Input('filtro-ubicacion-2', 'value'), Input('filtro-marca-2', 'value'), Input('filtro-fecha-2', 'start_date'), Input('filtro-fecha-2', 'end_date'),
               Input('ventas-radio-comp', 'value')])
def update_comparative_sales_chart(u1, m1, s1, e1, u2, m2, s2, e2, metric):
    if not all([s1, e1, s2, e2]): return dash.no_update
    df1 = filter_dataframe(df_global_completo, u1, m1, s1, e1)
    df2 = filter_dataframe(df_global_completo, u2, m2, s2, e2)
    metric_map = {'VENTAS': {'label':'Ventas Totales','value':'VENTAS','formatter':'$%{text:,.0f}'}, 'Ventas_por_MT2': {'label':'Ventas / Mt2','value':'Ventas_por_MT2','formatter':'$%{text:,.2f}'}, 'Relacion_Ventas_Canon': {'label':'Ventas / Canon Fijo','value':'Relacion_Ventas_Canon','formatter':'%{text:,.2f}x'}, 'ATV': {'label':'Ventas / Ticket (ATV)','value':'ATV','formatter':'$%{text:,.2f}'}, 'ASP': {'label':'Ventas / Unidad (ASP)','value':'ASP','formatter':'$%{text:,.2f}'}}
    return create_comparative_chart(df1, df2, metric_map[metric])

@app.callback(Output('grafico-unidades-comparativo', 'figure'),
              [Input('filtro-ubicacion-1', 'value'), Input('filtro-marca-1', 'value'), Input('filtro-fecha-1', 'start_date'), Input('filtro-fecha-1', 'end_date'),
               Input('filtro-ubicacion-2', 'value'), Input('filtro-marca-2', 'value'), Input('filtro-fecha-2', 'start_date'), Input('filtro-fecha-2', 'end_date'),
               Input('unidades-radio-comp', 'value')])
def update_comparative_units_chart(u1, m1, s1, e1, u2, m2, s2, e2, metric):
    if not all([s1, e1, s2, e2]): return dash.no_update
    df1 = filter_dataframe(df_global_completo, u1, m1, s1, e1)
    df2 = filter_dataframe(df_global_completo, u2, m2, s2, e2)
    metric_map = {'UNIDADES': {'label':'Unidades Totales','value':'UNIDADES','formatter':'%{text:,.0f}'}, 'UPT': {'label':'Unidades / Ticket (UPT)','value':'UPT','formatter':'%{text:,.2f}'}, 'Unidades_por_MT2': {'label':'Unidades / Mt2','value':'Unidades_por_MT2','formatter':'%{text:,.2f}'}, 'Unidades_por_Canon': {'label':'Unidades / Canon Fijo','value':'Unidades_por_Canon','formatter':'%{text:,.2f}'}}
    return create_comparative_chart(df1, df2, metric_map[metric])

@app.callback(Output('grafico-tickets-comparativo', 'figure'),
              [Input('filtro-ubicacion-1', 'value'), Input('filtro-marca-1', 'value'), Input('filtro-fecha-1', 'start_date'), Input('filtro-fecha-1', 'end_date'),
               Input('filtro-ubicacion-2', 'value'), Input('filtro-marca-2', 'value'), Input('filtro-fecha-2', 'start_date'), Input('filtro-fecha-2', 'end_date'),
               Input('tickets-radio-comp', 'value')])
def update_comparative_tickets_chart(u1, m1, s1, e1, u2, m2, s2, e2, metric):
    if not all([s1, e1, s2, e2]): return dash.no_update
    df1 = filter_dataframe(df_global_completo, u1, m1, s1, e1)
    df2 = filter_dataframe(df_global_completo, u2, m2, s2, e2)
    metric_map = {'TICKETS': {'label':'Tickets Totales','value':'TICKETS','formatter':'%{text:,.0f}'}, 'Tickets_por_MT2': {'label':'Tickets / Mt2','value':'Tickets_por_MT2','formatter':'%{text:,.2f}'}, 'Tickets_por_Canon': {'label':'Tickets / Canon Fijo','value':'Tickets_por_Canon','formatter':'%{text:,.2f}'}}
    return create_comparative_chart(df1, df2, metric_map[metric])
    

# --- Callback para el gráfico exploratorio---
@app.callback(
    Output('grafico-exploratorio', 'figure'),
    [Input('filtro-ubicacion', 'value'), Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'), Input('filtro-fecha', 'end_date'),
     Input('exploratorio-eje-x', 'value'),
     Input('exploratorio-eje-y', 'value')]
)
def update_exploratory_chart(selected_ubicaciones, selected_marcas, start_date, end_date, eje_x, eje_y):
    if not all([start_date, end_date, eje_x, eje_y]):
        return create_empty_figure("Selecciona variables para los ejes X e Y")

    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    if df_filtrado.empty:
        return create_empty_figure("Sin datos para la selección de filtros")

    # Agregar MARCA para tener puntos definidos en el gráfico
    df_agg = df_filtrado.groupby('MARCA', as_index=False).agg(
        VENTAS=('VENTAS', 'sum'),
        UNIDADES=('UNIDADES', 'sum'),
        TICKETS=('TICKETS', 'sum'),
        Metros_Cuadrados=('Metros_Cuadrados', 'sum'), # Usar sum para la huella total
        Canon_Fijo=('Canon_Fijo', 'sum')
    )
    df_agg.replace(0, np.nan, inplace=True)

    
    # Calcular TODAS las métricas derivadas que podrían ser seleccionadas
    with np.errstate(divide='ignore', invalid='ignore'):
        df_agg['Ventas_por_MT2'] = df_agg['VENTAS'] / df_agg['Metros_Cuadrados']
        df_agg['Unidades_por_MT2'] = df_agg['UNIDADES'] / df_agg['Metros_Cuadrados']
        df_agg['Tickets_por_MT2'] = df_agg['TICKETS'] / df_agg['Metros_Cuadrados']
        df_agg['Ventas_por_Canon'] = df_agg['VENTAS'] / df_agg['Canon_Fijo']
        df_agg['Unidades_por_Canon'] = df_agg['UNIDADES'] / df_agg['Canon_Fijo']
        df_agg['Tickets_por_Canon'] = df_agg['TICKETS'] / df_agg['Canon_Fijo']
        df_agg['ATV'] = df_agg['VENTAS'] / df_agg['TICKETS'] 
        df_agg['UPT'] = df_agg['UNIDADES'] / df_agg['TICKETS'] 
        df_agg['ASP'] = df_agg['VENTAS'] / df_agg['UNIDADES'] # Precio de Venta Promedio
    
    df_agg.dropna(subset=[eje_x, eje_y], inplace=True)
    if df_agg.empty:
        return create_empty_figure("Datos insuficientes para las variables seleccionadas")

    fig = px.scatter(
        df_agg, x=eje_x, y=eje_y,
        color='MARCA',
        size='VENTAS', 
        hover_name='MARCA',
        text='MARCA',
        custom_data=['VENTAS', 'UNIDADES', 'TICKETS']
    )
    
    # --- HOVERTEMPLATE ---
    fig.update_traces(
        textposition='top center', 
        textfont_size=10,
        hovertemplate=(
            f"<b>%{{hovertext}}</b><br><br>"
            f"{eje_x}: %{{x:,.2f}}<br>"
            f"{eje_y}: %{{y:,.2f}}<br>"
            "Ventas Totales: %{customdata[0]:$,.0f}<br>" 
            "Unidades Totales: %{customdata[1]:,.0f}<br>"
            "Tickets Totales: %{customdata[2]:,.0f}<br>"
            "<extra></extra>" 
        )
    )
    
    fig.update_layout(
        title=f'Análisis de Dispersión: {eje_y} vs. {eje_x}',
        paper_bgcolor=COLOR_FONDO_GRAFICO, plot_bgcolor=COLOR_FONDO_GRAFICO,
        font_color=COLOR_TEXTO_OSCURO,
        xaxis=dict(title=eje_x, gridcolor='#e9ecef'),
        yaxis=dict(title=eje_y, gridcolor='#e9ecef')
    )
    return fig

# --- Callback para el nuevo gráfico de KPIs en la pestaña general ---
@app.callback(
    Output('grafico-kpi-dinamico', 'figure'),
    [Input('filtro-ubicacion', 'value'),
     Input('filtro-marca', 'value'),
     Input('filtro-fecha', 'start_date'),
     Input('filtro-fecha', 'end_date'),
     Input('kpi-transaccion-radio', 'value')]
)
def update_kpi_dynamic_chart(selected_ubicaciones, selected_marcas, start_date, end_date, selected_metric):
    if start_date is None: return dash.no_update # Evita errores si el callback se dispara antes de tiempo
    df_filtrado = filter_dataframe(df_global_completo, selected_ubicaciones, selected_marcas, start_date, end_date)
    
    metric_map = {
        'UPT': {'label':'Unidades / Ticket (UPT)','value':'UPT','formatter':'%{text:,.2f}'},
        'ATV': {'label':'Ventas / Ticket (ATV)','value':'ATV','formatter':'$%{text:,.2f}'},
        'ASP': {'label':'Ventas / Unidad (ASP)','value':'ASP','formatter':'$%{text:,.2f}'}
    }
    
    return create_interactive_yoy_chart(df_filtrado, selected_marcas, metric_map[selected_metric])


# --- Callback para el nuevo gráfico de KPIs en la pestaña comparativa ---
@app.callback(
    Output('grafico-kpi-comparativo', 'figure'),
    [Input('filtro-ubicacion-1', 'value'), Input('filtro-marca-1', 'value'), Input('filtro-fecha-1', 'start_date'), Input('filtro-fecha-1', 'end_date'),
     Input('filtro-ubicacion-2', 'value'), Input('filtro-marca-2', 'value'), Input('filtro-fecha-2', 'start_date'), Input('filtro-fecha-2', 'end_date'),
     Input('kpi-transaccion-radio-comp', 'value')]
)
def update_comparative_kpi_chart(u1, m1, s1, e1, u2, m2, s2, e2, metric):
    if not all([s1, e1, s2, e2]): return dash.no_update
    df1 = filter_dataframe(df_global_completo, u1, m1, s1, e1)
    df2 = filter_dataframe(df_global_completo, u2, m2, s2, e2)

    metric_map = {
        'UPT': {'label':'Unidades / Ticket (UPT)','value':'UPT','formatter':'%{text:,.2f}'},
        'ATV': {'label':'Ventas / Ticket (ATV)','value':'ATV','formatter':'$%{text:,.2f}'},
        'ASP': {'label':'Ventas / Unidad (ASP)','value':'ASP','formatter':'$%{text:,.2f}'}
    }
    
    return create_comparative_chart(df1, df2, metric_map[metric])

# ---  Ejecutar la App ---
if __name__ == '__main__':
    # Primero, verificar si los datos se cargaron correctamente
    if df_global_completo is None or df_global_completo.empty:
        # Si no, imprimir un error y no iniciar el servidor
        print("ERROR CRÍTICO: La carga de datos falló. La aplicación no puede iniciar.")
        print("Por favor, revisa los mensajes de error anteriores para identificar el problema en los archivos Excel.")
    else:
        # Si todo está bien, iniciar el servidor
        print("\nDatos cargados correctamente.")
        # Render usará la variable de entorno PORT, si no, usa el puerto 8050 para desarrollo local
        port = int(os.environ.get("PORT", 8050))
        print(f"Iniciando servidor Dash en http://0.0.0.0:{port}/")
        # Usamos host='0.0.0.0' para que sea accesible en redes y para el despliegue
        app.run(host='0.0.0.0', port=port, debug=True)
