#!/usr/bin/env python3
"""
Test script untuk memverifikasi data PT. Sanghiang Perkasa
"""

from pt_sanghiang_data import PTSanghiangDataProcessor

def test_pt_sanghiang_data():
    """Test data PT. Sanghiang Perkasa"""
    print("🧪 Testing PT. Sanghiang Perkasa Data...")
    
    # Initialize processor
    processor = PTSanghiangDataProcessor()
    
    # Test routes data
    print(f"\n📊 Total routes loaded: {len(processor.routes_data)}")
    for route in processor.routes_data:
        print(f"   - {route.branch_code}: {route.route_name} ({route.distance_km}km)")
    
    # Test optimization data
    print(f"\n🔍 Testing optimization data (Jabodetabek only)...")
    optimization_data = processor.get_optimization_data(jabodetabek_only=True)
    print(f"   Found {len(optimization_data)} routes")
    
    for route in optimization_data:
        print(f"   - {route['route_id']}: {route['route_name']} -> {route['location']['name']}")
        print(f"     Capacity: {route['capacity']}kg, Load: {route['current_load']}kg")
        print(f"     Distance: {route['distance_km']}km, Utilization: {route['utilization_percent']}%")
    
    # Test statistics
    print(f"\n📈 Testing statistics...")
    stats = processor.get_route_statistics(jabodetabek_only=True)
    print(f"   Statistics: {stats}")
    
    # Test vehicle types
    print(f"\n🚛 Testing vehicle types...")
    vehicle_types = processor.get_vehicle_types()
    for vtype, vdata in vehicle_types.items():
        print(f"   - {vtype}: {vdata['description']} ({len(vdata['routes'])} routes)")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    test_pt_sanghiang_data() 