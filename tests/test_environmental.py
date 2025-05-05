import unittest
import sys
import os

# Aggiungi la directory src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulator.environmental import EnvironmentalDataGenerator

class TestEnvironmentalDataGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EnvironmentalDataGenerator(
            location='TestFarm',
            start_date='2024-01-01',
            end_date='2024-01-10'
        )
        self.data = self.generator.generate()

    def test_dataframe_shape(self):
        # Controlla che il dataframe abbia 10 righe (dal 1 al 10 gennaio)
        self.assertEqual(self.data.shape[0], 10)

    def test_columns_exist(self):
        # Controlla che tutte le colonne siano presenti
        for col in ['date', 'temperature', 'humidity', 'precipitation', 'solar_radiation']:
            self.assertIn(col, self.data.columns)

    def test_temperature_range(self):
        # Controlla che la temperatura sia un numero reale
        self.assertTrue(self.data['temperature'].dtype.kind in 'fi')

if __name__ == '__main__':
    unittest.main()
