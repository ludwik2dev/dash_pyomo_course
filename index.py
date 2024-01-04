from dash import Dash, html, dcc, callback, Output, Input

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([
    html.Div('Hello World'),
    dcc.Dropdown(
        id='id-dropdown-1',
        options=units,
        value=units[1],  # 'Coal 2',
        multi=False
    ),
    dcc.Dropdown(
        id='id-dropdown-2',
        options=units,
        value=units[2], 
        multi=False
    ),
    html.H4(id='id-output-1'),
    html.H4(id='id-output-2'),
])


@callback(
    Output('id-output-1', 'children'),
    Output('id-output-2', 'children'),
    Input('id-dropdown-1', 'value'),
    Input('id-dropdown-2', 'value'),
    prevent_initial_call=True
)
def select_dropdown(value_1, value_2):

    text_1 = f'First selection: {value_1}'
    text_2 = f'Second selection: {value_2}'

    return text_1, text_2


if __name__ == '__main__':
    app.run(debug=True)