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

    # --- Flipper trend tests ---
    def test_flipper_general_case1(self):
        data = [
            {"species": "Adelie", "flipper_length_mm": "180", "year": "2007"},
            {"species": "Adelie", "flipper_length_mm": "190", "year": "2008"}
        ]
        result = flipper_length_trend(data)
        self.assertEqual(result["Adelie"][2007], 180)
        self.assertEqual(result["Adelie"][2008], 190)

    def test_flipper_general_case2(self):
        data = [
            {"species": "Adelie", "flipper_length_mm": "180", "year": "2007"},
            {"species": "Gentoo", "flipper_length_mm": "230", "year": "2007"}
        ]
        result = flipper_length_trend(data)
        self.assertEqual(result["Adelie"][2007], 180)
        self.assertEqual(result["Gentoo"][2007], 230)

    def test_flipper_edge_case1(self):
        data = [
            {"species": "Adelie", "flipper_length_mm": "", "year": "2007"},
            {"species": "Adelie", "flipper_length_mm": "", "year": "2008"}
        ]
        result = flipper_length_trend(data)
        self.assertEqual(result, {"Adelie": {}})

    def test_flipper_edge_case2(self):
        data = []
        result = flipper_length_trend(data)
        self.assertEqual(result, {})



#andrew's test cases 
# -----------------------------

class TestPenguinAveragesAndrew(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rows = penguin_pullinfo("test.csv")
        print(f"[tests] loaded {len(cls.rows)} rows from test.csv")

    def _expected_avg(self, rows, species, island, column_key):
        total = 0.0
        count = 0
        for r in rows:
            if r["species"] == species and r["island"] == island:
                v = str(r[column_key]).strip()
                if v != "NA" and v != "":
                    total += float(v)
                    count += 1
        if count == 0:
            return None, 0
        return total / count, count

    # --- Bill length tests ---
    def test_bill_average_length_general_adelie_torgersen(self):
        out = bill_average_length(self.rows, "Adelie", "Torgersen")[0]
        exp_avg, exp_cnt = self._expected_avg(self.rows, "Adelie", "Torgersen", "bill_length_mm")
        if exp_avg is None:
            self.assertEqual(out["average_bill_length"], None)
        else:
            self.assertEqual(round(out["average_bill_length"], 6), round(exp_avg, 6))
        self.assertEqual(out["count"], exp_cnt)

    def test_bill_average_length_general_gentoo_biscoe(self):
        out = bill_average_length(self.rows, "Gentoo", "Biscoe")[0]
        exp_avg, exp_cnt = self._expected_avg(self.rows, "Gentoo", "Biscoe", "bill_length_mm")
        if exp_avg is None:
            self.assertEqual(out["average_bill_length"], None)
        else:
            self.assertEqual(round(out["average_bill_length"], 6), round(exp_avg, 6))
        self.assertEqual(out["count"], exp_cnt)

    def test_bill_average_length_edge_no_pair(self):
        out = bill_average_length(self.rows, "Chinstrap", "Biscoe")[0]
        self.assertEqual(out["average_bill_length"], None)
        self.assertEqual(out["count"], 0)

    def test_bill_average_length_edge_case_sensitivity(self):
        out = bill_average_length(self.rows, "Adelie", "torgersen")[0]
        self.assertEqual(out["average_bill_length"], None)
        self.assertEqual(out["count"], 0)

    # --- Bill depth tests ---
    def test_bill_average_depth_general_adelie_torgersen(self):
        out = bill_average_depth(self.rows, "Adelie", "Torgersen")[0]
        exp_avg, exp_cnt = self._expected_avg(self.rows, "Adelie", "Torgersen", "bill_depth_mm")
        if exp_avg is None:
            self.assertEqual(out["average_bill_depth"], None)
        else:
            self.assertEqual(round(out["average_bill_depth"], 6), round(exp_avg, 6))
        self.assertEqual(out["count"], exp_cnt)

    def test_bill_average_depth_general_gentoo_biscoe(self):
        out = bill_average_depth(self.rows, "Gentoo", "Biscoe")[0]
        exp_avg, exp_cnt = self._expected_avg(self.rows, "Gentoo", "Biscoe", "bill_depth_mm")
        if exp_avg is None:
            self.assertEqual(out["average_bill_depth"], None)
        else:
            self.assertEqual(round(out["average_bill_depth"], 6), round(exp_avg, 6))
        self.assertEqual(out["count"], exp_cnt)

    


if __name__ == "__main__":
    unittest.main(verbosity=2)
