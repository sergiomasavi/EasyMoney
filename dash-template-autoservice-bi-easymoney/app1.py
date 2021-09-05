"""
Prototipo de Autoservicio BI de EasyMoney. La plantilla utiliza:
 - Dash bootstrap (dbc). componentes dash boostrap.
 - Dash HTML (hml). Componentes dash html.
 - Dash core (dcc). Componentes dash core.

El diseño consiste en:
 - Barra lateral de control.
 - Página de contenido principal.
"""
print(5*'-' + 'Easy Money - Autoservicio BI ' + 5 * '-')

# Librerías
print('Importing libs...')
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px

# Paquetes
print('Importing pkgs...')
from app import easymoney_app, get_data, sidebar, client_content, product_content, segmentacion_content, ai_content
from EasyMoney import visualization as vs
from EasyMoney import analisis as anl
from app import utils as utl

# 1. Importar datos
df_bar, clientes_activos, df_cpi_clientes, df_cpi_productos, df_cpi_ratios, lista_productos = get_data()

# 2. Definición de los callbacks
print('Defining callbacks...')

# Callback figura 1.
@easymoney_app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value')])
def update_graph_1(n_clicks, dropdown_value):
    nuevos_clientes_productos = df_cpi_clientes[['nuevos_clientes']].join(df_cpi_productos['nuevos_productos'])
    productos_seleccionados = utl.decode_dropdown_selection(lista_productos, dropdown_value)
    clientes_productos_contratados = df_cpi_clientes[['numero_clientes']].join(df_cpi_productos['productos_contratados'])

    fig = vs.bar_nuevos_clientes_productos(nuevos_clientes_productos,
                                           clientes_productos_contratados,
                                           clientes_activos,
                                           productos_seleccionados,
                                           show_fig=False)
    return fig


# Callback figura 3.
@easymoney_app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value')])
def update_graph_3(n_clicks, dropdown_value):
    productos_seleccionados = utl.decode_dropdown_selection(lista_productos, dropdown_value)
    clientes_productos_contratados = df_cpi_clientes[['numero_clientes']].join(df_cpi_productos['productos_contratados'])
    nuevos_clientes_productos = df_cpi_clientes[['nuevos_clientes']].join(df_cpi_productos['nuevos_productos'])

    fig = vs.bar_clientes_productos_ratio(df_cpi_ratios.iloc[1:].copy(),
                                          nuevos_clientes_productos.copy(),
                                          clientes_productos_contratados.copy(),
                                          clientes_activos.copy(),
                                          productos_seleccionados.copy(),
                                          show_fig=False)
    return fig


# Callback figura 4.
@easymoney_app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    clientes_productos_contratados = df_cpi_clientes[['numero_clientes']].join(df_cpi_productos['productos_contratados'])

    productos_seleccionados = utl.decode_dropdown_selection(lista_productos, dropdown_value)


    fig = vs.scatter_clientes_productos(clientes_productos_contratados,
                                        clientes_activos,
                                        productos_seleccionados,
                                        show_fig=False)
    return fig


# Callback figura 5.
@easymoney_app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length')
    return fig


# Callback figura 6.
@easymoney_app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')]
)
def update_graph_6(n_clicks):
    print(n_clicks)

    fig_bar_np = vs.bar_nivel_permanencia(df_bar=df_bar, plot=False)
    return fig_bar_np

"""
# Callback card title 1.
@easymoney_app.callback(
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure

"""

## 4. Establecer layout de la web
#easymoney_app.layout = html.Div([sidebar, client_content])

# Callback card text 1.
@easymoney_app.callback(
    Output('web_title', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('radio_items', 'value')]
)
def update_card_text_1(n_clicks, radio_items_value):
    # 1. Obtener título personalizado por sección
    base_title = 'Easy Money Autoservice BI'
    radioitems_options = {
        'radioitems_value1': 'Clientes',
        'radioitems_value2': 'Productos',
        'radioitems_value3': 'Segmentación',
        'radioitems_value4': 'Aprendizaje Automático',

    }
    label = base_title + ' - ' +radioitems_options[radio_items_value]

    # 2. Establecer layout correspondiente a la sección
    if radioitems_options[radio_items_value] == 'Clientes':
        easymoney_app.layout = html.Div([sidebar, client_content])

    return label

if __name__ == '__main__':
    easymoney_app.run_server(port=8085, debug=True)




