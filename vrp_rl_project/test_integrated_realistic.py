#!/usr/bin/env python3
"""
Test Integrated Realistic Polyline - PT. Sanghiang Perkasa VRP
Script untuk test realistic polyline yang terintegrasi dengan backend dan frontend
"""

import requests
import json
import time
from realistic_route_system import RealisticRouteSystem

def test_backend_realistic_polyline():
    """Test backend realistic polyline"""
    print("🔍 Testing Backend Realistic Polyline")
    print("=" * 45)
    
    try:
        # Test the API endpoint
        response = requests.get("http://localhost:8000/api/simple-pt-sanghiang-data", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Backend API responding")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check each route's polyline
            realistic_routes = 0
            total_routes = 0
            
            for i, route in enumerate(data.get('routes', [])):
                total_routes += 1
                print(f"\n📍 Route {i+1}: {route.get('destination', 'N/A')}")
                
                polyline = route.get('route_polyline', [])
                polyline_points = len(polyline)
                
                print(f"   Polyline Points: {polyline_points}")
                
                if polyline_points > 2:
                    realistic_routes += 1
                    print(f"   ✅ Realistic polyline detected")
                    print(f"   📍 Start: {polyline[0]}")
                    print(f"   📍 Middle: {polyline[polyline_points//2]}")
                    print(f"   📍 End: {polyline[-1]}")
                    
                    # Check if format is correct for Leaflet
                    if all('lat' in p and 'lng' in p for p in polyline):
                        print(f"   ✅ Correct format for Leaflet Polyline")
                    else:
                        print(f"   ❌ Wrong format for Leaflet Polyline")
                else:
                    print(f"   ❌ Still straight line")
                
                # Check road segments
                road_segments = route.get('road_segments', [])
                print(f"   Road Segments: {len(road_segments)}")
                
                for j, segment in enumerate(road_segments[:2]):  # Show first 2
                    print(f"      {j+1}. {segment.get('road_name', 'N/A')}")
                    print(f"         Length: {segment.get('length_km', 'N/A')} km")
                    print(f"         Traffic: {segment.get('traffic_level', 'N/A')}")
            
            print(f"\n📊 Summary:")
            print(f"   Total Routes: {total_routes}")
            print(f"   Realistic Routes: {realistic_routes}")
            print(f"   Success Rate: {(realistic_routes/total_routes*100):.1f}%")
            
            if realistic_routes == total_routes:
                print(f"   ✅ All routes are realistic!")
                return True
            else:
                print(f"   ⚠️ Some routes still straight lines")
                return False
            
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_frontend_ready():
    """Test if frontend is ready for realistic polyline"""
    print("\n🎨 Testing Frontend Readiness")
    print("=" * 35)
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Frontend is accessible")
            print(f"   URL: http://localhost:3000")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"❌ Frontend error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to frontend: {e}")
        print(f"   Make sure to run: cd frontend && npm start")
        return False

