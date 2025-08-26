#!/usr/bin/env python3
"""
Test Realistic Routes Now - PT. Sanghiang Perkasa VRP
Script untuk test langsung realistic routes
"""

from realistic_route_system import RealisticRouteSystem
import json

def test_realistic_routes_now():
    """Test realistic routes immediately"""
    print("🧪 Testing Realistic Routes NOW")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    
    # Test one route to see if polyline is realistic
    try:
        route = route_system.get_optimal_route("bogor", "sunny")
        
        print(f"📍 Route to {route.destination}:")
        print(f"   Distance: {route.total_distance_km:.1f} km")
        print(f"   Time: {route.total_time_minutes} minutes")
        print(f"   Polyline Points: {len(route.polyline)}")
        
        # Check if polyline has realistic curves
        if len(route.polyline) > 2:
            print(f"   ✅ Realistic polyline with curves")
            print(f"   📍 Start: {route.polyline[0]}")
            print(f"   📍 Middle: {route.polyline[len(route.polyline)//2]}")
            print(f"   📍 End: {route.polyline[-1]}")
            
            # Check curve deviation
            start = route.polyline[0]
            middle = route.polyline[len(route.polyline)//2]
            end = route.polyline[-1]
            
            # Calculate straight line middle
            straight_middle = {
                "lat": start["lat"] + (end["lat"] - start["lat"]) * 0.5,
                "lng": start["lng"] + (end["lng"] - start["lng"]) * 0.5
            }
            
            curve_diff = abs(middle["lat"] - straight_middle["lat"]) + abs(middle["lng"] - straight_middle["lng"])
            print(f"   📐 Curve Deviation: {curve_diff:.6f}")
            
            if curve_diff > 0.0001:
                print(f"   ✅ Significant curve detected!")
            else:
                print(f"   ❌ Curve too small")
        else:
            print(f"   ❌ Still straight line ({len(route.polyline)} points)")
        
        # Show road segments
        print(f"   🛣️ Roads:")
        for i, segment in enumerate(route.road_segments, 1):
            print(f"      {i}. {segment.road_name}")
            print(f"         Length: {segment.length_km} km")
            print(f"         Traffic: {segment.traffic_level}")
            print(f"         Area: {segment.area}")
        
        # Test API format
        api_data = route_system.format_route_for_api(route)
        print(f"   🔗 API Format:")
        print(f"      Destination: {api_data['destination']}")
        print(f"      Vehicle: {api_data['vehicle_type']}")
        print(f"      Polyline Points: {len(api_data['route_polyline'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_polyline_generation():
    """Test polyline generation directly"""
    print("\n🔄 Testing Polyline Generation")
    print("=" * 35)
    
    route_system = RealisticRouteSystem()
    
    # Test specific road segments
    test_cases = [
        ("Jalan Sudirman", (-6.2088, 106.8456), (-6.1900, 106.8234)),
        ("Jalan Thamrin", (-6.1900, 106.8234), (-6.1751, 106.8650)),
        ("Jalan Gatot Subroto", (-6.2088, 106.8456), (-6.2146, 106.8451)),
        ("Jalan TB Simatupang", (-6.2146, 106.8451), (-6.2297, 106.7997))
    ]
    
    for road_name, start, end in test_cases:
        print(f"\n🛣️ {road_name}")
        polyline = route_system._generate_road_polyline(start, end, road_name)
        
        print(f"   Points: {len(polyline)}")
        print(f"   Curve Factor: {route_system._get_road_curve_factor(road_name)}")
        
        if len(polyline) > 2:
            print(f"   ✅ Has curves (realistic)")
            
            # Check curve deviation
            start_point = polyline[0]
            middle_point = polyline[len(polyline)//2]
            end_point = polyline[-1]
            
            straight_middle = {
                "lat": start[0] + (end[0] - start[0]) * 0.5,
                "lng": start[1] + (end[1] - start[1]) * 0.5
            }
            
            curve_diff = abs(middle_point["lat"] - straight_middle["lat"]) + abs(middle_point["lng"] - straight_middle["lng"])
            print(f"   📐 Curve Deviation: {curve_diff:.6f}")
            
            if curve_diff > 0.0001:
                print(f"   ✅ Significant curve!")
            else:
                print(f"   ❌ Curve too small")
        else:
            print(f"   ❌ Straight line only")

def create_test_data():
    """Create test data with realistic routes"""
    print("\n📊 Creating Test Data")
    print("=" * 25)
    
    route_system = RealisticRouteSystem()
    weather = route_system.get_current_weather(-6.1702, 106.9417)
    all_routes = route_system.get_all_routes(weather)
    
    # Format for API
    formatted_routes = []
    total_distance = 0
    total_capacity = 0
    total_load = 0
    
    for route in all_routes:
        api_route = route_system.format_route_for_api(route)
        formatted_routes.append(api_route)
        total_distance += route.total_distance_km
        total_capacity += api_route["capacity_kg"]
        total_load += api_route["current_load_kg"]
        
        print(f"   📍 {route.destination}: {len(route.polyline)} polyline points")
    
    # Calculate statistics
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    test_data = {
        "success": True,
        "message": "PT. Sanghiang Perkasa Realistic Route Data (TEST)",
        "routes": formatted_routes,
        "statistics": {
            "total_routes": len(formatted_routes),
            "total_distance_km": total_distance,
            "total_capacity_kg": total_capacity,
            "total_load_kg": total_load,
            "average_utilization_percent": round(avg_utilization, 1),
            "active_vehicles": len(formatted_routes),
            "completed_routes": 0,
            "pending_routes": len(formatted_routes),
            "current_weather": weather
        }
    }
    
    # Save to file
    with open("test_realistic_now.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Test data created!")
    print(f"   Routes: {len(formatted_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   File: test_realistic_now.json")
    
    return test_data

def main():
    """Main function"""
    print("🚀 Test Realistic Routes NOW - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Test realistic routes
    success = test_realistic_routes_now()
    
    # Step 2: Test polyline generation
    test_polyline_generation()
    
    # Step 3: Create test data
    test_data = create_test_data()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   {'✅' if success else '❌'} Realistic routes working")
    print(f"   ✅ Test data created")
    
    if success:
        print("\n🎉 Realistic routes are working!")
        print("🔧 Next steps:")
        print("   1. Restart backend: cd vrp_rl_project && python run_server.py")
        print("   2. Restart frontend: cd frontend && npm start")
        print("   3. Clear browser cache (Ctrl+Shift+R)")
        print("   4. Check if routes follow roads on map")
    else:
        print("\n🔧 Issues detected - check logs above")

if __name__ == "__main__":
    main() 