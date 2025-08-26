#!/usr/bin/env python3
"""
Quick Test Curves - Test cepat untuk memverifikasi kurva yang sudah diperbaiki
"""

from realistic_route_system import RealisticRouteSystem
import math

def test_curves():
    print("🧪 Quick Test - Curved Routes")
    print("=" * 40)
    
    route_system = RealisticRouteSystem()
    
    # Test single road curve
    print("\n🛣️  Testing single road curve:")
    start = (-6.2088, 106.8456)  # Jakarta
    end = (-6.5950, 106.8167)    # Bogor
    
    polyline = route_system._generate_road_polyline(start, end, "Jalan Raya Bogor")
    curve_factor = route_system._get_road_curve_factor("Jalan Raya Bogor")
    
    print(f"   Road: Jalan Raya Bogor")
    print(f"   Curve factor: {curve_factor}")
    print(f"   Points: {len(polyline)}")
    
    if len(polyline) > 10:
        # Check curve
        first = polyline[0]
        last = polyline[-1]
        mid = polyline[len(polyline)//2]
        
        expected_lat = (first['lat'] + last['lat']) / 2
        expected_lng = (first['lng'] + last['lng']) / 2
        
        deviation = abs(mid['lat'] - expected_lat) + abs(mid['lng'] - expected_lng)
        
        print(f"   Deviation: {deviation:.6f}")
        if deviation > 0.001:
            print(f"   ✅ CURVED - Should be visible on map!")
        else:
            print(f"   ⚠️  Still straight")
    else:
        print(f"   ❌ Too few points")
    
    # Test full route
    print(f"\n📍 Testing full route to Bogor:")
    route = route_system.get_optimal_route("bogor", "sunny")
    
    print(f"   Distance: {route.total_distance_km:.1f} km")
    print(f"   Polyline points: {len(route.polyline)}")
    
    if len(route.polyline) > 20:
        print(f"   ✅ Good polyline length")
        
        # Check curve
        first = route.polyline[0]
        last = route.polyline[-1]
        mid = route.polyline[len(route.polyline)//2]
        
        expected_lat = (first['lat'] + last['lat']) / 2
        expected_lng = (first['lng'] + last['lng']) / 2
        
        deviation = abs(mid['lat'] - expected_lat) + abs(mid['lng'] - expected_lng)
        
        print(f"   Deviation: {deviation:.6f}")
        if deviation > 0.001:
            print(f"   ✅ CURVED ROUTE - Should follow roads on map!")
        else:
            print(f"   ⚠️  Still straight route")
    else:
        print(f"   ❌ Too few polyline points")
    
    print(f"\n🎯 Expected Results:")
    print(f"   - Polyline should have > 20 points")
    print(f"   - Deviation should be > 0.001 for visible curves")
    print(f"   - Frontend map should show curved routes, not straight lines")
    print(f"   - Routes should follow actual road paths")

if __name__ == "__main__":
    test_curves() 