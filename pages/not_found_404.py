import dash
from dash import html


dash.register_page(__name__)


layout = html.Div([
    html.H2('This is our custom 404 content')
], className='page-container')