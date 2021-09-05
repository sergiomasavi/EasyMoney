print(5*'-' + 'Easy Money - Autoservicio BI '+'-')
# Librerías
print('Importing libs...')
import pandas as pd
import numpy as np
from datetime import datetime
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# Configuración librerías
print('Setting libs config...')
pio.templates.default = "simple_white"

# Importar paquetes
print('Importing pkgs...')
from EasyMoney import analisis as anl
from EasyMoney import visualization as vs

# Parámetros de la página web
COLOR_HEADER = "rgb(255, 87, 51)" # color del header
graphs = [
    dcc.Graph(id="nivel-permanencia-bar-chart"),
    dcc.Graph(id="donut-chart")]

# 1. Lectura de los datos
df_bar = anl.get_nivel_permanencia(filename = 'data/nivel_permanencia.csv')

df = pd.read_csv("avocado.csv", index_col=0).reset_index(drop=True)
df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
df.sort_values("Date", inplace=True)
regions = df.region.unique()
avocado_types = df.type.unique()
min_date = df.Date.min()
max_date = df.Date.max()

# Lista con los títulos y los filtros de la barra de la izquierda.
MENU = [
    html.P("Avocado Type", className="title-filter"),
    dcc.RadioItems(
        id="type-selector",
        options=[{"label": t.title(), "value": t} for t in avocado_types],
        value=avocado_types[0],
    ),
    html.P("Region", className="title-filter"),
    dcc.Dropdown(
        id="region-selector",
        options=[{"label": r, "value": r} for r in regions],
        value=regions[:3],
        multi=True,
        clearable=False,
    ),
    html.P("Dates", className="title-filter"),
    dcc.DatePickerRange(
        id="date-selector",
        start_date=min_date,
        min_date_allowed=min_date,
        end_date=max_date,
        max_date_allowed=max_date,
        initial_visible_month=min_date,
    ),
]

# 2. Estructurar aplicación
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            id="header",
            children=[html.H1("Easy Money - Autoservice BI", id="title")],
            style={"background": COLOR_HEADER},
        ),
        html.Div(
            children=[
                html.Div(
                    id="menu",
                    children=MENU,
                ),
                html.Div(
                    id="graphs",
                    children=graphs,
                ),
            ],
            id="content",
        ),
    ],
    id="wrapper",
)


# Callback de actualización
@app.callback(
    [
        Output("nivel-permanencia-bar-chart", "figure"),
        Output("donut-chart", "figure")
    ],

    [
        Input("type-selector", "value"),
        Input("region-selector", "value"),
        Input("date-selector", "start_date"),
        Input("date-selector", "end_date"),
    ],
)
def update_graphs(avocado_type, selected_regions, start_date, end_date):

    filter_region = df.region.isin(selected_regions)
    filter_type = df.type == avocado_type
    filter_date = df.Date.between(start_date, end_date)

    # Filter data
    df_line = df[(filter_region) & (filter_type) & (filter_date)]
    df_donut = df[(filter_region) & (filter_type) & (filter_date)][
        ["region", "Total Volume"]
    ]
    df_donut = df_donut.groupby("region").sum().reset_index()

    # Create figures
    fig_donut = px.pie(
        data_frame=df_donut,
        names="region",
        values="Total Volume",
        hole=0.5,
        title="Total Volume per Region",
    )

    # Obtener BarChar del nivel de permanencia
    fig_bar_np = vs.bar_nivel_permanencia(df_bar=df_bar, plot=False)

    return fig_bar_np, fig_donut


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
