import dash
from dash import html, dcc, callback, Output, Input, State, Patch, no_update, ALL, ctx
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
from dash.exceptions import PreventUpdate

import input
from partials import modals


dash.register_page(__name__)


units = list(input.units.keys())
min_lat, max_lat = (25, 37)
min_lon, max_lon = (-112.5, -87.5)


layout = dbc.Container([

    html.Div([],
        id='id-alert-container', 
            style={
                'position': 'absolute',
                'zIndex': '10001',
                'right': 0,
                'marginRight': '2rem',
                'opacity': 0.75,
                'width': '15rem',
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


def make_alerts(alerts, msg, color):
    ALERT_TIME = 10  # sec
    alerts.append(
        dbc.Alert(
            msg, 
            is_open=True, 
            color=color, 
            duration=ALERT_TIME*1000
            )
        )

    return alerts


@callback(
    Output('id-store-results', 'data'),
    Input('id-button-generate-results', 'n_clicks'),
    prevent_initial_call=True
)
def generate_results(click):
    
    '''Simulating running pyomo model'''
    
    results = input.results
    
    return results


@callback(
    Output('id-graph-results', 'figure'),
    Input('id-store-results', 'data'),
    Input('id-store-colors', 'data'),
    State('id-store-units', 'data'),
)
def generate_graph_results(results, colors, units):

    sorted_units = sorted( units.items(), key=lambda x: x[1]['vc'])
    sorted_units = dict(sorted_units).keys()

    fig = go.Figure()
    for unit in sorted_units:
        if results is None:
            break
        if unit not in results.keys():
            continue

        x = results[unit].keys()  # each hour
        y = results[unit].values()  # each hour
        kind = units[unit]['type']

        fig.add_trace(
            go.Bar(
                x=list(x),
                y=list(y),
                name=unit,
                marker=dict(color=colors[kind], opacity=0.6, line=dict(width=0.5, color='black')),
                hovertemplate='Power: %{y} MW',
                showlegend=False
            )
        )
    fig.update_layout(
        barmode='relative',
        bargap=0,
        plot_bgcolor='white',
        height=250, 
        margin={'r':5,'t':5,'l':5,'b':5},
    )
    fig.update_xaxes(
        tickfont=dict(size=11),
        linewidth=1,
        linecolor='black',
        ticks='outside',
        mirror=True
    )
    fig.update_yaxes(
        title=dict(text='Power [MW]', font=dict(size=14)),
        tickfont=dict(size=11),
        linewidth=1,
        linecolor='black',
        ticks='outside',
        mirror=True
    )

    if results is None:
        fig.add_annotation(
            text='To see results click button first',
            xref='paper', 
            yref='paper',
            x=0.5, 
            y=0.5, 
            showarrow=False
            )
    
    return fig


@callback(
    Output('id-graph-map', 'figure'),
    Input('id-store-units', 'data'),
    Input('id-store-colors', 'data')
)
def generate_graph_map(units, colors):

    fig = go.Figure()
    for unit in units.keys():
        kind = units[unit]['type']
        fig.add_trace(
            go.Scattergeo(
            lon=[units[unit]['lon']],
            lat=[units[unit]['lat']],
            text=[unit],
            mode='markers',
            name='',
            customdata=[units[unit]['power']],
            showlegend=False,
            hovertemplate='%{text} : %{customdata} MW',
            marker=dict(
                size=units[unit]['power']/10,
                opacity=0.6,
                reversescale=True,
                autocolorscale=False,
                symbol='circle',
                color=colors[kind],
                line=dict(
                    width=1,
                    color='black',
                    ),
                )
            )
        )

    fig.add_trace(
        go.Scattergeo(
            lon=[ ele[0] for ele in input.texas_boundaries ],
            lat=[ ele[1] for ele in input.texas_boundaries ],
            line_color='brown',
            line_width=2,
            mode='lines',
            showlegend=False,
            hoverinfo='none',
            text=[ 'border' for _ in input.texas_boundaries ],
        ))

    fig.update_layout(
            height=375, 
            margin={'r':5,'t':5,'l':5,'b':5},
            geo=dict(
                landcolor='rgb(250, 250, 250)',
                oceancolor='#ccf5ff',
                lakecolor='#ccf5ff',
                showcountries=True,
                showlakes=True,
                showland=True,
                showocean=True,
                showrivers=True,
                resolution=50, 
                scope='world',
                lataxis={'range': [min_lat, max_lat]},
                lonaxis={'range': [min_lon, max_lon]},
            ), 
        )
    fig.add_annotation(x=0, y=0, text='', showarrow=False)
    
    return fig


@callback(
    Output('id-table', 'rowData'), 
    Output('id-table', 'getRowStyle'), 
    Input('id-store-units', 'data'),
    Input('id-store-colors', 'data'),
)
def create_grid(units, colors):

    data = []
    for key, value in units.items():
        value['name'] = key
        data.append(value)
    df = pd.DataFrame.from_dict(data)

    df_colors = pd.DataFrame(list( zip( colors.keys(), colors.values() ) ), columns=['type', 'color']) 
    df = df.merge(df_colors, on=['type'])
    data = df.to_dict('records')
    
    getRowStyle = {
        'styleConditions': [
            {
                'condition': f"params.data.type == '{kind}'",
                'style': {'color': color},
            } for kind, color in colors.items()
        ] 
    }
    
    return data, getRowStyle


@callback(
    Output('id-graph-map', 'figure', allow_duplicate=True),
    Input('id-table', 'selectedRows'),
    prevent_initial_call=True
)
def create_annotation(row_selected): 

    lat = (float(row_selected[0]['lat']) - min_lat) / ( max_lat - min_lat )
    lon = (float(row_selected[0]['lon']) - min_lon) / ( max_lon - min_lon )
    text = row_selected[0]['name']

    patched_figure = Patch()
    patched_figure['layout']['annotations'].clear()
    patched_figure['layout']['annotations'].extend(
        [
            dict(
                xref='paper',
                yref='paper',
                x=lon, 
                y=lat,
                text=text,
                showarrow=False,
                bgcolor='white',
                opacity=0.6,
            ),
        ])

    return patched_figure 


@callback(
    Output('id-graph-map', 'figure', allow_duplicate=True),
    Input('id-table', 'cellDoubleClicked'),
    prevent_initial_call=True
)
def delete_annotations(row_selected):

    patched_figure = Patch()
    patched_figure['layout']['annotations'].clear()

    return patched_figure 


@callback(
    Output('id-modal-update-delete-unit', 'is_open'),
    Output('id-graph-map', 'clickData'),
    Output('id-modal-update-delete-unit-header', 'children'),
    Output('id-input-update-delete-power', 'value'),
    Output('id-input-update-delete-vc', 'value'),
    Output('id-input-update-delete-lat', 'value'),
    Output('id-input-update-delete-lon', 'value'),
    Input('id-graph-map', 'clickData'),
    State('id-store-units', 'data'),
    prevent_initial_call=True
)
def open_modal_update_delete_unit(clickData, units):

    if clickData['points'][0]['text'] == 'border':
        raise PreventUpdate
    
    unit = clickData['points'][0]['text']
    power = units[unit]['power']
    vc = units[unit]['vc']
    lat = units[unit]['lat']
    lon = units[unit]['lon']
    
    return True, None, unit, power, vc, lat, lon


@callback(
    Output('id-modal-update-delete-unit', 'is_open', allow_duplicate=True),
    Output('id-store-units', 'data', allow_duplicate=True), 
    Output('id-alert-container', 'children', allow_duplicate=True),
    Input('id-button-delete', 'n_clicks'),
    State('id-store-units', 'data'), 
    State('id-modal-update-delete-unit-header', 'children'),
    State('id-alert-container', 'children'),
    prevent_initial_call=True
)
def delete_unit(click, data, name, alerts):

    del data[name]

    msg = f'Deleted unit: {name}'
    color = 'success'
    alerts = make_alerts(alerts, msg, color)

    return False, data, alerts


@callback(
    Output('id-modal-update-delete-unit', 'is_open', allow_duplicate=True),
    Output('id-store-units', 'data', allow_duplicate=True), 
    Output('id-alert-container', 'children', allow_duplicate=True),
    Input('id-button-update', 'n_clicks'),
    State('id-store-units', 'data'), 
    State('id-modal-update-delete-unit-header', 'children'),
    State('id-input-update-delete-power', 'value'),
    State('id-input-update-delete-vc', 'value'),
    State('id-alert-container', 'children'),
    prevent_initial_call=True
)
def update_unit(click, data, name, power, vc, alerts):

    # Error handling
    for value in [power, vc]:
        if value is None or value < 0 or value > 1500:
            msg = f'Unit: {name} was not updated.'
            color = 'warning'
            alerts = make_alerts(alerts, msg, color)
            return False, no_update, alerts

    data[name]['power'] = power
    data[name]['vc'] = vc

    msg = f'Updated unit: {name}'
    color = 'success'
    alerts = make_alerts(alerts, msg, color)

    return False, data, alerts


@callback(
    Output('id-modal-create-unit', 'is_open'),
    Output('id-input-create-lat', 'value'),
    Output('id-input-create-lon', 'value'),
    Input('id-graph-map', 'selectedData'),
    prevent_initial_call=True
)
def open_modal_create_unit(select):
    
    if select is None:
        raise PreventUpdate  # return no_update
    
    rectangle = select['range']['geo']
    lon = round( 0.5 * ( rectangle[0][0] + rectangle[1][0] ), 2 )
    lat = round( 0.5 * ( rectangle[0][1] + rectangle[1][1] ), 2 )
    
    return True, lat, lon


@callback(
    Output('id-modal-create-unit', 'is_open', allow_duplicate=True),
    Output('id-store-units', 'data', allow_duplicate=True), 
    Output('id-input-create-name', 'value', allow_duplicate=True),
    Output('id-alert-container', 'children', allow_duplicate=True),
    Input('id-button-create', 'n_clicks'),
    State('id-store-units', 'data'), 
    State('id-input-create-name', 'value'),
    State('id-input-create-type', 'value'),
    State('id-input-create-power', 'value'),
    State('id-input-create-vc', 'value'),
    State('id-input-create-lat', 'value'),
    State('id-input-create-lon', 'value'),
    State('id-alert-container', 'children'),
    prevent_initial_call=True
)
def create_unit(click, data, name, kind, power, vc, lat, lon, alerts):

    # Error handling
    for value in [power, vc]:
        if value is None or value < 0 or value > 1500:
            msg = f'Unit: {name} was not created.'
            color = 'warning'
            alerts = make_alerts(alerts, msg, color)
            return False, data, None, alerts

    new_unit = {
        'type': kind, 
        'lat': lat, 
        'lon': lon, 
        'power': power, 
        'vc': vc, 
    }
    data[name] = new_unit

    msg = f'Created unit: {name}'
    color = 'success'
    alerts = make_alerts(alerts, msg, color)
    
    return False, data, None, alerts


@callback(
    Output('id-button-create', 'disabled'),
    Input('id-input-create-name', 'value'),
    State('id-store-units', 'data'), 
    prevent_initial_call=True
)
def check_unit_name(text, data):

    if text is None or len(text) < 3 or text in data.keys():
        return True
    return False


@callback(
    Output('id-div-colors', 'children'),
    Input('id-store-colors', 'data')
)
def generate_colors_div(colors):
    
    lst = []
    for key, value in colors.items():
        lst.append(
            dbc.Button(
                key.title(),
                id={'index': f'id-button-color-{key}', 'type': 'change-color'},
                style={'color': value,},
                color='link'
            )
        )

    return lst


@callback(
    Output('id-modal-change-color', 'is_open'),
    Output('id-color-picker', 'value'),
    Output('id-color-picker', 'label'),
    Input({'type': 'change-color', 'index': ALL}, 'n_clicks'),
    State('id-store-colors', 'data'),
    prevent_initial_call=True
)
def open_modal_color_change(clicks, colors):

    if not any(clicks):
        raise PreventUpdate

    unit_clicked = ctx.triggered_id['index'].split('-')[-1]
    color = colors[unit_clicked]
    color = dict(hex=color)
    label = unit_clicked

    return True, color, label


@callback(
    Output('id-modal-change-color', 'is_open', allow_duplicate=True),
    Output('id-store-colors', 'data'),
    Input('id-button-change-color', 'n_clicks'),
    State('id-color-picker', 'value'),
    State('id-color-picker', 'label'),
    State('id-store-colors', 'data'),
    prevent_initial_call=True
)
def save_color(click, value, unit, colors):

    color = value['hex']
    colors[unit] = color

    return False, colors