from dash import html
import dash_bootstrap_components as dbc

def create_kpi_card(title, value, change, icon, is_positive=True, period_label="vs 7 gg precedenti"):
    """
    Crea una scheda KPI con titolo, valore, variazione e icona.
    period_label : testo da mostrare accanto alla percentuale di variazione.
    """
    if isinstance(value, (int, float)):
        value_display = f"{value:,.2f}"
    else:
        value_display = value

    if isinstance(change, (int, float)):
        change_display = f"{change:.2f}"
    else:
        change_display = change

    change_color = "text-success" if is_positive else "text-danger"
    change_icon = "bi bi-caret-up-fill" if is_positive else "bi bi-caret-down-fill"
    border_class = "border-start border-5 " + ("border-success" if is_positive else "border-danger")
    
    return dbc.Card(
        dbc.CardBody([
            html.H4([html.I(className=f"bi {icon} me-2"), title], className="text-nowrap"),
            html.H2(value_display, className="my-2"),
            html.Div([
                html.I(f"{change_display}%", className=f"{change_icon} {change_color}"),
                f" {period_label}"
            ])
        ]),
        className=f"text-center m-2 shadow {border_class}"
    )

def create_kpi_section():
    """
    Crea il contenitore per le KPI cards senza valori hard‑coded.
    Le card verranno poi popolate dinamicamente dal callback `update_kpi_cards`.
    """
    return html.Div([
        dbc.Row(id="kpi-row", className="mb-4")
    ])
