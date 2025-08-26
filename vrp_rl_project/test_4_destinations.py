#!/usr/bin/env python3
"""
Test 4 Destinations - Verifikasi bahwa semua 4 destinasi muncul
"""

from realistic_route_system import RealisticRouteSystem

def test_4_destinations():
    print("🧪 Testing 4 Destinations")
    print("=" * 40)
    
    route_system = RealisticRouteSystem()
    
    # Check destinations
    print(f"📋 Available destinations:")
    for key, dest in route_system.destinations.items():
        print(f"   - {key}: {dest['name']} at {dest['coordinates']}")
        print(f"     Route key: {dest['route_key']}")
    
    # Test get_all_routes
    print(f"\n📍 Testing get_all_routes:")
    all_routes = route_system.get_all_routes("sunny")
    print(f"   Generated {len(all_routes)} routes")
    
    for route in all_routes:
        print(f"   - {route.destination}: {route.total_distance_km:.1f} km")
        print(f"     Roads: {[s.road_name for s in route.road_segments]}")
        print(f"     Polyline points: {len(route.polyline)}")
    
    # Test individual routes
    print(f"\n🔍 Testing individual routes:")
    destinations = ["bogor", "tangerang", "jakarta", "bekasi"]
    
    for dest in destinations:
        try:
            route = route_system.get_optimal_route(dest, "sunny")
            print(f"   ✅ {dest.upper()}: {route.total_distance_km:.1f} km")
        except Exception as e:
            print(f"   ❌ {dest.upper()}: Error - {e}")
    
    print(f"\n🎯 Expected Results:")
    print(f"   - Should have 4 destinations: Bogor, Tangerang, Jakarta, Bekasi")
    print(f"   - All routes should have > 10 polyline points")
    print(f"   - All routes should have curved polylines")

if __name__ == "__main__":
    test_4_destinations() 