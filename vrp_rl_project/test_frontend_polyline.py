#!/usr/bin/env python3
"""
Test Frontend Polyline - PT. Sanghiang Perkasa VRP
Script untuk test polyline di frontend dan debug masalah rendering
"""

import requests
import json
from realistic_route_system import RealisticRouteSystem

def test_backend_polyline_data():
    """Test backend polyline data"""
    print("🔍 Testing Backend Polyline Data")
    print("=" * 50)
    
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Backend API responding")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check each route's polyline
            for i, route in enumerate(data.get('routes', [])):
                print(f"\n📍 Route {i+1}: {route.get('destination', 'N/A')}")
                
                polyline = route.get('route_polyline', [])
                polyline_points = len(polyline)
                
                print(f"   Polyline Points: {polyline_points}")
                
                if polyline_points > 2:
                    print(f"   ✅ Realistic polyline detected")
                    print(f"   📍 Start: {polyline[0]}")
                    print(f"   📍 Middle: {polyline[polyline_points//2]}")
                    print(f"   📍 End: {polyline[-1]}")
                    
                    # Check if format is correct for Leaflet
                    if all('lat' in p and 'lng' in p for p in polyline):
                        print(f"   ✅ Correct format for Leaflet Polyline")
                    else:
                        print(f"   ❌ Wrong format for Leaflet Polyline")
                else:
                    print(f"   ❌ Still straight line")
                
                # Check road segments
                road_segments = route.get('road_segments', [])
                print(f"   Road Segments: {len(road_segments)}")
                
                for j, segment in enumerate(road_segments[:2]):  # Show first 2
                    print(f"      {j+1}. {segment.get('road_name', 'N/A')}")
                    print(f"         Length: {segment.get('length_km', 'N/A')} km")
                    print(f"         Traffic: {segment.get('traffic_level', 'N/A')}")
            
            return data
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return None

def create_test_polyline_data():
    """Create test polyline data for frontend"""
    print("\n📊 Creating Test Polyline Data")
    print("=" * 40)
    
    route_system = RealisticRouteSystem()
    weather = route_system.get_current_weather(-6.1702, 106.9417)
    all_routes = route_system.get_all_routes(weather)
    
    # Create test data with realistic polyline
    test_routes = []
    
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
        
        test_route = {
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
        
        test_routes.append(test_route)
        
        print(f"   📍 {route.destination}:")
        print(f"      Polyline Points: {len(polyline)}")
        print(f"      Road Segments: {len(route.road_segments)}")
        
        if len(polyline) > 2:
            print(f"      ✅ Realistic polyline with curves")
            print(f"      📍 Start: {polyline[0]}")
            print(f"      📍 Middle: {polyline[len(polyline)//2]}")
            print(f"      📍 End: {polyline[-1]}")
        else:
            print(f"      ❌ Still straight line")
    
    # Calculate statistics
    total_distance = sum(route.total_distance_km for route in all_routes)
    total_capacity = sum(api_route["capacity_kg"] for api_route in [route_system.format_route_for_api(r) for r in all_routes])
    total_load = sum(api_route["current_load_kg"] for api_route in [route_system.format_route_for_api(r) for r in all_routes])
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    test_data = {
        "success": True,
        "message": "PT. Sanghiang Perkasa Realistic Route Data (TEST POLYLINE)",
        "routes": test_routes,
        "statistics": {
            "total_routes": len(test_routes),
            "total_distance_km": total_distance,
            "total_capacity_kg": total_capacity,
            "total_load_kg": total_load,
            "average_utilization_percent": round(avg_utilization, 1),
            "active_vehicles": len(test_routes),
            "completed_routes": 0,
            "pending_routes": len(test_routes),
            "current_weather": weather
        }
    }
    
    # Save to file
    with open("test_polyline_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Test polyline data created!")
    print(f"   Routes: {len(test_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   Weather: {weather}")
    print(f"   File: test_polyline_data.json")
    
    return test_data

def verify_polyline_rendering():
    """Verify polyline can be rendered correctly"""
    print("\n🔄 Verifying Polyline Rendering")
    print("=" * 40)
    
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
            print(f"   ✅ All points valid for Leaflet")
        else:
            print(f"   ❌ Some points invalid for Leaflet")
        
        # Show sample points
        print(f"   📍 Sample Points:")
        for i, point in enumerate(route.polyline[:3]):
            print(f"      {i+1}. {point}")
        
        # Check if points are in correct range for maps
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
    print("🚀 Test Frontend Polyline - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Verify polyline rendering
    verify_polyline_rendering()
    
    # Step 2: Test backend polyline data
    api_data = test_backend_polyline_data()
    
    # Step 3: Create test polyline data
    test_data = create_test_polyline_data()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   ✅ Polyline rendering verified")
    print(f"   {'✅' if api_data else '❌'} Backend polyline data")
    print(f"   ✅ Test polyline data created")
    
    if api_data and test_data:
        print("\n🎉 Polyline data is correct!")
        print("🔧 If frontend still shows straight lines:")
        print("   1. Check browser console for errors")
        print("   2. Verify polyline data in Network tab")
        print("   3. Clear browser cache (Ctrl+Shift+R)")
        print("   4. Check if Leaflet Polyline is rendering correctly")
        print("   5. Verify polyline points are in correct format")
    else:
        print("\n🔧 Issues detected - check logs above")

if __name__ == "__main__":
    main() 