"""
Equipment Valuation Service

This service calculates Market (FMV) and Auction (FLV) values for construction equipment
based on Classification ID and Model Year.

The calculation formula is: Value = Cost * Ratio
- Cost (bookCost) is static for a given Classification ID
- Ratio varies by Value Type (FMV/FLV) and Model Year
"""

import json
import os
from typing import Dict, Optional, Tuple


class EquipmentValuationService:
    """Service for calculating equipment market and auction values."""
    
    MIN_MODEL_YEAR = 2006
    MAX_MODEL_YEAR = 2020
    
    def __init__(self, data_file: str = "Book.json"):
        """
        Initialize the service with equipment data.
        
        Args:
            data_file: Path to the JSON file containing equipment data
        """
        self.data_file = data_file
        self.equipment_data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load equipment data from JSON file."""
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"Data file '{self.data_file}' not found.")
        
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _validate_model_year(self, model_year: int) -> None:
        """
        Validate that model year is within acceptable range.
        
        Args:
            model_year: The model year to validate
            
        Raises:
            ValueError: If model year is outside the valid range
        """
        if not isinstance(model_year, int):
            raise ValueError(f"Model year must be an integer, got {type(model_year).__name__}")
        
        if model_year < self.MIN_MODEL_YEAR or model_year > self.MAX_MODEL_YEAR:
            raise ValueError(
                f"Model year must be between {self.MIN_MODEL_YEAR} and {self.MAX_MODEL_YEAR}, "
                f"got {model_year}"
            )
    
    def _validate_classification_id(self, classification_id: str) -> None:
        """
        Validate that classification ID exists in the data.
        
        Args:
            classification_id: The classification ID to validate
            
        Raises:
            ValueError: If classification ID is not found
        """
        if classification_id not in self.equipment_data:
            raise ValueError(
                f"Classification ID '{classification_id}' not found in equipment data."
            )
    
    def calculate_values(self, classification_id: str, model_year: int) -> Dict[str, float]:
        """
        Calculate Market (FMV) and Auction (FLV) values for a given Classification ID and Model Year.
        
        Args:
            classification_id: The Classification ID (as string)
            model_year: The Model Year (must be between 2006 and 2020)
            
        Returns:
            Dictionary with 'fmv' (Market Value) and 'flv' (Auction Value) rounded to nearest dollar
            
        Raises:
            ValueError: If classification_id is not found or model_year is invalid
        """
        # Convert to string if needed
        classification_id = str(classification_id)
        
        # Validate inputs
        self._validate_model_year(model_year)
        self._validate_classification_id(classification_id)
        
        # Get equipment data
        equipment = self.equipment_data[classification_id]
        book_cost = equipment["baseValue"]["bookCost"]
        
        # Get ratios for the model year
        model_year_str = str(model_year)
        if model_year_str not in equipment["schedule"]["years"]:
            raise ValueError(
                f"Model year {model_year} not found in schedule for Classification ID {classification_id}"
            )
        
        year_data = equipment["schedule"]["years"][model_year_str]
        fmv_ratio = year_data["fmv"]
        flv_ratio = year_data["flv"]
        
        # Calculate values: Cost * Ratio
        fmv_value = book_cost * fmv_ratio
        flv_value = book_cost * flv_ratio
        
        # Round to nearest dollar
        return {
            "fmv": round(fmv_value),
            "flv": round(flv_value)
        }
    
    def get_equipment_info(self, classification_id: str) -> Optional[Dict]:
        """
        Get equipment classification information.
        
        Args:
            classification_id: The Classification ID
            
        Returns:
            Dictionary with classification info or None if not found
        """
        classification_id = str(classification_id)
        if classification_id in self.equipment_data:
            return self.equipment_data[classification_id].get("classification")
        return None
