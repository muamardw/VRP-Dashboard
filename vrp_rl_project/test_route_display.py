#!/usr/bin/env python3
"""
Test Route Display
Script untuk memverifikasi bahwa informasi jalan ditampilkan dengan benar
"""

from route_info_system import RouteInfoSystem
import json

def test_route_display():
    """Test route display with road information"""
    
    print("🧪 Testing Route Display dengan Informasi Jalan")
    print("=" * 60)
    
    # Initialize system
    route_system = RouteInfoSystem()
    
    # Test route
    test_route = [
        (-6.2088, 106.8456),  # Customer 0
        (-6.2146, 106.8451),  # Customer 2
        (-6.1865, 106.8343),  # Customer 4
        (-6.1751, 106.8650),  # Customer 1
        (-6.2297, 106.7997),  # Customer 3
        (-6.2088, 106.8456)   # Back to depot
    ]
    
    # Test different weather conditions
    weather_conditions = ["sunny", "rainy"]
    
    for weather in weather_conditions:
        print(f"\n🌤️ Testing dengan weather: {weather}")
        print("-" * 40)
        
        route_info = route_system.get_vehicle_route_info(1, test_route, weather)
        
        print(f"📊 Informasi Rute Kendaraan {route_info['vehicle_id']}:")
        print(f"Total Distance: {route_info['total_distance']:.2f} km")
        print(f"Total Time: {route_info['total_time']:.2f} jam")
        print(f"Weather: {route_info['weather_condition']}")
        print(f"Start Time: {route_info['start_time'].strftime('%H:%M')}")
        print(f"Estimated Completion: {route_info['estimated_completion'].strftime('%H:%M')}")
        
        print(f"\n🛣️ Detail Rute dengan Informasi Jalan:")
        for i, segment in enumerate(route_info['route_segments']):
            print(f"\nSegment {i+1}: {segment['from']} → {segment['to']}")
            print(f"  Distance: {segment['distance']:.2f} km")
            print(f"  Travel Time: {segment['travel_time']:.2f} jam")
            print(f"  Traffic: {segment['traffic_condition']}")
            print(f"  Weather: {segment['weather_condition']}")
            print(f"  Speed: {segment['adjusted_speed']:.1f} km/h")
            print(f"  ETA: {segment['estimated_arrival'].strftime('%H:%M')}")
            
            # Show detailed road information
            print(f"  🛣️ Jalan yang akan dilewati:")
            if 'road_segments' in segment and segment['road_segments']:
                for j, road in enumerate(segment['road_segments']):
                    print(f"    {j+1}. {road['road_name']} ({road.get('area', 'Unknown')})")
                    print(f"       - Panjang: {road['length']:.1f} km")
                    print(f"       - Traffic Level: {road['traffic_level']}")
                    print(f"       - Weather Impact: {road['weather_impact']}")
                    status = route_system._get_segment_status(
                        {"traffic_level": road['traffic_level']}, 
                        {"condition": road['traffic_level']}, 
                        {"condition": segment['weather_condition']}
                    )
                    print(f"       - Status: {status}")
            else:
                print(f"    ⚠️ Tidak ada informasi jalan yang tersedia")
        
        # Test API response format
        print(f"\n📡 Testing API Response Format:")
        api_response = {
            "vehicle_id": route_info["vehicle_id"],
            "total_distance": round(route_info["total_distance"], 2),
            "total_time": round(route_info["total_time"], 2),
            "weather_condition": route_info["weather_condition"],
            "start_time": route_info["start_time"].strftime("%H:%M"),
            "estimated_completion": route_info["estimated_completion"].strftime("%H:%M"),
            "route_segments": []
        }
        
        for segment in route_info["route_segments"]:
            formatted_segment = {
                "from": segment["from"],
                "to": segment["to"],
                "distance": round(segment["distance"], 2),
                "travel_time": round(segment["travel_time"], 2),
                "traffic_condition": segment["traffic_condition"],
                "weather_condition": segment["weather_condition"],
                "adjusted_speed": round(segment["adjusted_speed"], 1),
                "estimated_arrival": segment["estimated_arrival"].strftime("%H:%M"),
                "road_segments": segment["road_segments"]
            }
            api_response["route_segments"].append(formatted_segment)
        
        print("✅ API Response format:")
        print(json.dumps(api_response, indent=2, ensure_ascii=False))
        
        # Check if road_segments are present
        road_segments_count = 0
        for segment in api_response["route_segments"]:
            if "road_segments" in segment and segment["road_segments"]:
                road_segments_count += len(segment["road_segments"])
        
        print(f"\n📊 Road Segments Summary:")
        print(f"Total segments: {len(api_response['route_segments'])}")
        print(f"Total road segments: {road_segments_count}")
        
        if road_segments_count > 0:
            print("✅ Road segments are present in API response")
        else:
            print("❌ No road segments found in API response")

def test_simple_route():
    """Test simple route to debug"""
    
    print("\n🔍 Testing Simple Route")
    print("=" * 30)
    
    route_system = RouteInfoSystem()
    
    # Simple route
    simple_route = [
        (-6.2088, 106.8456),  # Customer 0
        (-6.2146, 106.8451),  # Customer 2
        (-6.2088, 106.8456)   # Back to depot
    ]
    
    route_info = route_system.get_vehicle_route_info(1, simple_route, "sunny")
    
    print(f"Route info keys: {list(route_info.keys())}")
    print(f"Number of segments: {len(route_info['route_segments'])}")
    
    for i, segment in enumerate(route_info['route_segments']):
        print(f"\nSegment {i+1} keys: {list(segment.keys())}")
        if 'road_segments' in segment:
            print(f"Road segments count: {len(segment['road_segments'])}")
            for j, road in enumerate(segment['road_segments']):
                print(f"  Road {j+1}: {road}")
        else:
            print("No road_segments found")

if __name__ == "__main__":
    test_route_display()
    test_simple_route() 