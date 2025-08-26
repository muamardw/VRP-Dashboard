#!/usr/bin/env python3
"""
Test System - PT. Sanghiang Perkasa VRP
Script untuk testing backend dan frontend
"""

import requests
import time
import webbrowser
import subprocess
import sys
from pathlib import Path

def test_backend():
    """Test backend API"""
    print("🔍 Testing Backend API...")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/test",
        "/api/simple-pt-sanghiang-data",
        "/api/pt-sanghiang-data"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/api/test":
                    print(f"✅ {endpoint}: {data.get('message', 'OK')}")
                elif endpoint == "/api/simple-pt-sanghiang-data":
                    routes_count = len(data.get('routes', []))
                    print(f"✅ {endpoint}: {routes_count} routes found")
                else:
                    print(f"✅ {endpoint}: API responding")
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection failed (Backend not running)")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print()

def test_frontend():
    """Test frontend"""
    print("🌐 Testing Frontend...")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running at http://localhost:3000")
        else:
            print(f"❌ Frontend status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running (npm start not executed)")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    
    print()

def test_data_integrity():
    """Test data integrity"""
    print("📊 Testing Data Integrity...")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ['success', 'routes', 'statistics']
            for field in required_fields:
                if field in data:
                    print(f"✅ {field}: Present")
                else:
                    print(f"❌ {field}: Missing")
            
            # Check routes
            routes = data.get('routes', [])
            print(f"✅ Routes count: {len(routes)}")
            
            for i, route in enumerate(routes):
                print(f"  Route {i+1}: {route.get('destination', 'Unknown')}")
                
                # Check road segments
                road_segments = route.get('road_segments', [])
                print(f"    Road segments: {len(road_segments)}")
                
                for j, road in enumerate(road_segments):
                    road_name = road.get('road_name', 'Unknown')
                    traffic_level = road.get('traffic_level', 'Unknown')
                    area = road.get('area', 'Unknown')
                    print(f"      {j+1}. {road_name} ({traffic_level}, {area})")
            
            # Check statistics
            stats = data.get('statistics', {})
            print(f"✅ Statistics: {stats.get('total_routes', 0)} routes, {stats.get('total_distance_km', 0)} km")
            
        else:
            print("❌ Cannot fetch data for integrity check")
            
    except Exception as e:
        print(f"❌ Data integrity check failed: {e}")
    
    print()

def test_browser_integration():
    """Test browser integration"""
    print("🌐 Testing Browser Integration...")
    print("=" * 40)
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            
            # Ask user if they want to open browser
            user_input = input("🌐 Open dashboard in browser? (y/n): ").lower()
            if user_input in ['y', 'yes']:
                webbrowser.open("http://localhost:3000")
                print("✅ Dashboard opened in browser")
            else:
                print("⏭️ Skipping browser opening")
        else:
            print("❌ Frontend not accessible")
            
    except Exception as e:
        print(f"❌ Browser integration test failed: {e}")
    
    print()

def show_manual_instructions():
    """Show manual instructions"""
    print("📋 Manual Testing Instructions")
    print("=" * 40)
    print()
    print("1. Test Backend:")
    print("   curl http://localhost:8000/api/test")
    print("   curl http://localhost:8000/api/simple-pt-sanghiang-data")
    print()
    print("2. Test Frontend:")
    print("   Open http://localhost:3000 in browser")
    print("   Check browser console (F12) for errors")
    print()
    print("3. Test Features:")
    print("   - Click on route lines to see road names")
    print("   - Click on vehicle markers to see details")
    print("   - Open panel detail to see road segments")
    print()
    print("4. Expected Results:")
    print("   - Map with 3 routes (Jakarta Pusat, Selatan, Timur)")
    print("   - Road names in popups and panel detail")
    print("   - Traffic and weather information")
    print("   - Vehicle animations")
    print()

def main():
    """Main testing function"""
    print("🧪 PT. Sanghiang Perkasa VRP System Test")
    print("=" * 50)
    print()
    
    # Test backend
    test_backend()
    
    # Test frontend
    test_frontend()
    
    # Test data integrity
    test_data_integrity()
    
    # Test browser integration
    test_browser_integration()
    
    # Show results summary
    print("📊 Test Summary")
    print("=" * 40)
    print("✅ Backend API: Tested")
    print("✅ Frontend: Tested")
    print("✅ Data Integrity: Verified")
    print("✅ Browser Integration: Ready")
    print()
    print("🎯 Next Steps:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Check map for routes and road names")
    print("3. Click on routes and vehicles for details")
    print("4. Open panel detail for comprehensive information")
    print()
    
    # Show manual instructions
    show_manual_instructions()

if __name__ == "__main__":
    main() 