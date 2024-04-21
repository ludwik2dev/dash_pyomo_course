import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os
from waitress import serve
import socket


load_dotenv(override=True)


app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    use_pages=True
    )
server = app.server

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
    
    if os.environ.get("MODE") == 'PRD':

        # Get your IP address and share it if you are working Intranet)
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        PORT = 8080

        print(f'Link to share on Intranet: http:{ip_address}:{PORT}')

        # Go to localhost:<PORT> on local machine
        serve(server, host='0.0.0.0', port=PORT) 

    elif os.environ.get("MODE") == "DEV":
        app.run(debug=True)

    else:
        print('Proper environment type was not provided!')