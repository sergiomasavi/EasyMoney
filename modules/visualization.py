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
        x=df_bar['region_permanencia'],
        y=df_bar['total'],
        name='Permanencia'
    ))

    fig.update_layout(title_text="Nivel de permanencia", yaxis_title='Total (%)', xaxis_title='Meses como cliente')
    fig.update_traces(hovertemplate="%{y:.2f}")

    # fig_line.update_yaxes(tickprefix="$")

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