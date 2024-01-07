import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

import input
from partials import modals


def layout():
    
    return dbc.Container([

    html.Div([],
        id='id-alert-container', 
            style={
                'position': 'absolute',
                'zIndex': '10001',
                'right': 0,
                'marginRight': '2rem',
                'opacity': 0.75,
                'width': '15rem',
                'top': '1rem',
            },
    ),

    modals.modal_update_delete,
    modals.modal_create,
    modals.modal_change_color,

    dcc.Store(id='id-store-units', data=input.units),
    dcc.Store(id='id-store-results', data=None),
    dcc.Store(id='id-store-colors', data=input.units_colors),

    dbc.Row([

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5('Map with units locations and technical information'),
                    html.Div(
                        dcc.Graph(
                            id='id-graph-map',
                            config={'modeBarButtonsToRemove': ['lasso2d', 'zoom2d', 'pan2d', 'zoomInGeo', 'zoomOutGeo', 'resetScale2d', 'resetGeo', 'zoom2d', 'toImage'], 'displaylogo': False},
                            style={'maxWidth':' 800px', 'margin': 'auto'}
                            ) 
                    ),
                ]), className='mb-2 shadow-box'),
        ], xxl=8, className='mb-2', style={'display': 'grid'}),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5("Unit's geographical coordinates"),   
                            html.Div(
                            dag.AgGrid(
                                id='id-table',   
                                columnDefs=[
                                    { 'field': 'name', 'sortable': True, 'resizable': True},
                                    { 'field': 'lat', 'resizable': True},
                                    { 'field': 'lon', 'resizable': True},
                                    ],
                                dashGridOptions={'pagination':True, 'paginationAutoPageSize': True, 'rowSelection':'single'},
                                columnSize='responsiveSizeToFit',
                                )
                            ),             
                ]), className='mb-2 shadow-box'),
        ], xxl=4, className='mb-2', style={'display': 'grid'})
    ]), 

    dbc.Row([

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5('Configuration panel'),
                    html.H6('Change color of unit type:', className='my-3'),
                    html.Div(id='id-div-colors'),
                    html.Div(
                        dbc.Button([
                            html.I(className='bi bi-power me-2'),
                            'Generate results',
                            ],
                            id='id-button-generate-results',
                            n_clicks=0,
                            outline=True, 
                            color='secondary',
                            className='d-flex align-items-center'
                            ),
                        className='d-grid gap-2'
                    ),
                ]), className='mb-2 shadow-box'),
        ], xxl=4, className='mb-2', style={'display': 'grid'}),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H5('Unit commitment results'),
                    dcc.Graph(
                        id='id-graph-results',
                        config={'displayModeBar': False},
                        className='p-1'
                        ),                  
                ]), className='mb-2 shadow-box'),
        ], xxl=8, className='mb-2', style={'display': 'grid'})
    ]), 
], className='page-container')
