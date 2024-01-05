import dash_bootstrap_components as dbc


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
    is_open=True
)
