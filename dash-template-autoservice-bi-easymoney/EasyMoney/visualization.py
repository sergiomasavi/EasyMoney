# Librerías
import pandas as pd
import plotly
import plotly.graph_objects as go

def violin_plot(y, title, name, plot=True):
    """
    Violinplot del nivel de permanencia

    Args:
    ------
    y {[pandas.DataFrame]} -- Variable y del violinplot

    """
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            y=y,
            box_visible=False,
            line_color='black',
            meanline_visible=True,
            fillcolor='lightseagreen',
            opacity=0.6,
            name=name
        )
    )

    fig.update_layout(yaxis_zeroline=False, title=title)

    if plot:
        fig.show()
    else:
        return fig

def bar_nivel_permanencia(df_bar, plot=True):
    """
    Visualización BarChar del niel de permanencia por región:

        - (1) Fidelización baja. Aquellos clientes que permanencen en el registro entre 0 y 6 meses.
        - (2) Fidelización media. Aquellos clientes que permanecen en el registro entre 7 y 10 meses.
        - (3) Fidelización alta. Aquellos clientes que permanecen en el registro entre 11 y 15 meses.
        - (4) Fidelización completa. Aquellos clientes que permanencen en el registro entre 16 y 17 meses.

    Args:
        df_bar [{pandas.DataFrame}] -- DataFrame del df_bar

    Returns:

    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_bar['region'],
        y=df_bar['total'],
        name='Permanencia'
    ))

    fig.update_layout(title_text="Nivel de permanencia", yaxis_title='Clientes (%)', xaxis_title='Meses')
    fig.update_traces(hovertemplate="%{y:.2f}")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    if plot:
        fig.show()
    else:
        return fig

def scatter_clientes_productos(clientes_productos_contratados, clientes_activos, productos_seleccionados, show_fig=True):
    """
    Visualización temporal del número de clientes con servicio contratado
    y número de productos contratados.
    """

    productos_no_seleccionados = [p for p in clientes_activos.columns.to_list() if p not in productos_seleccionados]

    if len(productos_no_seleccionados) != 0:
        # Productos activos por fecha.
        clientes_productos_contratados['productos_contratados'] = clientes_productos_contratados['productos_contratados'] - clientes_activos[productos_no_seleccionados].sum(axis=1)

    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=clientes_productos_contratados.index,
            y=clientes_productos_contratados['numero_clientes'],
            mode='lines+markers',
            name='Número de clientes'
        )
    )

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=clientes_productos_contratados.index,
            y=clientes_productos_contratados['productos_contratados'],
            mode='lines+markers',
            name='Productos contratados'
        )
    )

    # Configuración
    fig.update_layout(title_text="Evolución temporal de clientes y productos contratados",
                      yaxis_title='Número de clientes', xaxis_title='Meses')
    fig.update_traces(hovertemplate="%{y:.2f}")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    if show_fig:
        fig.show()
    else:
        return fig


def bar_nuevos_clientes_productos(nuevos_clientes_productos,
                                  clientes_productos_contratados,
                                  clientes_activos,
                                  productos_seleccionados,
                                  show_fig=True):
    """

    """

    productos_no_seleccionados = [p for p in clientes_activos.columns.to_list() if p not in productos_seleccionados]

    if len(productos_no_seleccionados) != 0:
        # Productos activos por fecha.
        clientes_productos_contratados['productos_contratados'] = clientes_productos_contratados['productos_contratados'] - clientes_activos[productos_no_seleccionados].sum(axis=1)

        # Productos nuevos contratados.
        nuevos_clientes_productos['nuevos_productos'] = (clientes_productos_contratados['productos_contratados'] - clientes_productos_contratados['productos_contratados'].shift(1)).fillna(0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=nuevos_clientes_productos.index,
        y=nuevos_clientes_productos['nuevos_clientes'],
        name='Nuevos Clientes',
        marker_color='red'
    ))

    fig.add_trace(go.Bar(
        x=nuevos_clientes_productos.index,
        y=nuevos_clientes_productos['nuevos_productos'],
        name='Nuevos Productos',
        marker_color='blue'
    ))

    # Configuración
    fig.update_layout(title_text="Nuevos cientes y productos contratados",
                      yaxis_title='Cantidad', xaxis_title='')
    fig.update_traces(hovertemplate="%{y:.2f}")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    fig.update_layout(legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                                ))
    if show_fig:
        fig.show()
    else:
        return fig


def bar_clientes_productos_ratio(clientes_productos_ratio,
                                 nuevos_clientes_productos,
                                 clientes_productos_contratados,
                                 clientes_activos,
                                 productos_seleccionados,
                                 show_fig=True):
    """

    """
    productos_no_seleccionados = [p for p in clientes_activos.columns.to_list() if p not in productos_seleccionados]

    if len(productos_no_seleccionados) != 0:
        # Productos activos por fecha.
        clientes_productos_contratados['productos_contratados'] = clientes_productos_contratados['productos_contratados'] - clientes_activos[productos_no_seleccionados].sum(axis=1)

        # Productos nuevos contratados.
        nuevos_clientes_productos['nuevos_productos'] = (clientes_productos_contratados['productos_contratados'] - clientes_productos_contratados['productos_contratados'].shift(1)).fillna(0)

        # Ratio de productos respecto a numero de clientes
        clientes_productos_ratio['producto_cliente_ratio'] = clientes_productos_contratados['productos_contratados'] / clientes_productos_contratados['numero_clientes']

        # Ratio de nuevos productos respecto a nuevo número de clientes
        clientes_productos_ratio['nuevos_producto_cliente_ratio'] = (nuevos_clientes_productos['nuevos_productos']/nuevos_clientes_productos['nuevos_clientes']).fillna(0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=clientes_productos_ratio.index,
        y=clientes_productos_ratio['producto_cliente_ratio'],
        name='Ratio Productos - Clientes',
        marker_color='red'
    ))

    fig.add_trace(go.Bar(
        x=clientes_productos_ratio.index,
        y=clientes_productos_ratio['nuevos_producto_cliente_ratio'],
        name='Ratio Nuevos Productos -  Nuevos clientes',
        marker_color='blue'
    ))

    # Configuración
    fig.update_layout(title_text="Ratio de Producto - Cliente",
                      yaxis_title='Cantidad', xaxis_title='')
    fig.update_traces(hovertemplate="%{y:.2f}")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    fig.update_layout(legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                                ))
    if show_fig:
        fig.show()
    else:
        return fig