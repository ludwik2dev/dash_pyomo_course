import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os


load_dotenv()

mode = os.environ.get("MODE")


app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    use_pages=True
    )

app.layout = dbc.Container([
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
], className='main-container')


if __name__ == '__main__':
    
    if mode == 'PRD':

        from waitress import serve
        import platform


        computer_name = platform.node()
        wsgi_app = app.server

        serve(wsgi_app, host=computer_name, port=8080)

    elif mode == "DEV":
        app.run(debug=True)

    else:
        print('Proper environment type was not provided!')