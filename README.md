# Equipment Valuation Service

A service for calculating Market (FMV) and Auction (FLV) values for construction equipment based on Classification ID and Model Year.

## Overview

This service determines the Retail (Market) and Auction values of construction equipment using the formula:

**Value = Cost × Ratio**

Where:
- **Cost** (bookCost) is static for a given Classification ID regardless of Model Year
- **Ratio** (Depreciation Schedule Percentage) varies for each Value Type (FMV/FLV) and Model Year

## Features

- Calculate Market (FMV) and Auction (FLV) values for equipment
- Validates Model Year range (2006-2020)
- Returns rounded dollar values
- Comprehensive error handling
- Full unit test coverage

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Usage

### Basic Example

```python
from equipment_valuation_service import EquipmentValuationService

# Initialize the service
service = EquipmentValuationService("Book.json")

# Calculate values for Classification ID 87390, Model Year 2016
result = service.calculate_values("87390", 2016)

print(f"Market Value (FMV): ${result['fmv']:,}")
print(f"Auction Value (FLV): ${result['flv']:,}")
# Output:
# Market Value (FMV): $30,008
# Auction Value (FLV): $20,426
```

### Example with Different ID

```python
service = EquipmentValuationService("Book.json")
result = service.calculate_values("67352", 2016)

print(f"FMV: ${result['fmv']:,}")
print(f"FLV: ${result['flv']:,}")
```

### Get Equipment Information

```python
service = EquipmentValuationService("Book.json")
info = service.get_equipment_info("87390")

if info:
    print(f"Category: {info['category']}")
    print(f"Subcategory: {info['subcategory']}")
    print(f"Make: {info['make']}")
    print(f"Model: {info['model']}")
```

## Error Handling

The service provides friendly error messages for invalid inputs:

- **Invalid Model Year**: Model year must be between 2006 and 2020
- **Invalid Classification ID**: Classification ID not found in equipment data
- **File Not Found**: Data file (Book.json) not found

### Example Error Handling

```python
try:
    result = service.calculate_values("87390", 2021)  # Invalid year
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Model year must be between 2006 and 2020, got 2021
```

## Running Tests

Run the unit tests using:

```bash
python -m pytest test_equipment_valuation_service.py -v
```

Or using unittest:

```bash
python test_equipment_valuation_service.py
```

## Test Coverage

The test suite includes:

-  Valid calculations for example cases
-  Boundary testing (min/max model years)
-  Error handling for invalid inputs
-  Type validation
-  Rounding verification
-  All years in valid range (2006-2020)

## Data Format

The service expects a JSON file with the following structure:

```json
{
  "CLASSIFICATION_ID": {
    "schedule": {
      "years": {
        "YEAR": {
          "fmv": RATIO,
          "flv": RATIO
        }
      }
    },
    "baseValue": {
      "bookCost": COST
    },
    "classification": {
      "category": "...",
      "subcategory": "...",
      "make": "...",
      "model": "..."
    }
  }
}
```

## API Reference

### `EquipmentValuationService`

#### `__init__(data_file: str = "Book.json")`
Initialize the service with equipment data.

**Parameters:**
- `data_file` (str): Path to the JSON file containing equipment data

#### `calculate_values(classification_id: str, model_year: int) -> Dict[str, float]`
Calculate Market (FMV) and Auction (FLV) values.

**Parameters:**
- `classification_id` (str): The Classification ID
- `model_year` (int): The Model Year (2006-2020)

**Returns:**
- Dictionary with `fmv` (Market Value) and `flv` (Auction Value) rounded to nearest dollar

**Raises:**
- `ValueError`: If classification_id is not found or model_year is invalid
- `FileNotFoundError`: If data file is not found

#### `get_equipment_info(classification_id: str) -> Optional[Dict]`
Get equipment classification information.

**Parameters:**
- `classification_id` (str): The Classification ID

**Returns:**
- Dictionary with classification info or None if not found
