#!/usr/bin/env python3
"""
Quick Test Realistic Polyline - PT. Sanghiang Perkasa VRP
Test cepat untuk memverifikasi bahwa polyline realistis sudah berfungsi
"""

from realistic_route_system import RealisticRouteSystem

def quick_test():
    """Quick test untuk realistic polyline"""
    print("🧪 Quick Test Realistic Polyline")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    
    # Test satu rute
    try:
        route = route_system.get_optimal_route("bogor", "sunny")
        
        print(f"✅ Route to {route.destination}:")
        print(f"   Distance: {route.total_distance_km:.1f} km")
        print(f"   Time: {route.total_time_minutes} minutes")
        print(f"   Score: {route.overall_score:.2f}")
        print(f"   Polyline Points: {len(route.polyline)}")
        
        # Show polyline coordinates
        if route.polyline:
            print(f"   📍 Polyline:")
            print(f"      Start: {route.polyline[0]}")
            print(f"      End: {route.polyline[-1]}")
            print(f"      Total Points: {len(route.polyline)}")
            
            # Check if polyline has curves (not just start and end)
            if len(route.polyline) > 2:
                print(f"      ✅ Has intermediate points (realistic curves)")
                print(f"      Middle point: {route.polyline[len(route.polyline)//2]}")
            else:
                print(f"      ❌ Only start and end points (straight line)")
        
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

def test_polyline_curves():
    """Test specific polyline curve generation"""
    print("\n🔄 Testing Polyline Curves")
    print("=" * 30)
    
    route_system = RealisticRouteSystem()
    
    # Test different road types
    test_cases = [
        ("Jalan Tol Jakarta-Bogor", (-6.2088, 106.8456), (-6.5950, 106.8167)),
        ("Jalan Raya Jakarta-Bekasi", (-6.2088, 106.8456), (-6.2200, 106.9000)),
        ("Jalan Gatot Subroto", (-6.2088, 106.8456), (-6.2146, 106.8451))
    ]
    
    for road_name, start, end in test_cases:
        print(f"\n🛣️ {road_name}")
        polyline = route_system._generate_road_polyline(start, end, road_name)
        
        print(f"   Points: {len(polyline)}")
        print(f"   Curve Factor: {route_system._get_road_curve_factor(road_name)}")
        
        if len(polyline) > 2:
            print(f"   ✅ Has curves (realistic)")
            print(f"   First: {polyline[0]}")
            print(f"   Middle: {polyline[len(polyline)//2]}")
            print(f"   Last: {polyline[-1]}")
        else:
            print(f"   ❌ Straight line only")

if __name__ == "__main__":
    success = quick_test()
    test_polyline_curves()
    
    if success:
        print("\n✅ Realistic polyline is working!")
        print("🎯 Now start the backend and frontend to see realistic routes")
    else:
        print("\n❌ Realistic polyline has issues")
        print("🔧 Check the realistic_route_system.py implementation") 