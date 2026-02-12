# Equipment Valuation Service

Calculate **Market (FMV)** and **Auction (FLV)** values for construction equipment from Classification ID and Model Year. Pure Python, standard library only—no build step or external dependencies.

---

## Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Data Format](#data-format)
- [Testing](#testing)
- [Deployment](#deployment)
- [Design Notes](#design-notes)

---

## Overview

**Formula:** `Value = Cost × Ratio`

- **Cost** (`bookCost`) is fixed per Classification ID.
- **Ratio** (depreciation schedule) depends on value type (FMV/FLV) and model year.

**Features:**

- FMV and FLV calculation with rounded dollar results
- Model year validation (2006–2020)
- Equipment metadata lookup by classification ID
- Clear `ValueError`/`FileNotFoundError` for invalid inputs
- No external dependencies (Python 3.6+)

---

## Quick Start

**Requirements:** Python 3.6+, no extra packages.

1. Ensure `Book.json` is in the project (or pass its path to the service).
2. Import and use:

```python
from equipment_valuation_service import EquipmentValuationService

service = EquipmentValuationService("Book.json")
result = service.calculate_values("87390", 2016)
# {"fmv": 30008, "flv": 20426}
```

Run the example script:

```bash
python example_usage.py
```

---

## Usage

### Calculate FMV/FLV

```python
service = EquipmentValuationService("Book.json")
result = service.calculate_values("87390", 2016)

print(f"Market (FMV): ${result['fmv']:,}")   # $30,008
print(f"Auction (FLV): ${result['flv']:,}")  # $20,426
```

| Parameter           | Type | Notes                    |
|--------------------|------|--------------------------|
| `classification_id`| str  | e.g. `"87390"`           |
| `model_year`       | int  | 2006–2020                |

### Equipment metadata

```python
info = service.get_equipment_info("87390")
if info:
    print(info["category"], info["subcategory"], info["make"], info["model"])
```

### Error handling

Invalid inputs raise `ValueError` with clear messages:

```python
try:
    service.calculate_values("87390", 2021)  # year out of range
except ValueError as e:
    print(e)  # Model year must be between 2006 and 2020, got 2021
```

- **Invalid model year** → must be 2006–2020  
- **Unknown classification ID** → not in data  
- **Missing file** → `FileNotFoundError` for bad data path  

---

## API Reference

### `EquipmentValuationService(data_file: str = "Book.json")`

Loads equipment data from the given JSON path. Use this path in your environment (e.g. `"Book.json"` next to the script).

### `calculate_values(classification_id: str, model_year: int) -> Dict[str, float]`

Returns `{"fmv": <int>, "flv": <int>}` (rounded to nearest dollar).

**Raises:** `ValueError` for invalid year or unknown ID; `FileNotFoundError` if the data file is missing.

### `get_equipment_info(classification_id: str) -> Optional[Dict]`

Returns a dict with `category`, `subcategory`, `make`, `model`, or `None` if the ID is not found.

---

## Data Format

JSON keyed by classification ID:

```json
{
  "CLASSIFICATION_ID": {
    "schedule": {
      "years": {
        "YEAR": { "fmv": RATIO, "flv": RATIO }
      }
    },
    "baseValue": { "bookCost": COST },
    "classification": {
      "category": "...",
      "subcategory": "...",
      "make": "...",
      "model": "..."
    }
  }
}
```

---

## Testing

```bash
python -m pytest test_equipment_valuation_service.py -v
```

Or with unittest:

```bash
python test_equipment_valuation_service.py
```

Coverage includes: valid calculations, min/max year boundaries, invalid inputs, type checks, rounding, and all years 2006–2020.

---

## Deployment

- **As a library:** Ship `equipment_valuation_service.py` and your data file (e.g. `Book.json`); import and instantiate with the data path.
- **As a script:** Run from the project directory (e.g. `python example_usage.py`).
- **Over HTTP:** Use a thin wrapper (Flask, FastAPI, etc.) in your own project; this module has no server.

Optional virtual environment:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
```

---

## Design Notes

- **Service class:** One place for loading data and running valuations; callers use the service, not raw JSON or formulas.
- **Constructor injection:** Data file path is passed in `__init__`; no hard-coded paths for testability and reuse.
- **Validation:** Model year and classification ID are validated before calculation; invalid input raises `ValueError` with clear messages.
- **Constants:** `MIN_MODEL_YEAR` / `MAX_MODEL_YEAR` centralize the valid year range.
- **Single responsibility:** Valuation and metadata only; no HTTP, logging, or extra I/O—handled by the caller or another layer.
