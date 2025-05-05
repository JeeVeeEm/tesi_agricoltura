import numpy as np
import pandas as pd

class EnvironmentalDataGenerator:
    def __init__(self, location, start_date, end_date, frequency='D'):
        self.location = location
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.frequency = frequency
        self.base_parameters = {
            'temperature': {
                1: (5, 3), 2: (7, 3), 3: (10, 4), 4: (15, 5), 5: (20, 5),
                6: (25, 4), 7: (28, 3), 8: (27, 3), 9: (22, 4), 10: (17, 5),
                11: (10, 4), 12: (6, 3)
            }
        }

    def generate(self):
        dates = pd.date_range(self.start_date, self.end_date, freq=self.frequency)
        temperatures = [np.random.normal(self.base_parameters['temperature'][date.month][0],
                                         self.base_parameters['temperature'][date.month][1]) for date in dates]
        humidity = np.random.uniform(40, 90, len(dates))
        precipitation = np.random.exponential(2, len(dates))
        solar_radiation = np.random.uniform(100, 300, len(dates))
        df = pd.DataFrame({
            'date': dates,
            'temperature': temperatures,
            'humidity': humidity,
            'precipitation': precipitation,
            'solar_radiation': solar_radiation
        })
        return df
