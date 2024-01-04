from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([

    dcc.Store(id='id-store-units', data=input.units),
    dcc.Store(id='id-store-results', data=input.results),

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
)
def generate_results_graph(results):

    fig = go.Figure()
    for unit in results.keys():

        x = results[unit].keys()  # each hour
        y = results[unit].values()  # each hour

        fig.add_trace(
            go.Bar(
                x=list(x),
                y=list(y),
                name=unit,
            )
        )

    return fig


if __name__ == '__main__':
    app.run(debug=True)