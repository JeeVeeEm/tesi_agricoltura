from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
PRICE_MAP = {
    'grano': 230,
    'soia': 510,
    'orzo': 215,
    'girasole': 420,
    'mais': 200
}
BASE_VAR_COST_MAP = {
    'grano': 800,
    'soia': 900,
    'orzo': 750,
    'girasole': 850,
    'mais': 1000
}
from simulator.environmental import EnvironmentalDataGenerator
from simulator.production import AgriculturalProductionGenerator
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import html, dcc

def register_callbacks(app):
    
    @app.callback(
        Output("tab-content", "children"),
        [Input("card-tabs", "active_tab"),
         Input("update-button", "n_clicks")],
        [State("date-range-picker", "start_date"),
         State("date-range-picker", "end_date"),
         State("crop-type-dropdown", "value"),
         State("farm-size-input", "value")]
    )
    def render_tab_content(active_tab, n_clicks, start_date, end_date, crop_type, farm_size):
        # Conversione delle date
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
            
        # Genera i dati
        env_gen = EnvironmentalDataGenerator('Azienda Agricola', start_date, end_date)
        env_data = env_gen.generate()
        prod_gen = AgriculturalProductionGenerator(env_data, crop_type, farm_size)
        prod_data = prod_gen.simulate()
        
        # Prezzo di vendita per la coltura selezionata
        price_per_ton = PRICE_MAP.get(crop_type, 250)
        if crop_type not in PRICE_MAP:
            print(f"[WARN] Prezzo non definito per {crop_type}. Uso 250 €/t di default.")

        business_fixed_cost = 15000
        land_rent_per_ha = 300
        land_rent = land_rent_per_ha * farm_size
        base_var_cost = BASE_VAR_COST_MAP.get(crop_type, 800)
        variable_cost_per_ha = max(
            base_var_cost / (1 + 0.4 * np.log1p(farm_size)),
            0.5 * base_var_cost
        )
        variable_cost = variable_cost_per_ha * farm_size
        total_cost = business_fixed_cost + land_rent + variable_cost
        base_daily_cost = total_cost / len(env_data)
        daily_cost_series = base_daily_cost * (
            1 + np.random.normal(loc=0, scale=0.1, size=len(env_data))
        )
        financial_data = pd.DataFrame({
            'date': env_data['date'],
            'revenue': prod_data['yield'] * price_per_ton,
            'costs': daily_cost_series,
            'profit': (prod_data['yield'] * price_per_ton) - daily_cost_series,
        })
        
        # Crea il contenuto in base alla scheda attiva
        if active_tab == "tab-environmental":
            return [
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='temp-graph',
                        figure=px.line(env_data, x='date', y='temperature', title='Temperatura Giornaliera')
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='hum-graph',
                        figure=px.line(env_data, x='date', y='humidity', title='Umidità Giornaliera')
                    ), md=6)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='prec-graph',
                        figure=px.line(env_data, x='date', y='precipitation', title='Precipitazioni Giornaliere')
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='solar-graph',
                        figure = px.line(env_data, x='date', y='solar_radiation', title='Radiazione Solare Giornaliera')
                    ), md=6)
                ])
            ]
        
        elif active_tab == "tab-production":
            return [
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='yield-graph',
                        figure=px.line(prod_data, x='date', y='yield', title=f'Resa Giornaliera di {crop_type.capitalize()}')
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='yield-temp-graph',
                        figure=px.scatter(pd.merge(prod_data, env_data, on='date'), 
                                         x='temperature_x', y='yield', title='Correlazione Temperatura-Resa',
                                         trendline='ols')
                    ), md=6)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='yield-cum-graph',
                        figure=px.area(prod_data.assign(cum_yield=prod_data['yield'].cumsum()), 
                                       x='date', y='cum_yield', title='Resa Cumulativa')
                    ), md=12)
                ])
            ]
        
        elif active_tab == "tab-financial":
            return [
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='revenue-graph',
                        figure=px.line(financial_data, x='date', y='revenue', title='Ricavi Giornalieri')
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='costs-graph',
                        figure=px.line(financial_data, x='date', y='costs', title='Costi Giornalieri')
                    ), md=6)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='profit-graph',
                        figure=px.line(financial_data, x='date', y='profit', title='Profitto Giornaliero')
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='profit-pie-graph',
                        figure=px.pie(
                            names=['Ricavi', 'Costi'], 
                            values=[financial_data['revenue'].sum(), financial_data['costs'].sum()],
                            title='Ripartizione Finanziaria'
                        )
                    ), md=6)
                ])
            ]
        
        elif active_tab == "tab-forecast":
            mean_yield = prod_data['yield'].mean()
            mean_profit = financial_data['profit'].mean()
            mean_cost = financial_data['costs'].mean()

            scenario_labels = ['Pessimistico', 'Neutro', 'Ottimistico']
            yield_mult   = np.array([0.8, 1.0, 1.2])
            profit_mult  = np.array([0.7, 1.0, 1.3])
            cost_mult    = np.array([1.2, 1.0, 0.9])

            scenario_yield  = mean_yield  * yield_mult
            scenario_profit = mean_profit * profit_mult
            scenario_costs  = mean_cost   * cost_mult
            scenario_roi    = (scenario_profit / total_cost) * 100  # ROI %

            forecast_data = pd.DataFrame({
                'scenario': scenario_labels * 4,
                'metrica':  ['Resa']*3 + ['Profitto']*3 + ['Costi']*3 + ['ROI']*3,
                'valore':   list(scenario_yield) + list(scenario_profit) + list(scenario_costs) + list(scenario_roi)
            })
            
            return [
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='forecast-yield-graph',
                        figure=px.bar(
                            forecast_data[forecast_data['metrica'] == 'Resa'], 
                            x='scenario', y='valore', title='Previsione Resa',
                            color='scenario', barmode='group'
                        )
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='forecast-profit-graph',
                        figure=px.bar(
                            forecast_data[forecast_data['metrica'] == 'Profitto'], 
                            x='scenario', y='valore', title='Previsione Profitto',
                            color='scenario', barmode='group'
                        )
                    ), md=6)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='forecast-costs-graph',
                        figure=px.bar(
                            forecast_data[forecast_data['metrica'] == 'Costi'], 
                            x='scenario', y='valore', title='Previsione Costi',
                            color='scenario', barmode='group'
                        )
                    ), md=6),
                    dbc.Col(dcc.Graph(
                        id='forecast-roi-graph',
                        figure=px.bar(
                            forecast_data[forecast_data['metrica'] == 'ROI'], 
                            x='scenario', y='valore', title='Previsione ROI',
                            color='scenario', barmode='group'
                        )
                    ), md=6)
                ])
            ]
    
    @app.callback(
        Output("kpi-row", "children"),
        [Input("update-button", "n_clicks")],
        [State("date-range-picker", "start_date"),
         State("date-range-picker", "end_date"),
         State("crop-type-dropdown", "value"),
         State("farm-size-input", "value")]
    )
    def update_kpi_cards(n_clicks, start_date, end_date, crop_type, farm_size):
        from dashboard.components.kpi_section import create_kpi_card
        from dash import html
        import dash_bootstrap_components as dbc

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")

        env_gen = EnvironmentalDataGenerator('Azienda Agricola', start_date, end_date)
        env_data = env_gen.generate()
        prod_gen = AgriculturalProductionGenerator(env_data, crop_type, farm_size)
        prod_data = prod_gen.simulate()

        price_per_ton = PRICE_MAP.get(crop_type, 250)
        if crop_type not in PRICE_MAP:
            print(f"[WARN] Prezzo non definito per {crop_type}. Uso 250 €/t di default.")

        business_fixed_cost = 15000
        land_rent_per_ha = 300
        land_rent = land_rent_per_ha * farm_size
        base_var_cost = BASE_VAR_COST_MAP.get(crop_type, 800)
        variable_cost_per_ha = max(
            base_var_cost / (1 + 0.4 * np.log1p(farm_size)),
            0.5 * base_var_cost
        )
        variable_cost = variable_cost_per_ha * farm_size
        total_cost = business_fixed_cost + land_rent + variable_cost
        base_daily_cost = total_cost / len(env_data)
        daily_cost_series = base_daily_cost * (
            1 + np.random.normal(loc=0, scale=0.1, size=len(env_data))
        )
        financial_data = pd.DataFrame({
            'date': env_data['date'],
            'revenue': prod_data['yield'] * price_per_ton,
            'costs': daily_cost_series,
            'profit': (prod_data['yield'] * price_per_ton) - daily_cost_series,
        })

        total_yield = prod_data['yield'].sum()
        potential_yield = prod_gen.crop_parameters[crop_type]['base_yield'] * farm_size
        efficiency_val = (total_yield / potential_yield) * 100 if potential_yield else 0
        total_costs = financial_data['costs'].sum()
        total_profit = financial_data['profit'].sum()

        if len(prod_data) >= 14:
            production_last_week = prod_data.iloc[-7:]['yield'].sum()
            production_prev_week = prod_data.iloc[-14:-7]['yield'].sum()
            production_trend = (
                (production_last_week - production_prev_week) / production_prev_week * 100
                if production_prev_week else 0
            )
        else:
            production_trend = 0

        if len(financial_data) >= 14:
            profit_last_week = financial_data.iloc[-7:]['profit'].sum()
            profit_prev_week = financial_data.iloc[-14:-7]['profit'].sum()
            profit_trend = (
                (profit_last_week - profit_prev_week) / abs(profit_prev_week) * 100
                if profit_prev_week else 0
            )

            costs_last_week = financial_data.iloc[-7:]['costs'].sum()
            costs_prev_week = financial_data.iloc[-14:-7]['costs'].sum()
            costs_trend = (
                (costs_last_week - costs_prev_week) / costs_prev_week * 100
                if costs_prev_week else 0
            )
        else:
            profit_trend = 0
            costs_trend = 0

        if len(prod_data) >= 14:
            efficiency_last_week = (
                production_last_week / (farm_size * prod_gen.crop_parameters[crop_type]['base_yield']) * 100
            )
            efficiency_prev_week = (
                production_prev_week / (farm_size * prod_gen.crop_parameters[crop_type]['base_yield']) * 100
            )
            efficiency_trend = (
                (efficiency_last_week - efficiency_prev_week) / efficiency_prev_week * 100
                if efficiency_prev_week else 0
            )
        else:
            efficiency_trend = 0

        production_str = f"{total_yield:,.1f} t"
        efficiency_str = f"{efficiency_val:.1f}%"
        costs_str = f"€ {int(total_costs):,}"
        profit_str = f"€ {int(total_profit):,}"

        return [
            dbc.Col(create_kpi_card("Produzione", production_str, production_trend, "bi-basket", production_trend >= 0), md=3),
            dbc.Col(create_kpi_card("Efficienza", efficiency_str, efficiency_trend, "bi-graph-up", efficiency_trend >= 0), md=3),
            dbc.Col(create_kpi_card("Costi", costs_str, costs_trend, "bi-currency-euro", costs_trend < 0), md=3),
            dbc.Col(create_kpi_card("Profitto", profit_str, profit_trend, "bi-piggy-bank", profit_trend >= 0), md=3)
        ]
