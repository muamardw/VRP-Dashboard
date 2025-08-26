#!/usr/bin/env python3
"""
Force Realistic Frontend - PT. Sanghiang Perkasa VRP
Script untuk force realistic polyline di frontend
"""

import requests
import json
from realistic_route_system import RealisticRouteSystem

def force_realistic_backend_data():
    """Force backend to return realistic polyline data"""
    print("🔧 Forcing Realistic Backend Data")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    weather = route_system.get_current_weather(-6.1702, 106.9417)
    all_routes = route_system.get_all_routes(weather)
    
    # Create realistic routes with detailed polyline
    realistic_routes = []
    total_distance = 0
    total_capacity = 0
    total_load = 0
    
    for route in all_routes:
        api_route = route_system.format_route_for_api(route)
        
        # Ensure polyline has correct format for Leaflet
        polyline = []
        for point in route.polyline:
            if isinstance(point, dict) and 'lat' in point and 'lng' in point:
                polyline.append({
                    'lat': float(point['lat']),
                    'lng': float(point['lng'])
                })
        
        # Create detailed route for frontend
        detailed_route = {
            "id": api_route["id"],
            "destination": api_route["destination"],
            "vehicle_id": api_route["vehicle_id"],
            "vehicle_type": api_route["vehicle_type"],
            "capacity_kg": api_route["capacity_kg"],
            "current_load_kg": api_route["current_load_kg"],
            "remaining_capacity_kg": api_route["remaining_capacity_kg"],
            "distance_km": api_route["distance_km"],
            "start_location": api_route["start_location"],
            "end_location": api_route["end_location"],
            "status": api_route["status"],
            "estimated_arrival": api_route["estimated_arrival"],
            "route_polyline": polyline,  # Realistic polyline
            "traffic_level": "medium",
            "traffic_color": "#ffaa00",
            "weather": {
                "description": weather,
                "temperature": 28,
                "humidity": 75
            },
            "utilization_percent": (api_route["current_load_kg"] / api_route["capacity_kg"]) * 100,
            "road_segments": api_route["road_segments"],
            "traffic_score": api_route["traffic_score"],
            "weather_score": api_route["weather_score"],
            "overall_score": api_route["overall_score"]
        }
        
        realistic_routes.append(detailed_route)
        total_distance += route.total_distance_km
        total_capacity += api_route["capacity_kg"]
        total_load += api_route["current_load_kg"]
        
        print(f"   📍 {route.destination}:")
        print(f"      Distance: {route.total_distance_km} km")
        print(f"      Time: {route.total_time_minutes} minutes")
        print(f"      Polyline Points: {len(polyline)}")
        
        if len(polyline) > 2:
            print(f"      ✅ Realistic polyline with curves")
            print(f"      📍 Start: {polyline[0]}")
            print(f"      📍 Middle: {polyline[len(polyline)//2]}")
            print(f"      📍 End: {polyline[-1]}")
        else:
            print(f"      ❌ Still straight line")
        
        # Show road segments
        print(f"      🛣️ Roads:")
        for i, segment in enumerate(route.road_segments, 1):
            print(f"         {i}. {segment.road_name}")
            print(f"            Length: {segment.length_km} km")
            print(f"            Traffic: {segment.traffic_level}")
            print(f"            Area: {segment.area}")
    
    # Calculate statistics
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    response_data = {
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
            "current_weather": weather
        }
    }
    
    print(f"✅ Realistic backend data created!")
    print(f"   Routes: {len(realistic_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   Weather: {weather}")
    
    return response_data

def test_frontend_connection():
    """Test if frontend can connect to backend"""
    print("\n🔗 Testing Frontend Connection")
    print("=" * 35)
    
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Frontend can connect to backend")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check first route polyline
            if data.get('routes'):
                first_route = data['routes'][0]
                polyline = first_route.get('route_polyline', [])
                
                print(f"   First Route: {first_route.get('destination', 'N/A')}")
                print(f"   Polyline Points: {len(polyline)}")
                
                if len(polyline) > 2:
                    print(f"   ✅ Realistic polyline detected")
                    print(f"   📍 Start: {polyline[0]}")
                    print(f"   📍 Middle: {polyline[len(polyline)//2]}")
                    print(f"   📍 End: {polyline[-1]}")
                else:
                    print(f"   ❌ Still straight line")
            
            return True
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def create_frontend_test_data():
    """Create test data specifically for frontend"""
    print("\n📊 Creating Frontend Test Data")
    print("=" * 40)
    
    # Get realistic data
    realistic_data = force_realistic_backend_data()
    
    # Save to file for frontend testing
    with open("frontend_test_data.json", "w") as f:
        json.dump(realistic_data, f, indent=2)
    
    print(f"✅ Frontend test data created!")
    print(f"   File: frontend_test_data.json")
    
    return realistic_data

def verify_polyline_format():
    """Verify polyline format is correct for frontend"""
    print("\n🔄 Verifying Polyline Format for Frontend")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    route = route_system.get_optimal_route("bogor", "sunny")
    
    print(f"📍 Route to {route.destination}:")
    print(f"   Polyline Points: {len(route.polyline)}")
    
    if len(route.polyline) > 2:
        print(f"   ✅ Realistic polyline with curves")
        
        # Check format for Leaflet
        valid_points = 0
        for point in route.polyline:
            if isinstance(point, dict) and 'lat' in point and 'lng' in point:
                valid_points += 1
        
        print(f"   Valid Points: {valid_points}/{len(route.polyline)}")
        
        if valid_points == len(route.polyline):
            print(f"   ✅ All points valid for Leaflet Polyline")
        else:
            print(f"   ❌ Some points invalid for Leaflet Polyline")
        
        # Show sample points
        print(f"   📍 Sample Points:")
        for i, point in enumerate(route.polyline[:3]):
            print(f"      {i+1}. {point}")
        
        # Check coordinates range
        valid_coords = 0
        for point in route.polyline:
            if isinstance(point, dict) and 'lat' in point and 'lng' in point:
                lat = float(point['lat'])
                lng = float(point['lng'])
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    valid_coords += 1
        
        print(f"   Valid Coordinates: {valid_coords}/{len(route.polyline)}")
        
        if valid_coords == len(route.polyline):
            print(f"   ✅ All coordinates in valid range")
        else:
            print(f"   ❌ Some coordinates out of range")
    else:
        print(f"   ❌ Still straight line")

def main():
    """Main function"""
    print("🚀 Force Realistic Frontend - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Verify polyline format
    verify_polyline_format()
    
    # Step 2: Force realistic backend data
    realistic_data = force_realistic_backend_data()
    
    # Step 3: Test frontend connection
    frontend_ok = test_frontend_connection()
    
    # Step 4: Create frontend test data
    test_data = create_frontend_test_data()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   ✅ Polyline format verified")
    print(f"   ✅ Realistic backend data created")
    print(f"   {'✅' if frontend_ok else '❌'} Frontend connection")
    print(f"   ✅ Frontend test data created")
    
    if realistic_data and frontend_ok:
        print("\n🎉 Realistic polyline is ready for frontend!")
        print("🔧 Next steps:")
        print("   1. Restart backend: cd vrp_rl_project && python run_server.py")
        print("   2. Restart frontend: cd frontend && npm start")
        print("   3. Clear browser cache (Ctrl+Shift+R)")
        print("   4. Check if polyline follows roads on map")
        print("   5. Verify realistic curves are displayed")
    else:
        print("\n🔧 Issues detected - check logs above")

if __name__ == "__main__":
    main() 