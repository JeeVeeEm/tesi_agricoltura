import sys
import os

# Aggiungi la directory 'src' al percorso di Python
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
sys.path.append(src_dir)

import dash
import dash_bootstrap_components as dbc
from dash import html
from dashboard.components.headers import create_header
from dashboard.components.control_panel import create_control_panel
from dashboard.components.kpi_section import create_kpi_section
from dashboard.components.tabs import create_tabs
from dashboard.callbacks import register_callbacks

# Inizializzazione dell'app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)
server = app.server

# Layout dell'app
app.layout = html.Div([
    create_header(),
    html.Div([
        dbc.Row([
            dbc.Col(create_control_panel(), md=3),
            dbc.Col([
                create_kpi_section(),
                create_tabs()
            ], md=9)
        ])
    ], className="container-fluid p-4")
])

# Registrazione dei callback
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