def create_browser_test_script():
    """Create JavaScript test script for browser console"""
    print("\n🌐 Creating Browser Test Script")
    print("=" * 35)
    
    test_script = """
// Test Integrated Realistic Polyline - Browser Console
console.log("Testing Integrated Realistic Polyline...");

// Test 1: Check API Response
async function testAPIPolyline() {
    try {
        const response = await fetch('http://localhost:8000/api/simple-pt-sanghiang-data');
        const data = await response.json();
        
        console.log("API Response received");
        console.log("Routes:", data.routes?.length || 0);
        
        let realisticCount = 0;
        data.routes?.forEach((route, index) => {
            const points = route.route_polyline?.length || 0;
            console.log(`Route ${index + 1} (${route.destination}): ${points} points`);
            
            if (points > 2) {
                realisticCount++;
                console.log(`   Realistic polyline`);
            } else {
                console.log(`   Straight line`);
            }
        });
        
        console.log(`Summary: ${realisticCount}/${data.routes?.length} realistic routes`);
        return realisticCount === data.routes?.length;
    } catch (error) {
        console.error("API Error:", error);
        return false;
    }
}

// Test 2: Check Map Rendering
function testMapRendering() {
    const map = document.querySelector('.leaflet-container')?._leaflet_map;
    if (!map) {
        console.log("No map found");
        return false;
    }
    
    const polylines = [];
    map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
            polylines.push(layer);
        }
    });
    
    console.log(`Found ${polylines.length} polylines on map`);
    
    let realisticCount = 0;
    polylines.forEach((polyline, index) => {
        const positions = polyline.getLatLngs();
        console.log(`   Polyline ${index + 1}: ${positions.length} points`);
        
        if (positions.length > 2) {
            realisticCount++;
            console.log(`   Realistic curves`);
        } else {
            console.log(`   Straight line`);
        }
    });
    
    console.log(`Map Summary: ${realisticCount}/${polylines.length} realistic polylines`);
    return realisticCount === polylines.length;
}

// Run tests
async function runIntegratedTests() {
    console.log("Running Integrated Tests...");
    
    const apiOk = await testAPIPolyline();
    const mapOk = testMapRendering();
    
    console.log("Results:");
    console.log(`   API: ${apiOk ? 'OK' : 'FAILED'}`);
    console.log(`   Map: ${mapOk ? 'OK' : 'FAILED'}`);
    
    if (apiOk && mapOk) {
        console.log("All tests passed! Realistic polyline is working!");
    } else {
        console.log("Some issues detected - check logs above");
    }
}

// Auto-run
runIntegratedTests();
"""
    
    # Save to file with UTF-8 encoding
    with open("browser_test_script.js", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print(f"Browser test script created!")
    print(f"   File: browser_test_script.js")
    print(f"   Copy and paste into browser console to test")

def show_integration_instructions():
    """Show integration instructions"""
    print("\n📋 Integration Instructions")
    print("=" * 35)
    
    print("1. 🚀 Start Backend:")
    print("   cd vrp_rl_project")
    print("   python run_server.py")
    print("")
    
    print("2. 🎨 Start Frontend:")
    print("   cd frontend")
    print("   npm start")
    print("")
    
    print("3. 🔍 Test Integration:")
    print("   python test_integrated_realistic.py")
    print("")
    
    print("4. 🌐 Test in Browser:")
    print("   Open: http://localhost:3000")
    print("   Press F12 → Console")
    print("   Copy browser_test_script.js content")
    print("")
    
    print("5. ✅ Expected Results:")
    print("   - Backend: 4 routes with 41+ polyline points each")
    print("   - Frontend: Curved routes on map (not straight lines)")
    print("   - Console: Realistic polyline detected messages")

def main():
    """Main function"""
    print("🚀 Test Integrated Realistic Polyline - PT. Sanghiang Perkasa VRP")
    print("=" * 70)
    
    # Step 1: Test backend realistic polyline
    backend_ok = test_backend_realistic_polyline()
    
    # Step 2: Test frontend readiness
    frontend_ok = test_frontend_ready()
    
    # Step 3: Create browser test script
    create_browser_test_script()
    
    # Step 4: Show instructions
    show_integration_instructions()
    
    print("\n" + "=" * 70)
    print("🎯 Integration Summary:")
    print(f"   Backend: {'✅' if backend_ok else '❌'} Realistic polyline")
    print(f"   Frontend: {'✅' if frontend_ok else '❌'} Ready")
    print(f"   Browser Test: ✅ Script created")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Integration is ready!")
        print("🔧 Next steps:")
        print("   1. Start backend: cd vrp_rl_project && python run_server.py")
        print("   2. Start frontend: cd frontend && npm start")
        print("   3. Open browser: http://localhost:3000")
        print("   4. Check console for realistic polyline messages")
        print("   5. Verify curved routes on map")
    else:
        print("\n🔧 Issues detected - follow instructions above")

if __name__ == "__main__":
    main() 