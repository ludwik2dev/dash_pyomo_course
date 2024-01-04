from dash import Dash, html, dcc

import input


units = list(input.units.keys())


app = Dash(__name__)

app.layout = html.Div([
    html.Div('Hello World'),
    dcc.Dropdown(
        options=units,
        value=units[1],  # 'Coal 2',
        multi=False
    )
])

if __name__ == '__main__':
    app.run(debug=True)