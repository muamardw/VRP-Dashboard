#!/usr/bin/env python3
"""
Test Backend Curved Routes - Verifikasi bahwa backend mengirim polyline yang berkelok
"""

import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend_curved_routes():
    """Test bahwa backend mengirim polyline yang berkelok"""
    print("🧪 Testing Backend Curved Routes")
    print("=" * 50)
    
    # Test backend endpoint
    try:
        print("📡 Testing backend endpoint...")
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend response successful")
            
            routes = data.get("routes", [])
            print(f"📊 Found {len(routes)} routes")
            
            for i, route in enumerate(routes):
                print(f"\n📍 Route {i+1} to {route['destination']}:")
                
                # Check polyline
                polyline = route.get("route_polyline", [])
                print(f"   Polyline points: {len(polyline)}")
                
                if len(polyline) > 10:
                    print(f"   ✅ Good: {len(polyline)} points")
                    
                    # Check for curves
                    first_point = polyline[0]
                    last_point = polyline[-1]
                    mid_point = polyline[len(polyline)//2]
                    
                    # Calculate expected straight line
                    expected_lat = (first_point['lat'] + last_point['lat']) / 2
                    expected_lng = (first_point['lng'] + last_point['lng']) / 2
                    
                    # Calculate deviation
                    lat_deviation = abs(mid_point['lat'] - expected_lat)
                    lng_deviation = abs(mid_point['lng'] - expected_lng)
                    total_deviation = lat_deviation + lng_deviation
                    
                    if total_deviation > 0.001:
                        print(f"   ✅ Curved: Deviation = {total_deviation:.6f}")
                        print(f"      Mid: ({mid_point['lat']:.6f}, {mid_point['lng']:.6f})")
                        print(f"      Expected: ({expected_lat:.6f}, {expected_lng:.6f})")
                    else:
                        print(f"   ⚠️  Still straight: Deviation = {total_deviation:.6f}")
                    
                    # Show road segments
                    road_segments = route.get("road_segments", [])
                    print(f"   🛣️  Road segments: {len(road_segments)}")
                    for j, segment in enumerate(road_segments):
                        print(f"      {j+1}. {segment.get('road_name', 'Unknown')} ({segment.get('length_km', 0)} km)")
                        
                else:
                    print(f"   ❌ Too few points: {len(polyline)}")
                
                # Show other details
                print(f"   📏 Distance: {route.get('distance_km', 0)} km")
                print(f"   🚛 Vehicle: {route.get('vehicle_type', 'Unknown')}")
                print(f"   📦 Capacity: {route.get('capacity_kg', 0)} kg")
                print(f"   🎯 Utilization: {route.get('utilization_percent', 0):.1f}%")
                
        else:
            print(f"❌ Backend error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("   Start backend with: python run_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_realistic_route_system():
    """Test realistic route system directly"""
    print("\n🛣️  Testing Realistic Route System Directly")
    print("=" * 50)
    
    try:
        from realistic_route_system import RealisticRouteSystem
        
        route_system = RealisticRouteSystem()
        
        # Test all destinations
        destinations = ["bogor", "tangerang", "jakarta", "bekasi"]
        
        for dest in destinations:
            print(f"\n📍 Testing {dest.upper()} route:")
            
            route = route_system.get_optimal_route(dest, "sunny")
            
            print(f"   Distance: {route.total_distance_km:.1f} km")
            print(f"   Time: {route.total_time_minutes} minutes")
            print(f"   Score: {route.overall_score:.2f}")
            
            # Check polyline
            polyline = route.polyline
            print(f"   Polyline points: {len(polyline)}")
            
            if len(polyline) > 10:
                # Check curve
                first = polyline[0]
                last = polyline[-1]
                mid = polyline[len(polyline)//2]
                
                expected_lat = (first['lat'] + last['lat']) / 2
                expected_lng = (first['lng'] + last['lng']) / 2
                
                deviation = abs(mid['lat'] - expected_lat) + abs(mid['lng'] - expected_lng)
                
                if deviation > 0.001:
                    print(f"   ✅ Curved: {deviation:.6f}")
                else:
                    print(f"   ⚠️  Straight: {deviation:.6f}")
                    
                # Show road segments
                print(f"   🛣️  Roads: {[s.road_name for s in route.road_segments]}")
            else:
                print(f"   ❌ Too few points")
                
    except Exception as e:
        print(f"❌ Error testing realistic route system: {e}")

if __name__ == "__main__":
    test_backend_curved_routes()
    test_realistic_route_system()
    
    print(f"\n🎯 Summary:")
    print(f"   - Backend should return routes with > 10 polyline points")
    print(f"   - Polyline should have deviation > 0.001 for visible curves")
    print(f"   - Frontend should display curved routes on the map")
    print(f"   - Routes should follow actual road paths, not straight lines") 