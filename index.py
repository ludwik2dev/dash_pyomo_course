from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([

    dcc.Store(id='id-store-units', data=input.units),
    dcc.Store(id='id-store-results', data=input.results),
    dcc.Store(id='id-store-colors', data=input.units_colors),

    html.Div('Hello World'),
    dcc.Dropdown(
        id='id-dropdown-1',
        options=units,
        value=units[1],  # 'Coal 2',
        multi=False
    ),
    html.H4(id='id-output-1'),
    html.P(id='id-output-2'),

    dcc.Graph(id='id-graph-results'),  

])


@callback(
    Output('id-output-1', 'children'),
    Output('id-output-2', 'children'),
    Input('id-dropdown-1', 'value'),
    State('id-store-units', 'data'),
    prevent_initial_call=True
)
def select_dropdown(value, units):

    text_1 = f'First selection: {value}'
    text_2 = f'Power of chose unit: {units[value]["power"]}'

    return text_1, text_2


@callback(
    Output('id-graph-results', 'figure'),
    Input('id-store-results', 'data'),
    State('id-store-colors', 'data'),
    State('id-store-units', 'data'),
)
def generate_graph_results(results, colors, units):

    sorted_units = sorted( units.items(), key=lambda x: x[1]['vc'])
    sorted_units = dict(sorted_units).keys()

    fig = go.Figure()
    for unit in sorted_units:
        if results is None:
            break
        if unit not in results.keys():
            continue

        x = results[unit].keys()  # each hour
        y = results[unit].values()  # each hour
        kind = units[unit]['type']

        fig.add_trace(
            go.Bar(
                x=list(x),
                y=list(y),
                name=unit,
                marker=dict(color=colors[kind], opacity=0.6, line=dict(width=0.5, color='black')),
                hovertemplate='Power: %{y} MW',
                showlegend=False
            )
        )
    fig.update_layout(
        barmode='relative',
        bargap=0,
        plot_bgcolor='white',
        height=250, 
        margin={'r':5,'t':5,'l':5,'b':5},
    )
    fig.update_xaxes(
        tickfont=dict(size=11),
        linewidth=1,
        linecolor='black',
        ticks='outside',
        mirror=True
    )
    fig.update_yaxes(
        title=dict(text='Power [MW]', font=dict(size=14)),
        tickfont=dict(size=11),
        linewidth=1,
        linecolor='black',
        ticks='outside',
        mirror=True
    )
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)