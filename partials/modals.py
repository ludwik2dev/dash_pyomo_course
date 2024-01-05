import dash_bootstrap_components as dbc
from dash import dcc
import dash_daq as daq

import input


modal_update_delete = dbc.Modal([

    dbc.ModalHeader(dbc.ModalTitle('Header', id='id-modal-update-delete-unit-header')),
    dbc.ModalBody([

        dbc.Form([
            dbc.Row([
                    dbc.Label('Power', width=3, html_for='id-input-update-delete-power'),
                    dbc.Col(
                        dbc.Input(id='id-input-update-delete-power', type='number'),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Variable cost', width=3, html_for='id-input-update-delete-vc'),
                    dbc.Col(
                        dbc.Input(id='id-input-update-delete-vc', type='number'), 
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Latitude', width=3, html_for='id-input-update-delete-lat'),
                    dbc.Col(
                        dbc.Input(id='id-input-update-delete-lat', type='number', disabled=True),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Longitude', width=3, html_for='id-input-update-delete-lon'),
                    dbc.Col(
                        dbc.Input(id='id-input-update-delete-lon', type='number', disabled=True),
                        width=9,
                    )], className='mb-3')
        ])
    ]),        
    dbc.ModalFooter([
        dbc.Button('Delete', id='id-button-delete', n_clicks=0, color='danger'),
        dbc.Button('Update', id='id-button-update',  n_clicks=0, color='success'),
    ]),
],
    id='id-modal-update-delete-unit',
    is_open=False
)

modal_create = dbc.Modal([

    dbc.ModalHeader(dbc.ModalTitle('Create new unit')),

    dbc.ModalBody([

        dbc.Form([
            dbc.Row([
                    dbc.Label('Unit name', width=3, html_for='id-input-create-name'),
                    dbc.Col(
                        dbc.Input(id='id-input-create-name', type='text', placeholder='Name must be unique'),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Unit type', width=3, html_for='id-input-create-type'),
                    dbc.Col(
                        dcc.Dropdown(options=input.unit_types, value='coal', clearable=False, id='id-input-create-type'),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Power', width=3, html_for='id-input-create-power'),
                    dbc.Col(
                        dbc.Input(id='id-input-create-power', type='number', value=200),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Variable cost', width=3, html_for='id-input-create-vc'),
                    dbc.Col(
                        dbc.Input(id='id-input-create-vc', type='number', value=100), 
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Latitude', width=3, html_for='id-input-create-lat'),
                    dbc.Col(
                        dbc.Input(id='id-input-create-lat', type='number', value=30, disabled=True),
                        width=9,
                    )], className='mb-3'),
            dbc.Row([
                    dbc.Label('Longitude', width=3, html_for='id-input-create-lon'),
                    dbc.Col(
                        dbc.Input(id='id-input-create-lon', type='number', value=-100, disabled=True),
                        width=9,
                    )], className='mb-3')
        ])
    ]),        
    dbc.ModalFooter([
        dbc.Button('Create', id='id-button-create', n_clicks=0, color='success', disabled=True),
    ]),
],
    id='id-modal-create-unit',
    is_open=False
)

modal_change_color = dbc.Modal([

    dbc.ModalHeader(dbc.ModalTitle('Change color')),

    dbc.ModalBody([

        daq.ColorPicker(
            id='id-color-picker',
            label='unit type'
            ),

    ], style={'margin': 'auto'}),        
    dbc.ModalFooter([
        dbc.Button('Save', id='id-button-change-color', n_clicks=0, color='success'),
    ]),
],
    id='id-modal-change-color',
    is_open=True
)