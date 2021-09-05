"""
Controles de la aplicación
"""

# Librerías.
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Paquetes
from app.styles import get_styles
from EasyMoney import analisis as anl

# 1. Obtener estilos
sidebar_style, content_style, text_style, card_text_style = get_styles()

def get_sidebar():
    """
    Crear sidebar.

    Return:
    ------
        sidebar [{dash.html.Div.Div}] -- HTML del sidebar
    """
    print('Creating sidebar...')

    # 1. Crear controles
    controls = get_sidebar_controls()

    # 2. Crear sidebar
    sidebar = html.Div(
        [
            html.H2('Parameters',
                    style=text_style),
                    html.Hr(),
                    controls
        ],

        style=sidebar_style)

    return sidebar

def get_sidebar_controls():
    """
    Crear FormGroup con los controles del sidebar.

    Return:
    ------
        form [{dash_bootstrap_components._components.FormGroup.FormGroup}] -- Sidebar de la aplicación web.
    """
    print('Creating sidebar controls...')

    # 1.Crear componentes
    # 1.1. Titulo
    dropdown_title = html.P('Selección de productos', style={
                'textAlign': 'center'
            })

    # 1.2. DropDown
    lista_productos = anl.get_lista_productos(filename='data/lista_productos.csv')
    dropdown_options = []
    for i, producto in enumerate(lista_productos):
        opt = {
            'label': ' '.join(producto.title().split('_')),
            'value': f'dropdown_v{i+1}'
        }
        dropdown_options.append(opt)

    default_dropdown_values = [opt['value'] for opt in dropdown_options]
    dropdown = dcc.Dropdown(id='dropdown',
                            options=dropdown_options,
                            value=default_dropdown_values,  # default value
                            multi=True
                            )


    # 1.3. Range Slider
    range_slider_title = html.P('Range Slider',
                                style={
                                    'textAlign': 'center'
                                })

    range_slider = dcc.RangeSlider(id='range_slider',
                                   min=0,
                                   max=20,
                                   step=0.5,
                                   value=[5, 15]
                                   )

    # 1.4. ChecBox
    checkbox_title = html.P('Check Box',
                            style={
                                'textAlign': 'center'
                            })

    checkbox_options = [
        {
            'label': 'Value One',
            'value': 'value1'
        },
        {
            'label': 'Value Two',
            'value': 'value2'
        },
        {
            'label': 'Value Three',
            'value': 'value3'
        }
    ]

    checkbox_value = ['value1', 'value2']

    checkbox_card = dbc.Card(
        [
            dbc.Checklist(
                id='check_list',
                options=checkbox_options,
                value=checkbox_value,
                inline=True
            )])

    # 1.5. RadioItems
    radioitems_title = html.P('Selector de servicio',
                              style={
                                  'textAlign': 'center'
                                    })

    radioitems_options = [
        {
            'label': 'Clientes',
            'value': 'radioitems_value1'
        },
        {
            'label': 'Productos',
            'value': 'radioitems_value2'
        },
        {
            'label': 'Segmentación',
            'value': 'radioitems_value3'
        },
        {
            'label': 'Aprendizaje',
            'value': 'radioitems_value4'
        }
    ]
    radioitems_value = 'radioitems_value1'
    radioitems_card = dbc.Card(
        [
            dbc.RadioItems(
                id='radio_items',
                options=radioitems_options,
                value=radioitems_value,
                style={
                    'margin': 'auto'
                }
            )])

    # 1.6. Submit button.
    submit_button = dbc.Button(
        id='submit_button',
        n_clicks=0,
        children='Submit',
        color='primary',
        block=True
    )

    # 2. Formulario de control
    controls = dbc.FormGroup(
        [
            radioitems_title,
            radioitems_card,
            html.Br(),  # salto de línea
            dropdown_title,
            dropdown,
            html.Br(), # salto de línea
            range_slider_title,
            range_slider,
            checkbox_title,
            checkbox_card,
            html.Br(), # salto de línea
            submit_button,
        ]
    )

    return controls

def get_client_content():
    """
    Crear contenido de la página web. El contenido está dividido en tres filas.

    Return:
    -------
        content [{dash.html.Div.Div}] -- Código html de la página web.
    """
    print('Creating content...')

    # Obtener contenido de las filas.
    content_first_row = get_content_first_row()
    content_second_row = get_content_second_row()
    content_third_row = get_content_third_row()
    content_fourth_row = get_content_fourth_row()

    content = html.Div(
        [
            html.H2(children='Easy Money Autoservice BI',
                    style=text_style,
                    id='web_title'),
            html.Hr(),
            content_first_row,
            content_second_row,
            content_third_row,
            content_fourth_row
        ],
        style=content_style
    )

    return content

def get_content_first_row():
    """
    Crear contenido de la primera fila del contenido de la página.

    Returns:
    -------
        content_first_row [{dash_bootstrap_components._components.Row.Row}] --- Contenido de la primera fila
    """
    print('Creating content first row...')

    # 1. First row. First column
    card_first_col = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Clientes',
                                className='card-title',
                                style=card_text_style,
                               ),

                        html.P('Análisis de clientes', style=card_text_style),
                    ]
                ),
            ])

    first_col = dbc.Col(card_first_col,
                        md=3
                        )

    # 2. First row. Second Column
    card_second_col = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Productos',
                                className='card-title',
                                style=card_text_style),

                        html.P('Análisis de productos', style=card_text_style),
                    ]
                ),
            ])

    second_col = dbc.Col(card_second_col,
                         md=3
                     )


    # 3. First row. Third Column
    card_third_col = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Segmentación', className='card-title', style=card_text_style),
                        html.P('Segmentación de clientes', style=card_text_style),
                    ]
                ),
            ])

    third_col = dbc.Col(card_third_col,
                        md=3
                    )

    # 4. First rowFourth Column
    card_fourth_col = dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4('AI', className='card-title', style=card_text_style),
                            html.P('Machine Learning', style=card_text_style),
                        ]
                    ),
                ])
    fourth_col = dbc.Col(card_fourth_col,
                         md=3
                         )

    # X. Contenido de la primera fila.
    content_first_row = dbc.Row(
        [
            first_col,
            second_col,
            third_col,
            fourth_col
        ]
    )

    return content_first_row

def get_content_second_row():
    """
    Crear contenido de la segunda fila del contenido de la página.

    Returns:
    -------
        content_segunda_row [{dash_bootstrap_components._components.Row.Row}] --- Contenido de la segunda fila
    """
    print('Creating content second row...')
    content_second_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='graph_1'), md=6
            ),
            dbc.Col(
                dcc.Graph(id='graph_3'), md=6
            )
        ])

    return content_second_row

def get_content_third_row():
    """
    Crear contenido de la tercera fila del contenido de la página.

    Returns:
    -------
        content_third_row [{dash_bootstrap_components._components.Row.Row}] --- Contenido de la tercera fila
    """
    print('Creating content third row...')

    content_third_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='graph_4'), md=12,
            )
        ]
    )

    return content_third_row

def get_content_fourth_row():
    """
    Crear contenido de la cuarta fila del contenido de la página.

    Returns:
    -------
        content_fourth_row [{dash_bootstrap_components._components.Row.Row}] --- Contenido de la cuarta fila
    """
    print('Creating content third row...')

    content_fourth_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='graph_5'), md=6
            ),
            dbc.Col(
                dcc.Graph(id='graph_6'), md=6
            )])

    return content_fourth_row