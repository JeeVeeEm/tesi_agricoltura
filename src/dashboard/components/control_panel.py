from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date

def create_control_panel():
    """
    Crea il pannello di controllo con i filtri interattivi
    """
    return dbc.Card([
        dbc.CardHeader(html.H4("Pannello di Controllo")),
        dbc.CardBody([
            html.H5("Intervallo Date", className="mt-2"),
            dcc.DatePickerRange(
                id='date-range-picker',
                min_date_allowed=date(2024, 1, 1),
                max_date_allowed=date(2024, 12, 31),
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31),
                display_format='DD/MM/YYYY',
                calendar_orientation='horizontal',
                clearable=True,
                with_portal=False,
                className="w-100 mb-3"
            ),
            
            html.H5("Tipo di Coltura", className="mt-4"),
            dcc.Dropdown(
                id='crop-type-dropdown',
                options=[
                    {'label': 'Grano', 'value': 'grano'},
                    {'label': 'Mais', 'value': 'mais'},
                    {'label': 'Soia', 'value': 'soia'},
                    {'label': 'Orzo', 'value': 'orzo'},
                    {'label': 'Girasole', 'value': 'girasole'}
                ],
                value='grano',
                clearable=False,
                className="mb-3"
            ),
            
            html.H5("Dimensione Azienda (ettari)", className="mt-4"),
            dcc.Input(
                id='farm-size-input',
                type='number',
                min=1,
                max=1000,
                step=1,
                value=100,
                className="form-control mb-3"
            ),
            
            dbc.Button(
                "Aggiorna Dashboard", 
                id="update-button", 
                color="primary", 
                className="mt-4 w-100"
            )
        ])
    ], className="mb-4 shadow")
