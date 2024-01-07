import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    use_pages=True
    )

app.layout = html.Div([
    dbc.NavbarSimple([
        dbc.NavItem(dbc.NavLink('Home', href='/')),
        dbc.NavItem(dbc.NavLink('Dashboard', href='dashboard')),
    ],
    brand='Unit Commitment App',
    brand_href='/',
    color='secondary',
    dark=True,
    className='px-4',
    ),    
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)