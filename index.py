from dash import Dash, html, dcc, callback, Output, Input, State

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([

    dcc.Store(id='id-store-units', data=input.units),

    html.Div('Hello World'),
    dcc.Dropdown(
        id='id-dropdown-1',
        options=units,
        value=units[1],  # 'Coal 2',
        multi=False
    ),
    html.H4(id='id-output-1'),
    html.P(id='id-output-2'),
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


if __name__ == '__main__':
    app.run(debug=True)