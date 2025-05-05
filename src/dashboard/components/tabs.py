from dash import html, dcc
import dash_bootstrap_components as dbc

def create_tabs():
    """
    Crea il sistema di schede per visualizzare diverse categorie di dati
    """
    return dbc.Card([
        dbc.CardHeader(
            dbc.Tabs([
                dbc.Tab(label="Dati Ambientali", tab_id="tab-environmental"),
                dbc.Tab(label="Produzione", tab_id="tab-production"),
                dbc.Tab(label="Finanziario", tab_id="tab-financial"),
                dbc.Tab(label="Previsioni", tab_id="tab-forecast")
            ], id="card-tabs", active_tab="tab-environmental")
        ),
        dbc.CardBody(html.Div(id="tab-content", className="p-3"))
    ], className="shadow")
