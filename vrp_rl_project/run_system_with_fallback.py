#!/usr/bin/env python3
"""
Run System with Fallback
Script untuk menjalankan sistem dengan error handling dan fallback data
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def check_api_server():
    """Check if API server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8001/", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Start the API server with error handling"""
    print("🚀 Starting Route Information API...")
    print("=" * 50)
    
    try:
        # Check if uvicorn is available
        import uvicorn
        
        # Start the API server
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "route_api:app", 
            "--host", "0.0.0.0", "--port", "8001"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("⏳ Waiting for API server to start...")
        time.sleep(5)
        
        if check_api_server():
            print("✅ API server started successfully!")
            print("📡 API available at: http://localhost:8001")
            print("📚 Documentation at: http://localhost:8001/docs")
            return api_process
        else:
            print("❌ API server failed to start")
            return None
            
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn"])
            return start_api_server()
        except:
            print("❌ Failed to install uvicorn")
            return None
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def open_dashboard():
    """Open the route dashboard in browser"""
    dashboard_path = Path("route_dashboard.html")
    
    if dashboard_path.exists():
        print("\n🌐 Opening Route Dashboard...")
        webbrowser.open(f"file://{dashboard_path.absolute()}")
        print("✅ Dashboard opened in browser!")
        print("📊 Dashboard URL: file://" + str(dashboard_path.absolute()))
    else:
        print("❌ Dashboard file not found!")
        print("Expected location:", dashboard_path.absolute())

def test_system():
    """Test the complete system"""
    print("\n🧪 Testing Complete System...")
    print("=" * 40)
    
    # Test 1: Check if route system works
    try:
        from route_info_system import RouteInfoSystem
        route_system = RouteInfoSystem()
        print("✅ Route system imported successfully")
    except Exception as e:
        print(f"❌ Route system import failed: {e}")
        return False
    
    # Test 2: Check if API can be imported
    try:
        from route_api import app
        print("✅ API can be imported successfully")
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False
    
    # Test 3: Test route calculation
    try:
        test_route = [
            (-6.2088, 106.8456),  # Customer 0
            (-6.2146, 106.8451),  # Customer 2
            (-6.2088, 106.8456)   # Back to depot
        ]
        
        route_info = route_system.get_vehicle_route_info(1, test_route, "sunny")
        print("✅ Route calculation working")
        print(f"   Total distance: {route_info['total_distance']:.2f} km")
        print(f"   Total time: {route_info['total_time']:.2f} jam")
        
        # Check if road segments are present
        road_segments_count = 0
        for segment in route_info['route_segments']:
            if 'road_segments' in segment:
                road_segments_count += len(segment['road_segments'])
        
        print(f"   Road segments: {road_segments_count}")
        
        if road_segments_count > 0:
            print("✅ Road segments are present")
        else:
            print("⚠️ No road segments found")
            
    except Exception as e:
        print(f"❌ Route calculation failed: {e}")
        return False
    
    return True

def show_manual_instructions():
    """Show manual instructions if automatic setup fails"""
    print("\n📋 Manual Setup Instructions")
    print("=" * 40)
    print("Jika sistem otomatis gagal, ikuti langkah berikut:")
    print()
    print("1. Start API Server:")
    print("   python route_api.py")
    print()
    print("2. Open Dashboard:")
    print("   Buka file route_dashboard.html di browser")
    print()
    print("3. Test API:")
    print("   curl http://localhost:8001/api/route-info/1?weather=sunny")
    print()
    print("4. Check Browser Console:")
    print("   F12 → Console → Refresh page")
    print()

def main():
    """Main function to run the system with fallback"""
    print("🚀 Route Information System untuk PT. Sanghiang Perkasa")
    print("=" * 60)
    
    # Test the system first
    if not test_system():
        print("❌ System test failed. Showing manual instructions...")
        show_manual_instructions()
        return
    
    # Start the API
    api_process = start_api_server()
    
    try:
        if api_process:
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
                
        else:
            print("\n⚠️ API server failed to start")
            print("Menggunakan fallback mode...")
            show_manual_instructions()
            
            # Open dashboard anyway
            open_dashboard()
            
            print("\n📊 Dashboard opened in fallback mode")
            print("⚠️ API server not running - using fallback data")
            print("💡 Start API manually: python route_api.py")
            
            # Keep running for dashboard
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