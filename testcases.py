import unittest
import os
from pro1 import island_species_average, flipper_length_trend , penguin_pullinfo, bill_average_length, bill_average_depth  

 
class TestPenguinsJoey(unittest.TestCase):

    def test_avg_general_case1(self):
        data = [
            {"species": "Adelie", "body_mass_g": "3500", "sex": "female"},
            {"species": "Adelie", "body_mass_g": "4300", "sex": "male"}
        ]
        result = island_species_average(data)
        self.assertEqual(result["Adelie"]["female"], 3500)
        self.assertEqual(result["Adelie"]["male"], 4300)
        self.assertEqual(result["Adelie"]["average"], 3900)

    def test_avg_general_case2(self):
        data = [
            {"species": "Adelie", "body_mass_g": "3500", "sex": "female"},
            {"species": "Gentoo", "body_mass_g": "6000", "sex": "male"}
        ]
        result = island_species_average(data)
        self.assertIn("Adelie", result)
        self.assertIn("Gentoo", result)
        self.assertEqual(result["Gentoo"]["male"], 6000)
        self.assertEqual(result["Gentoo"]["average"], 6000)

    def test_avg_edge_case1(self):
        data = [
            {"species": "Adelie", "body_mass_g": "4000", "sex": "male"},
            {"species": "Adelie", "body_mass_g": "4200", "sex": "male"}
        ]
        result = island_species_average(data)
        self.assertEqual(result["Adelie"]["female"], 0)
        self.assertEqual(result["Adelie"]["male"], 4100)
        self.assertEqual(result["Adelie"]["average"], 4100)

    def test_avg_edge_case2(self):
        data = []
        result = island_species_average(data)
        self.assertEqual(result, {})

    