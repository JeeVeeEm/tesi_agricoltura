from dash import html
import dash_bootstrap_components as dbc

def create_header():
    """
    Crea il componente header della dashboard con titolo e descrizione
    """
    return html.Div([
        html.H1("Dashboard Analisi Azienda Settore Primario", className="mb-2"),
        html.P(
            """
            Strumento di analisi per monitorare e ottimizzare le prestazioni aziendali 
            nel settore agricolo, integrando dati ambientali, produttivi e finanziari.
            Questa dashboard permette di visualizzare indicatori chiave, analizzare trend
            e prendere decisioni strategiche basate sui dati.
            """,
            className="lead mb-4"
        )
    ], className="p-4 bg-light border-bottom")
