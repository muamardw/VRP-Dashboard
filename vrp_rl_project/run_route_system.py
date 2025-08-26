#!/usr/bin/env python3
"""
Run Route Information System
Script untuk menjalankan sistem informasi rute dengan nama jalan dan kondisi dinamis
"""

import subprocess
import time
import webbrowser
import os
from pathlib import Path

def start_route_api():
    """Start the route information API"""
    print("🚗 Starting Route Information API...")
    print("=" * 50)
    
    try:
        # Start the API server
        api_process = subprocess.Popen([
            "python", "route_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Route API started successfully!")
        print("📡 API available at: http://localhost:8001")
        print("📚 Documentation at: http://localhost:8001/docs")
        
        return api_process
        
    except Exception as e:
        print(f"❌ Error starting Route API: {e}")
        return None

def open_dashboard():
    """Open the route dashboard in browser"""
    dashboard_path = Path("route_dashboard.html")
    
    if dashboard_path.exists():
        print("\n🌐 Opening Route Dashboard...")
        webbrowser.open(f"file://{dashboard_path.absolute()}")
        print("✅ Dashboard opened in browser!")
    else:
        print("❌ Dashboard file not found!")

def test_route_system():
    """Test the route information system"""
    print("\n🧪 Testing Route Information System...")
    print("=" * 50)
    
    try:
        # Import and test the route system
        from route_info_system import RouteInfoSystem
        
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
        weather_conditions = ["sunny", "cloudy", "rainy", "stormy"]
        
        for weather in weather_conditions:
            print(f"\n🌤️ Testing with weather: {weather}")
            route_info = route_system.get_vehicle_route_info(1, test_route, weather)
            
            print(f"  Total Distance: {route_info['total_distance']:.2f} km")
            print(f"  Total Time: {route_info['total_time']:.2f} jam")
            print(f"  Weather: {route_info['weather_condition']}")
            print(f"  Start Time: {route_info['start_time'].strftime('%H:%M')}")
            print(f"  Estimated Completion: {route_info['estimated_completion'].strftime('%H:%M')}")
            
            # Show road segments
            for i, segment in enumerate(route_info['route_segments']):
                print(f"  Segment {i+1}: {segment['from']} → {segment['to']}")
                print(f"    Distance: {segment['distance']:.2f} km")
                print(f"    Travel Time: {segment['travel_time']:.2f} jam")
                print(f"    Traffic: {segment['traffic_condition']}")
                print(f"    Weather: {segment['weather_condition']}")
                print(f"    Speed: {segment['adjusted_speed']:.1f} km/h")
                roads = [road['road_name'] for road in segment['road_segments']]
                print(f"    Roads: {', '.join(roads)}")
        
        print("\n✅ Route system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing route system: {e}")
        return False

def main():
    """Main function to run the route information system"""
    print("🚀 Route Information System untuk DQN VRP")
    print("=" * 60)
    
    # Test the route system first
    if not test_route_system():
        print("❌ Route system test failed. Exiting...")
        return
    
    # Start the API
    api_process = start_route_api()
    if not api_process:
        print("❌ Failed to start API. Exiting...")
        return
    
    try:
        # Wait a moment for the API to start
        print("\n⏳ Waiting for API to start...")
        time.sleep(3)
        
        # Open dashboard
        open_dashboard()
        
        print("\n🎉 Route Information System is running!")
        print("📊 Dashboard: Open route_dashboard.html in your browser")
        print("📡 API: http://localhost:8001")
        print("📚 Docs: http://localhost:8001/docs")
        print("\n💡 Press Ctrl+C to stop the system")
        
        # Keep the system running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Route Information System...")
        
        # Stop the API process
        if api_process:
            api_process.terminate()
            print("✅ API stopped successfully!")
        
        print("👋 Route Information System stopped. Goodbye!")

if __name__ == "__main__":
    main() 