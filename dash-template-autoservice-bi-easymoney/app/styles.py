"""
Variables de estilo de la página web.
"""

def get_styles():
    """
    Crear las variables de estilo de la página web.

    Returns:
        sidebar_style [{}] --
        content_style [{}] --
        text_style [{}] --
        card_text_style [{}] --

    """
    print('Setting styles...')
    # 1. Argumentos de estilo para la barra lateral.
    sidebar_style = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        'background-color': '#f8f9fa'
    }

    # 2. Argumentos de estilo para el contenido de la página principal.
    content_style = {
        'margin-left': '25%',
        'margin-right': '5%',
        'padding': '20px 10p'
    }

    text_style = {
        'textAlign': 'center',
        'color': '#191970'
    }

    card_text_style = {
        'textAlign': 'center',
        'color': '#0074D9'
    }

    return sidebar_style, content_style, text_style, card_text_style