# Librerías
print('Importing libs...')
import dash
import dash_bootstrap_components as dbc
from dash import html

# Paquetes
print('Importing pkgs...')
from app.styles import get_styles
from app.forms import get_sidebar, get_client_content
from EasyMoney import analisis as anl

# 1. Obtener componentes de la página.
sidebar_style, content_style, text_style, card_text_style = get_styles() # estilos

# 2. Importar componentes de la página.
sidebar = get_sidebar() # Barra de controles.
client_content = get_client_content()  # Contenido de visualización de la página.
product_content = get_client_content()  # Contenido de visualización de la página.
segmentacion_content = get_client_content()  # Contenido de visualización de la página.
ai_content = get_client_content()  # Contenido de visualización de la página.

# 3. Inicializar aplicación
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
easymoney_app = dash.Dash('Easy Money',external_stylesheets=external_stylesheets)

# 4. Establecer layout de la web
easymoney_app.layout = html.Div([sidebar, client_content])# 4. Establecer layout de la web
easymoney_app.layout = html.Div([sidebar, client_content])

def get_data():
    """ Lectura de datasets """
    # Nivel de permanencia
    df_bar = anl.get_nivel_permanencia(filename='data/nivel_permanencia.csv')

    # Información de productos contratados (estado igual a 1) por mes de ingesta y número total clientes.
    df_cpi_clientes, df_cpi_productos, df_cpi_ratios = anl.get_informacion_clientes_producto(filename='data/informacion_clientes_con_producto.csv')
    clientes_activos = anl.get_clientes_activos('data/clientes_activos.csv')
    lista_productos = anl.get_lista_productos(filename='data/lista_productos.csv')

    return df_bar, clientes_activos, df_cpi_clientes, df_cpi_productos, df_cpi_ratios, lista_productos#df_cpi_clientes, df_cpi_productos, df_cpi_ratios