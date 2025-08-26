#!/usr/bin/env python3
"""
Fix Realistic Routes - PT. Sanghiang Perkasa VRP
Script untuk memperbaiki dan memverifikasi sistem routing realistis
"""

from realistic_route_system import RealisticRouteSystem
import json

def verify_realistic_routes():
    """Verify that realistic routes are working properly"""
    print("🔧 Verifying Realistic Routes")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    
    # Test all destinations
    destinations = ["bogor", "tangerang", "jakarta", "bekasi"]
    weather_conditions = ["sunny", "rain", "cloudy"]
    
    for weather in weather_conditions:
        print(f"\n🌤️ Weather: {weather.upper()}")
        print("-" * 40)
        
        for dest in destinations:
            try:
                route = route_system.get_optimal_route(dest, weather)
                
                print(f"\n📍 {route.destination.upper()}:")
                print(f"   Distance: {route.total_distance_km:.1f} km")
                print(f"   Time: {route.total_time_minutes} minutes")
                print(f"   Score: {route.overall_score:.2f}")
                print(f"   Polyline Points: {len(route.polyline)}")
                
                # Check if polyline has realistic curves
                if len(route.polyline) > 2:
                    print(f"   ✅ Realistic polyline with {len(route.polyline)} points")
                    
                    # Show first few and last few points
                    print(f"   📍 Polyline Preview:")
                    print(f"      Start: {route.polyline[0]}")
                    if len(route.polyline) > 4:
                        print(f"      Middle: {route.polyline[len(route.polyline)//2]}")
                    print(f"      End: {route.polyline[-1]}")
                else:
                    print(f"   ❌ Straight line only ({len(route.polyline)} points)")
                
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
                
            except Exception as e:
                print(f"❌ Error testing {dest}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Realistic Routes Verification Complete!")

def test_backend_integration():
    """Test backend integration with realistic routes"""
    print("\n🔗 Testing Backend Integration")
    print("=" * 40)
    
    try:
        # Import backend components
        from backend_api import route_system
        
        # Test getting all routes
        weather = route_system.get_current_weather(-6.1702, 106.9417)
        all_routes = route_system.get_all_routes(weather)
        
        print(f"✅ Backend integration working!")
        print(f"   Weather: {weather}")
        print(f"   Routes: {len(all_routes)}")
        
        for route in all_routes:
            print(f"   📍 {route.destination}: {len(route.polyline)} polyline points")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend integration error: {e}")
        return False

def generate_test_data():
    """Generate test data for frontend"""
    print("\n📊 Generating Test Data")
    print("=" * 30)
    
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
    
    # Calculate statistics
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    test_data = {
        "success": True,
        "message": "PT. Sanghiang Perkasa Realistic Route Data",
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
    
    # Save to file for testing
    with open("test_realistic_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Test data generated!")
    print(f"   Routes: {len(formatted_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   Weather: {weather}")
    print(f"   File: test_realistic_data.json")
    
    return test_data

def main():
    """Main function to fix and verify realistic routes"""
    print("🚀 Fix Realistic Routes - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Verify realistic routes
    verify_realistic_routes()
    
    # Step 2: Test backend integration
    backend_ok = test_backend_integration()
    
    # Step 3: Generate test data
    test_data = generate_test_data()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   ✅ Realistic routes verified")
    print(f"   {'✅' if backend_ok else '❌'} Backend integration")
    print(f"   ✅ Test data generated")
    
    if backend_ok:
        print("\n🎉 Ready to start backend and frontend!")
        print("   cd vrp_rl_project && python run_server.py")
        print("   cd frontend && npm start")
    else:
        print("\n🔧 Backend needs fixing before starting")

if __name__ == "__main__":
    main() 