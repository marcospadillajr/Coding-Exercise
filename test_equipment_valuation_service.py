"""
Unit tests for Equipment Valuation Service
"""

import unittest
import json
import os
import tempfile
from equipment_valuation_service import EquipmentValuationService


class TestEquipmentValuationService(unittest.TestCase):
    """Test cases for EquipmentValuationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary JSON file with test data
        self.test_data = {
            "67352": {
                "schedule": {
                    "years": {
                        "2020": {"fmv": 1.425079, "flv": 0.548166},
                        "2019": {"fmv": 1.317403, "flv": 0.506748},
                        "2018": {"fmv": 1.217864, "flv": 0.468459},
                        "2017": {"fmv": 0.984058, "flv": 0.353885},
                        "2016": {"fmv": 0.955396, "flv": 0.339840},
                        "2015": {"fmv": 0.740176, "flv": 0.234374},
                        "2014": {"fmv": 0.718617, "flv": 0.227547},
                        "2013": {"fmv": 0.623239, "flv": 0.220245},
                        "2012": {"fmv": 0.431321, "flv": 0.213178},
                        "2011": {"fmv": 0.374074, "flv": 0.206337},
                        "2010": {"fmv": 0.363179, "flv": 0.198498},
                        "2009": {"fmv": 0.330725, "flv": 0.192716},
                        "2008": {"fmv": 0.324111, "flv": 0.188862},
                        "2007": {"fmv": 0.317628, "flv": 0.185085},
                        "2006": {"fmv": 0.311276, "flv": 0.181383}
                    }
                },
                "baseValue": {
                    "bookCost": 681252,
                    "retailSaleCount": 122,
                    "auctionSaleCount": 17
                },
                "classification": {
                    "category": "Earthmoving Equipment",
                    "subcategory": "Dozers",
                    "make": "Caterpillar",
                    "model": "D8T"
                }
            },
            "87390": {
                "schedule": {
                    "years": {
                        "2020": {"fmv": 1.106366, "flv": 0.772935},
                        "2019": {"fmv": 1.041526, "flv": 0.727636},
                        "2018": {"fmv": 0.980485, "flv": 0.684991},
                        "2017": {"fmv": 0.692965, "flv": 0.473205},
                        "2016": {"fmv": 0.613292, "flv": 0.417468},
                        "2015": {"fmv": 0.474556, "flv": 0.318204},
                        "2014": {"fmv": 0.448658, "flv": 0.237055},
                        "2013": {"fmv": 0.353526, "flv": 0.208517},
                        "2012": {"fmv": 0.343229, "flv": 0.188052},
                        "2011": {"fmv": 0.251370, "flv": 0.138759},
                        "2010": {"fmv": 0.234682, "flv": 0.124357},
                        "2009": {"fmv": 0.204723, "flv": 0.120735},
                        "2008": {"fmv": 0.192439, "flv": 0.113491},
                        "2007": {"fmv": 0.180893, "flv": 0.106681},
                        "2006": {"fmv": 0.170039, "flv": 0.100280}
                    }
                },
                "baseValue": {
                    "bookCost": 48929,
                    "retailSaleCount": 12,
                    "auctionSaleCount": 127
                },
                "classification": {
                    "category": "Aerial Equipment",
                    "subcategory": "Boom Lifts",
                    "make": "JLG",
                    "model": "340AJ"
                }
            }
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        
        # Initialize service with test data
        self.service = EquipmentValuationService(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_calculate_values_example_87390_2016(self):
        """Test the example case: ID 87390, Model Year 2016."""
        result = self.service.calculate_values("87390", 2016)
        
        # Expected: FMV = 48929 * 0.613292 = 30,007.68 ≈ 30,008
        # Expected: FLV = 48929 * 0.417468 = 20,426.18 ≈ 20,426
        self.assertEqual(result["fmv"], 30008)
        self.assertEqual(result["flv"], 20426)
    
    def test_calculate_values_67352_2016(self):
        """Test calculation for ID 67352, Model Year 2016."""
        result = self.service.calculate_values("67352", 2016)
        
        # Expected: FMV = 681252 * 0.955396 = 650,865.18 ≈ 650,865
        # Expected: FLV = 681252 * 0.339840 = 231,517.19 ≈ 231,517
        self.assertEqual(result["fmv"], 650865)
        self.assertEqual(result["flv"], 231517)
    
    def test_calculate_values_min_year_2006(self):
        """Test calculation with minimum valid model year (2006)."""
        result = self.service.calculate_values("87390", 2006)
        self.assertIn("fmv", result)
        self.assertIn("flv", result)
        self.assertIsInstance(result["fmv"], int)
        self.assertIsInstance(result["flv"], int)
    
    def test_calculate_values_max_year_2020(self):
        """Test calculation with maximum valid model year (2020)."""
        result = self.service.calculate_values("87390", 2020)
        self.assertIn("fmv", result)
        self.assertIn("flv", result)
        self.assertIsInstance(result["fmv"], int)
        self.assertIsInstance(result["flv"], int)
    
    def test_calculate_values_middle_year(self):
        """Test calculation with a middle year."""
        result = self.service.calculate_values("87390", 2013)
        self.assertIn("fmv", result)
        self.assertIn("flv", result)
        # Verify values are positive
        self.assertGreater(result["fmv"], 0)
        self.assertGreater(result["flv"], 0)
    
    def test_calculate_values_with_string_id(self):
        """Test that string classification ID works."""
        result = self.service.calculate_values("87390", 2016)
        self.assertEqual(result["fmv"], 30008)
        self.assertEqual(result["flv"], 20426)
    
    def test_calculate_values_with_numeric_id(self):
        """Test that numeric classification ID is converted to string."""
        result = self.service.calculate_values(87390, 2016)
        self.assertEqual(result["fmv"], 30008)
        self.assertEqual(result["flv"], 20426)
    
    def test_invalid_model_year_below_minimum(self):
        """Test error handling for model year below 2006."""
        with self.assertRaises(ValueError) as context:
            self.service.calculate_values("87390", 2005)
        
        self.assertIn("Model year must be between 2006 and 2020", str(context.exception))
    
    def test_invalid_model_year_above_maximum(self):
        """Test error handling for model year above 2020."""
        with self.assertRaises(ValueError) as context:
            self.service.calculate_values("87390", 2021)
        
        self.assertIn("Model year must be between 2006 and 2020", str(context.exception))
    
    def test_invalid_classification_id(self):
        """Test error handling for non-existent classification ID."""
        with self.assertRaises(ValueError) as context:
            self.service.calculate_values("99999", 2016)
        
        self.assertIn("Classification ID '99999' not found", str(context.exception))
    
    def test_invalid_model_year_type(self):
        """Test error handling for non-integer model year."""
        with self.assertRaises(ValueError) as context:
            self.service.calculate_values("87390", "2016")
        
        self.assertIn("Model year must be an integer", str(context.exception))
    
    def test_file_not_found(self):
        """Test error handling when data file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            EquipmentValuationService("nonexistent.json")
    
    def test_get_equipment_info_valid_id(self):
        """Test getting equipment information for valid ID."""
        info = self.service.get_equipment_info("87390")
        self.assertIsNotNone(info)
        self.assertEqual(info["category"], "Aerial Equipment")
        self.assertEqual(info["subcategory"], "Boom Lifts")
        self.assertEqual(info["make"], "JLG")
        self.assertEqual(info["model"], "340AJ")
    
    def test_get_equipment_info_invalid_id(self):
        """Test getting equipment information for invalid ID."""
        info = self.service.get_equipment_info("99999")
        self.assertIsNone(info)
    
    def test_values_are_rounded(self):
        """Test that returned values are rounded to integers."""
        result = self.service.calculate_values("87390", 2016)
        self.assertIsInstance(result["fmv"], int)
        self.assertIsInstance(result["flv"], int)
        # Verify rounding (should not have decimal places)
        self.assertEqual(result["fmv"], int(result["fmv"]))
        self.assertEqual(result["flv"], int(result["flv"]))
    
    def test_all_years_in_range(self):
        """Test that all valid years (2006-2020) work correctly."""
        for year in range(2006, 2021):
            result = self.service.calculate_values("87390", year)
            self.assertIn("fmv", result)
            self.assertIn("flv", result)
            self.assertGreater(result["fmv"], 0)
            self.assertGreater(result["flv"], 0)


if __name__ == '__main__':
    unittest.main()
