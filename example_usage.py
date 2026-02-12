"""
Example usage of the Equipment Valuation Service
"""

from equipment_valuation_service import EquipmentValuationService

# Initialize the service
service = EquipmentValuationService("Book.json")

# Example 1: ID 87390, Model Year 2016 (from requirements)
print("Example 1: Classification ID 87390, Model Year 2016")
result = service.calculate_values("87390", 2016)
print(f"  Market Value (FMV): ${result['fmv']:,}")
print(f"  Auction Value (FLV): ${result['flv']:,}")
print(f"  Expected: FMV = $30,008, FLV = $20,426")
print()

# Example 2: ID 67352, Model Year 2016
print("Example 2: Classification ID 67352, Model Year 2016")
result = service.calculate_values("67352", 2016)
print(f"  Market Value (FMV): ${result['fmv']:,}")
print(f"  Auction Value (FLV): ${result['flv']:,}")
print()

# Example 3: Get equipment information
print("Example 3: Equipment Information for ID 87390")
info = service.get_equipment_info("87390")
if info:
    print(f"  Category: {info['category']}")
    print(f"  Subcategory: {info['subcategory']}")
    print(f"  Make: {info['make']}")
    print(f"  Model: {info['model']}")
