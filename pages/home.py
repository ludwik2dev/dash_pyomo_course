import dash
from dash import html


dash.register_page(__name__, path='/')


layout = html.Div([   
    html.H1('Welcome home!'),
    html.Br(),
    html.P('Describe your app here!'),
], className='page-container')