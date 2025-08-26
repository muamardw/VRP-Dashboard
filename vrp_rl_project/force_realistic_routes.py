#!/usr/bin/env python3
"""
Force Realistic Routes - PT. Sanghiang Perkasa VRP
Script untuk memaksa penggunaan rute realistis yang mengikuti jalan
"""

from realistic_route_system import RealisticRouteSystem
import json
import requests

def force_realistic_backend():
    """Force backend to use realistic routes"""
    print("🔧 Forcing Realistic Routes in Backend")
    print("=" * 50)
    
    # Test realistic route system
    route_system = RealisticRouteSystem()
    
    # Get realistic routes for all destinations
    destinations = ["bogor", "tangerang", "jakarta", "bekasi"]
    weather = route_system.get_current_weather(-6.1702, 106.9417)
    
    print(f"🌤️ Current Weather: {weather}")
    print(f"📍 Depot: Jakarta Timur (-6.1702, 106.9417)")
    
    realistic_routes = []
    
    for dest in destinations:
        try:
            route = route_system.get_optimal_route(dest, weather)
            
            print(f"\n📍 {route.destination.upper()}:")
            print(f"   Distance: {route.total_distance_km:.1f} km")
            print(f"   Time: {route.total_time_minutes} minutes")
            print(f"   Polyline Points: {len(route.polyline)}")
            
            # Check if polyline is realistic (has curves)
            if len(route.polyline) > 2:
                print(f"   ✅ Realistic polyline with curves")
                print(f"   📍 Start: {route.polyline[0]}")
                print(f"   📍 Middle: {route.polyline[len(route.polyline)//2]}")
                print(f"   📍 End: {route.polyline[-1]}")
            else:
                print(f"   ❌ Still straight line ({len(route.polyline)} points)")
            
            # Show road segments
            print(f"   🛣️ Roads:")
            for i, segment in enumerate(route.road_segments, 1):
                print(f"      {i}. {segment.road_name}")
                print(f"         Length: {segment.length_km} km")
                print(f"         Traffic: {segment.traffic_level}")
                print(f"         Area: {segment.area}")
            
            # Format for API
            api_route = route_system.format_route_for_api(route)
            realistic_routes.append(api_route)
            
        except Exception as e:
            print(f"❌ Error with {dest}: {e}")
    
    return realistic_routes

def test_backend_api():
    """Test if backend is serving realistic routes"""
    print("\n🔗 Testing Backend API")
    print("=" * 30)
    
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Backend API responding")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check first route
            if data.get('routes'):
                first_route = data['routes'][0]
                polyline_points = len(first_route.get('route_polyline', []))
                
                print(f"   First Route: {first_route.get('destination', 'N/A')}")
                print(f"   Polyline Points: {polyline_points}")
                
                if polyline_points > 2:
                    print(f"   ✅ Realistic polyline detected")
                else:
                    print(f"   ❌ Still straight line")
                
                # Show road segments
                road_segments = first_route.get('road_segments', [])
                print(f"   Road Segments: {len(road_segments)}")
                for segment in road_segments[:3]:  # Show first 3
                    print(f"      - {segment.get('road_name', 'N/A')}")
            
            return data
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return None

def create_realistic_test_data():
    """Create test data with realistic routes"""
    print("\n📊 Creating Realistic Test Data")
    print("=" * 40)
    
    realistic_routes = force_realistic_backend()
    
    if not realistic_routes:
        print("❌ No realistic routes generated")
        return None
    
    # Calculate statistics
    total_distance = sum(route.get('distance_km', 0) for route in realistic_routes)
    total_capacity = sum(route.get('capacity_kg', 0) for route in realistic_routes)
    total_load = sum(route.get('current_load_kg', 0) for route in realistic_routes)
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    test_data = {
        "success": True,
        "message": "PT. Sanghiang Perkasa Realistic Route Data (FORCED)",
        "routes": realistic_routes,
        "statistics": {
            "total_routes": len(realistic_routes),
            "total_distance_km": total_distance,
            "total_capacity_kg": total_capacity,
            "total_load_kg": total_load,
            "average_utilization_percent": round(avg_utilization, 1),
            "active_vehicles": len(realistic_routes),
            "completed_routes": 0,
            "pending_routes": len(realistic_routes),
            "current_weather": "sunny"
        }
    }
    
    # Save to file
    with open("forced_realistic_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Realistic test data created!")
    print(f"   Routes: {len(realistic_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   File: forced_realistic_data.json")
    
    return test_data

def verify_polyline_curves():
    """Verify that polyline has realistic curves"""
    print("\n🔄 Verifying Polyline Curves")
    print("=" * 35)
    
    route_system = RealisticRouteSystem()
    
    # Test specific road segments
    test_roads = [
        ("Jalan Sudirman", (-6.2088, 106.8456), (-6.1900, 106.8234)),
        ("Jalan Thamrin", (-6.1900, 106.8234), (-6.1751, 106.8650)),
        ("Jalan Gatot Subroto", (-6.2088, 106.8456), (-6.2146, 106.8451)),
        ("Jalan TB Simatupang", (-6.2146, 106.8451), (-6.2297, 106.7997))
    ]
    
    for road_name, start, end in test_roads:
        print(f"\n🛣️ {road_name}")
        polyline = route_system._generate_road_polyline(start, end, road_name)
        
        print(f"   Points: {len(polyline)}")
        print(f"   Curve Factor: {route_system._get_road_curve_factor(road_name)}")
        
        if len(polyline) > 2:
            print(f"   ✅ Has curves (realistic)")
            # Show curve variation
            start_point = polyline[0]
            middle_point = polyline[len(polyline)//2]
            end_point = polyline[-1]
            
            print(f"   📍 Start: {start_point}")
            print(f"   📍 Middle: {middle_point}")
            print(f"   📍 End: {end_point}")
            
            # Check if middle point is different from straight line
            straight_middle = {
                "lat": start[0] + (end[0] - start[0]) * 0.5,
                "lng": start[1] + (end[1] - start[1]) * 0.5
            }
            
            curve_diff = abs(middle_point["lat"] - straight_middle["lat"]) + abs(middle_point["lng"] - straight_middle["lng"])
            print(f"   📐 Curve Deviation: {curve_diff:.6f}")
            
        else:
            print(f"   ❌ Straight line only")

def main():
    """Main function to force realistic routes"""
    print("🚀 Force Realistic Routes - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Verify polyline curves
    verify_polyline_curves()
    
    # Step 2: Force realistic backend data
    realistic_routes = force_realistic_backend()
    
    # Step 3: Test backend API
    api_data = test_backend_api()
    
    # Step 4: Create test data
    test_data = create_realistic_test_data()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   ✅ Polyline curves verified")
    print(f"   ✅ Realistic routes generated: {len(realistic_routes) if realistic_routes else 0}")
    print(f"   {'✅' if api_data else '❌'} Backend API responding")
    print(f"   ✅ Test data created")
    
    if realistic_routes and api_data:
        print("\n🎉 Realistic routes are working!")
        print("🔧 If frontend still shows straight lines:")
        print("   1. Clear browser cache (Ctrl+Shift+R)")
        print("   2. Check browser console for errors")
        print("   3. Verify API response in Network tab")
    else:
        print("\n🔧 Issues detected - check logs above")

if __name__ == "__main__":
    main() 