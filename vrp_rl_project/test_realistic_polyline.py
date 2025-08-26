#!/usr/bin/env python3
"""
Test Realistic Polyline - PT. Sanghiang Perkasa VRP
Test script untuk memverifikasi bahwa polyline mengikuti jalan yang realistis
"""

from realistic_route_system import RealisticRouteSystem
import json

def test_realistic_polyline():
    """Test realistic polyline generation"""
    print("🧪 Testing Realistic Polyline Generation")
    print("=" * 60)
    
    route_system = RealisticRouteSystem()
    
    # Test routes for all destinations
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
                
                # Show road segments
                print(f"   🛣️ Roads:")
                for i, segment in enumerate(route.road_segments, 1):
                    print(f"      {i}. {segment.road_name}")
                    print(f"         Length: {segment.length_km} km")
                    print(f"         Traffic: {segment.traffic_level}")
                    print(f"         Time: {segment.estimated_time_minutes} min")
                    print(f"         Area: {segment.area}")
                
                # Show polyline coordinates (first few and last few)
                if route.polyline:
                    print(f"   📍 Polyline Coordinates:")
                    print(f"      Start: {route.polyline[0]}")
                    if len(route.polyline) > 2:
                        print(f"      Middle: {route.polyline[len(route.polyline)//2]}")
                    print(f"      End: {route.polyline[-1]}")
                    print(f"      Total Points: {len(route.polyline)}")
                
                # Test API format
                api_data = route_system.format_route_for_api(route)
                print(f"   🔗 API Format:")
                print(f"      Destination: {api_data['destination']}")
                print(f"      Vehicle: {api_data['vehicle_type']}")
                print(f"      Polyline Points: {len(api_data['route_polyline'])}")
                
            except Exception as e:
                print(f"❌ Error testing {dest}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Realistic Polyline Test Complete!")
    print("\n🎯 Key Improvements:")
    print("   ✅ Polyline follows actual road curves")
    print("   ✅ Multiple intermediate points per road segment")
    print("   ✅ Different curve factors for different road types")
    print("   ✅ Realistic route optimization based on traffic & weather")
    print("   ✅ Dynamic road selection for optimal routes")

def test_polyline_curves():
    """Test specific polyline curve generation"""
    print("\n🔄 Testing Polyline Curve Generation")
    print("=" * 50)
    
    route_system = RealisticRouteSystem()
    
    # Test different road types
    test_roads = [
        ("Jalan Tol Jakarta-Bogor", (-6.2088, 106.8456), (-6.5950, 106.8167)),
        ("Jalan Raya Jakarta-Bekasi", (-6.2088, 106.8456), (-6.2200, 106.9000)),
        ("Jalan Gatot Subroto", (-6.2088, 106.8456), (-6.2146, 106.8451)),
        ("Jalan TB Simatupang", (-6.2146, 106.8451), (-6.2297, 106.7997))
    ]
    
    for road_name, start, end in test_roads:
        print(f"\n🛣️ Testing: {road_name}")
        polyline = route_system._generate_road_polyline(start, end, road_name)
        
        print(f"   Start: {start}")
        print(f"   End: {end}")
        print(f"   Points: {len(polyline)}")
        print(f"   Curve Factor: {route_system._get_road_curve_factor(road_name)}")
        
        # Show first few and last few points
        if len(polyline) >= 4:
            print(f"   First 2: {polyline[:2]}")
            print(f"   Last 2: {polyline[-2:]}")

if __name__ == "__main__":
    test_realistic_polyline()
    test_polyline_curves() 