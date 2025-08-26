#!/usr/bin/env python3
"""
Test Curved Routes - Verifikasi bahwa polyline sekarang memiliki kurva yang terlihat
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from realistic_route_system import RealisticRouteSystem
import json

def test_curved_polylines():
    """Test bahwa polyline sekarang memiliki kurva yang terlihat"""
    print("🧪 Testing Curved Polylines")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    
    # Test destinations
    destinations = ["bogor", "tangerang", "jakarta", "bekasi"]
    
    for dest in destinations:
        print(f"\n📍 Testing route to {dest.upper()}:")
        
        # Generate route
        route = route_system.get_optimal_route(dest, "sunny")
        
        print(f"   Distance: {route.total_distance_km:.1f} km")
        print(f"   Time: {route.total_time_minutes} minutes")
        print(f"   Score: {route.overall_score:.2f}")
        print(f"   Roads: {[s.road_name for s in route.road_segments]}")
        
        # Check polyline
        polyline_points = route.polyline
        print(f"   Polyline points: {len(polyline_points)}")
        
        if len(polyline_points) > 10:
            print(f"   ✅ Good: {len(polyline_points)} points (should show curves)")
            
            # Check if there are significant variations (curves)
            first_point = polyline_points[0]
            last_point = polyline_points[-1]
            mid_point = polyline_points[len(polyline_points)//2]
            
            # Calculate expected straight line distance
            expected_lat = (first_point['lat'] + last_point['lat']) / 2
            expected_lng = (first_point['lng'] + last_point['lng']) / 2
            
            # Calculate actual mid point deviation
            lat_deviation = abs(mid_point['lat'] - expected_lat)
            lng_deviation = abs(mid_point['lng'] - expected_lng)
            
            total_deviation = lat_deviation + lng_deviation
            
            if total_deviation > 0.001:  # Significant deviation indicates curves
                print(f"   ✅ Curved: Deviation = {total_deviation:.6f} (should be > 0.001)")
                print(f"      Mid point: ({mid_point['lat']:.6f}, {mid_point['lng']:.6f})")
                print(f"      Expected:  ({expected_lat:.6f}, {expected_lng:.6f})")
            else:
                print(f"   ⚠️  Still straight: Deviation = {total_deviation:.6f}")
        else:
            print(f"   ❌ Too few points: {len(polyline_points)} (need > 10)")
        
        # Show first few and last few points
        print(f"   First 3 points:")
        for i, point in enumerate(polyline_points[:3]):
            print(f"      {i+1}. ({point['lat']:.6f}, {point['lng']:.6f})")
        
        print(f"   Last 3 points:")
        for i, point in enumerate(polyline_points[-3:]):
            print(f"      {len(polyline_points)-2+i}. ({point['lat']:.6f}, {point['lng']:.6f})")
    
    print(f"\n🎯 Summary:")
    print(f"   - Routes should have > 10 polyline points")
    print(f"   - Mid-point deviation should be > 0.001 for visible curves")
    print(f"   - Check frontend map to see if routes follow roads")

def test_single_road_curve():
    """Test kurva untuk satu segmen jalan"""
    print("\n🛣️  Testing Single Road Curve")
    print("=" * 30)
    
    route_system = RealisticRouteSystem()
    
    # Test different road types
    test_roads = [
        ("Jalan Raya Bogor", (-6.2088, 106.8456), (-6.5950, 106.8167)),
        ("Jalan Tol Jakarta-Bogor", (-6.2088, 106.8456), (-6.3000, 106.8500)),
        ("Gang Siliwangi", (-6.6000, 106.8000), (-6.5950, 106.8167)),
        ("Jalan Sudirman", (-6.2088, 106.8456), (-6.1900, 106.8234))
    ]
    
    for road_name, start, end in test_roads:
        print(f"\n   Testing: {road_name}")
        
        polyline = route_system._generate_road_polyline(start, end, road_name)
        curve_factor = route_system._get_road_curve_factor(road_name)
        
        print(f"      Curve factor: {curve_factor}")
        print(f"      Points: {len(polyline)}")
        
        if len(polyline) > 5:
            # Check curve
            first = polyline[0]
            last = polyline[-1]
            mid = polyline[len(polyline)//2]
            
            expected_lat = (first['lat'] + last['lat']) / 2
            expected_lng = (first['lng'] + last['lng']) / 2
            
            deviation = abs(mid['lat'] - expected_lat) + abs(mid['lng'] - expected_lng)
            
            if deviation > 0.001:
                print(f"      ✅ Curved: {deviation:.6f}")
            else:
                print(f"      ⚠️  Straight: {deviation:.6f}")
        else:
            print(f"      ❌ Too few points")

if __name__ == "__main__":
    test_curved_polylines()
    test_single_road_curve()
    
    print(f"\n🎉 Test completed!")
    print(f"   If curves are visible, routes should now follow roads on the map!") 