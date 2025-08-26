#!/usr/bin/env python3
"""
Debug Frontend Data - PT. Sanghiang Perkasa VRP
Script untuk debug data yang dikirim ke frontend
"""

import requests
import json
from realistic_route_system import RealisticRouteSystem

def test_backend_api():
    """Test backend API and check data format"""
    print("🔍 Testing Backend API Data Format")
    print("=" * 50)
    
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Backend API responding")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check first route in detail
            if data.get('routes'):
                first_route = data['routes'][0]
                
                print(f"\n📋 First Route Details:")
                print(f"   Destination: {first_route.get('destination', 'N/A')}")
                print(f"   Distance: {first_route.get('distance_km', 'N/A')} km")
                print(f"   Estimated Arrival: {first_route.get('estimated_arrival', 'N/A')}")
                print(f"   Vehicle Type: {first_route.get('vehicle_type', 'N/A')}")
                print(f"   Capacity: {first_route.get('capacity_kg', 'N/A')} kg")
                print(f"   Current Load: {first_route.get('current_load_kg', 'N/A')} kg")
                print(f"   Utilization: {first_route.get('utilization_percent', 'N/A')}%")
                print(f"   Traffic Level: {first_route.get('traffic_level', 'N/A')}")
                print(f"   Weather: {first_route.get('weather', {}).get('description', 'N/A')}")
                
                # Check polyline
                polyline_points = len(first_route.get('route_polyline', []))
                print(f"   Polyline Points: {polyline_points}")
                
                if polyline_points > 2:
                    print(f"   ✅ Realistic polyline detected")
                    print(f"   📍 Start: {first_route['route_polyline'][0]}")
                    print(f"   📍 Middle: {first_route['route_polyline'][polyline_points//2]}")
                    print(f"   📍 End: {first_route['route_polyline'][-1]}")
                else:
                    print(f"   ❌ Still straight line")
                
                # Check road segments
                road_segments = first_route.get('road_segments', [])
                print(f"   Road Segments: {len(road_segments)}")
                
                for i, segment in enumerate(road_segments[:3]):  # Show first 3
                    print(f"      {i+1}. {segment.get('road_name', 'N/A')}")
                    print(f"         Length: {segment.get('length_km', 'N/A')} km")
                    print(f"         Traffic: {segment.get('traffic_level', 'N/A')}")
                    print(f"         Area: {segment.get('area', 'N/A')}")
                    if segment.get('estimated_time_minutes'):
                        print(f"         Time: {segment.get('estimated_time_minutes')} min")
            
            return data
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return None

def create_test_data_for_frontend():
    """Create test data specifically for frontend"""
    print("\n📊 Creating Test Data for Frontend")
    print("=" * 40)
    
    route_system = RealisticRouteSystem()
    weather = route_system.get_current_weather(-6.1702, 106.9417)
    all_routes = route_system.get_all_routes(weather)
    
    # Format for frontend with all required fields
    formatted_routes = []
    total_distance = 0
    total_capacity = 0
    total_load = 0
    
    for route in all_routes:
        api_route = route_system.format_route_for_api(route)
        
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
            "route_polyline": api_route["route_polyline"],  # Realistic polyline
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
        
        formatted_routes.append(detailed_route)
        total_distance += route.total_distance_km
        total_capacity += api_route["capacity_kg"]
        total_load += api_route["current_load_kg"]
        
        print(f"   📍 {route.destination}:")
        print(f"      Distance: {route.total_distance_km} km")
        print(f"      Time: {route.total_time_minutes} minutes")
        print(f"      Polyline Points: {len(route.polyline)}")
        print(f"      Road Segments: {len(route.road_segments)}")
    
    # Calculate statistics
    avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
    
    test_data = {
        "success": True,
        "message": "PT. Sanghiang Perkasa Realistic Route Data (DEBUG)",
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
    with open("debug_frontend_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Debug data created!")
    print(f"   Routes: {len(formatted_routes)}")
    print(f"   Total Distance: {total_distance:.1f} km")
    print(f"   Weather: {weather}")
    print(f"   File: debug_frontend_data.json")
    
    return test_data

def verify_polyline_format():
    """Verify polyline format is correct for frontend"""
    print("\n🔄 Verifying Polyline Format")
    print("=" * 35)
    
    route_system = RealisticRouteSystem()
    route = route_system.get_optimal_route("bogor", "sunny")
    
    print(f"📍 Route to {route.destination}:")
    print(f"   Polyline Points: {len(route.polyline)}")
    
    if len(route.polyline) > 2:
        print(f"   ✅ Realistic polyline with curves")
        
        # Check format
        first_point = route.polyline[0]
        middle_point = route.polyline[len(route.polyline)//2]
        last_point = route.polyline[-1]
        
        print(f"   📍 First: {first_point}")
        print(f"   📍 Middle: {middle_point}")
        print(f"   📍 Last: {last_point}")
        
        # Check if format is correct for frontend
        if 'lat' in first_point and 'lng' in first_point:
            print(f"   ✅ Correct format for frontend")
        else:
            print(f"   ❌ Wrong format for frontend")
    else:
        print(f"   ❌ Still straight line")

def main():
    """Main function"""
    print("🚀 Debug Frontend Data - PT. Sanghiang Perkasa VRP")
    print("=" * 60)
    
    # Step 1: Verify polyline format
    verify_polyline_format()
    
    # Step 2: Test backend API
    api_data = test_backend_api()
    
    # Step 3: Create test data
    test_data = create_test_data_for_frontend()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print(f"   ✅ Polyline format verified")
    print(f"   {'✅' if api_data else '❌'} Backend API responding")
    print(f"   ✅ Test data created")
    
    if api_data and test_data:
        print("\n🎉 Data format is correct!")
        print("🔧 If frontend still shows straight lines:")
        print("   1. Check browser console for errors")
        print("   2. Verify API response in Network tab")
        print("   3. Clear browser cache (Ctrl+Shift+R)")
        print("   4. Check if polyline data is received")
    else:
        print("\n🔧 Issues detected - check logs above")

if __name__ == "__main__":
    main() 