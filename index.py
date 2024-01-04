from dash import Dash, html, dcc, callback, Output, Input

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([
    html.Div('Hello World'),
    dcc.Dropdown(
        id='id-dropdown',
        options=units,
        value=units[1],  # 'Coal 2',
        multi=False
    ),
    html.H4(id='id-output'),
])


@callback(
    Output('id-output', 'children'),
    Input('id-dropdown', 'value'),
    prevent_initial_call=True
)
def select_dropdown(value):

    return f'User chose: {value}'


if __name__ == '__main__':
    app.run(debug=True)