import unittest
import sys
import os

# Aggiungi la directory src al path (sola riga necessaria)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from simulator.environmental import EnvironmentalDataGenerator
from simulator.production import AgriculturalProductionGenerator

class TestAgriculturalProductionGenerator(unittest.TestCase):
    def setUp(self):
        env_gen = EnvironmentalDataGenerator(
            location='TestFarm',
            start_date='2024-01-01',
            end_date='2024-01-10'
        )
        self.env_data = env_gen.generate()
        self.prod_gen = AgriculturalProductionGenerator(
            environmental_data=self.env_data,
            crop_type='grano',
            farm_size=100
        )
        self.prod_data = self.prod_gen.simulate()

    def test_output_shape(self):
        self.assertEqual(self.prod_data.shape[0], self.env_data.shape[0])

    def test_yield_positive(self):
        self.assertTrue((self.prod_data['yield'] >= 0).all())

    def test_profit_column(self):
        self.assertIn('profit', self.prod_data.columns)

if __name__ == '__main__':
    unittest.main()
