import numpy as np
import pandas as pd


class AgriculturalProductionGenerator:
    def __init__(self, environmental_data, crop_type, farm_size=100):
        """
        Parameters
        ----------
        environmental_data : pandas.DataFrame
            Must contain at least 'temperature' and 'precipitation' columns.
        crop_type : str
            One of the keys in self.crop_parameters (e.g. 'grano', 'mais', …).
        farm_size : float
            Size of the farm in hectares. Defaults to 100 ha.
        """
        self.environmental_data = environmental_data
        self.crop_type = crop_type
        self.farm_size = farm_size

        # Agronomic and economic parameters by crop
        self.crop_parameters = {
            "grano": {
                "optimal_temp": (15, 25),     # °C
                "growth_days": 180,
                "base_yield": 7.0,            # t / ha under ideal conditions
                "water_requirement": 4.5,     # mm of rain per day
                "price_per_ton": 250,         # €/t
                "cost_per_hectare": 1000,     # €/ha
                "planting_months": [10, 11, 12]
            },
            "soia": {
                "optimal_temp": (20, 30),
                "growth_days": 150,
                "base_yield": 3.2,
                "water_requirement": 5.0,
                "price_per_ton": 500,
                "cost_per_hectare": 800,
                "planting_months": [4, 5]
            },
            "orzo": {
                "optimal_temp": (12, 22),
                "growth_days": 170,
                "base_yield": 6.5,
                "water_requirement": 4.2,
                "price_per_ton": 230,
                "cost_per_hectare": 900,
                "planting_months": [10, 11]
            },
            "girasole": {
                "optimal_temp": (18, 28),
                "growth_days": 130,
                "base_yield": 2.8,
                "water_requirement": 4.8,
                "price_per_ton": 400,
                "cost_per_hectare": 750,
                "planting_months": [3, 4, 5]
            },
            "mais": {                        #  ← newly added crop
                "optimal_temp": (18, 30),
                "growth_days": 150,
                "base_yield": 10.5,
                "water_requirement": 5.5,
                "price_per_ton": 210,
                "cost_per_hectare": 1100,
                "planting_months": [4, 5]
            }
        }

    def simulate(self) -> pd.DataFrame:
        """Return a dataframe with yield, revenue, cost and profit day‑by‑day."""
        df = self.environmental_data.copy()

        # Look up the selected crop’s parameters
        crop_params = self.crop_parameters[self.crop_type]
        optimal_temp_min, optimal_temp_max = crop_params["optimal_temp"]

        # Temperature response curve (triangle‑shaped)
        df["temp_factor"] = df["temperature"].apply(
            lambda t: 1.0
            if optimal_temp_min <= t <= optimal_temp_max
            else max(
                0,
                1
                - abs(t - (optimal_temp_min + optimal_temp_max) / 2)
                / ((optimal_temp_max - optimal_temp_min) / 2),
            )
        )

        # Water availability factor (precipitation relative to requirement)
        df["water_factor"] = np.clip(
            df["precipitation"] / crop_params["water_requirement"], 0, 1
        )

        # Combined growth factor
        df["growth_factor"] = df["temp_factor"] * df["water_factor"]

        # Daily yield for the whole farm (tons)
        df["yield"] = (
            crop_params["base_yield"] * df["growth_factor"] * self.farm_size / 100
        )

        # Economics
        df["revenue"] = df["yield"] * crop_params["price_per_ton"]
        df["cost"] = crop_params["cost_per_hectare"] * self.farm_size
        df["profit"] = df["revenue"] - df["cost"]

        return df