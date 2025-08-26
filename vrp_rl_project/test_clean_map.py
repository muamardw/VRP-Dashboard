#!/usr/bin/env python3
"""
Test Clean Map - PT. Sanghiang Perkasa VRP
Memastikan map bersih dan tidak berantakan
"""

import requests
import json
import time

def test_clean_map():
    print("🧹 Test Clean Map - PT. Sanghiang Perkasa VRP")
    print("=" * 50)
    
    # Test backend API
    print("\n🔍 Testing Backend API")
    print("-" * 25)
    
    try:
        response = requests.get('http://localhost:8000/api/simple-pt-sanghiang-data', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API responding")
            print(f"   Routes: {len(data.get('routes', []))}")
            
            # Check each route
            for i, route in enumerate(data.get('routes', [])):
                print(f"\n📍 Route {i+1}: {route.get('destination', 'Unknown')}")
                
                # Check polyline
                polyline = route.get('route_polyline', [])
                print(f"   Polyline Points: {len(polyline)}")
                
                if len(polyline) > 2:
                    print("   ✅ Realistic polyline (will show curves)")
                else:
                    print("   ❌ Straight line only")
                
                # Check road segments
                road_segments = route.get('road_segments', [])
                print(f"   Road Segments: {len(road_segments)}")
                
                for j, segment in enumerate(road_segments[:2]):  # Show first 2
                    print(f"      {j+1}. {segment.get('road_name', 'Unknown')}")
                    print(f"         Length: {segment.get('length_km', segment.get('length', 0))} km")
                    print(f"         Traffic: {segment.get('traffic_level', 'unknown')}")
                
                # Check traffic level
                traffic = route.get('traffic_level', 'unknown')
                print(f"   Traffic Level: {traffic}")
                
                # Check weather
                weather = route.get('weather', {})
                print(f"   Weather: {weather.get('description', 'unknown')}")
                
        else:
            print(f"❌ Backend API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend API error: {e}")
        return False
    
    # Test frontend
    print("\n🌐 Testing Frontend")
    print("-" * 20)
    
    try:
        response = requests.get('http://localhost:3000', timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False
    
    # Create browser test
    print("\n🎯 Creating Browser Test")
    print("-" * 25)
    
    browser_test = """
// Test Clean Map - Browser Console
console.log("Testing Clean Map...");

// Test 1: Check if map is clean
function checkMapCleanliness() {
    const map = document.querySelector('.leaflet-container')?._leaflet_map;
    if (!map) {
        console.log("❌ No map found");
        return false;
    }
    
    let markerCount = 0;
    let polylineCount = 0;
    
    map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
            markerCount++;
        } else if (layer instanceof L.Polyline) {
            polylineCount++;
        }
    });
    
    console.log(`Map Elements:`);
    console.log(`   Markers: ${markerCount}`);
    console.log(`   Polylines: ${polylineCount}`);
    
    // Should have: 1 depot + 4 destinations + 4 vehicles + 4 traffic + 4 weather = 17 markers
    // Should have: 4 polylines
    const expectedMarkers = 17;
    const expectedPolylines = 4;
    
    if (markerCount === expectedMarkers && polylineCount === expectedPolylines) {
        console.log("✅ Map is clean and organized");
        return true;
    } else {
        console.log("❌ Map has unexpected elements");
        return false;
    }
}

// Test 2: Check traffic colors
function checkTrafficColors() {
    const map = document.querySelector('.leaflet-container')?._leaflet_map;
    if (!map) return false;
    
    let redMarkers = 0;
    let yellowMarkers = 0;
    let greenMarkers = 0;
    
    map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
            const icon = layer.getIcon();
            if (icon && icon.options && icon.options.className) {
                const className = icon.options.className;
                if (className.includes('traffic-heavy')) redMarkers++;
                else if (className.includes('traffic-moderate')) yellowMarkers++;
                else if (className.includes('traffic-light')) greenMarkers++;
            }
        }
    });
    
    console.log(`Traffic Colors:`);
    console.log(`   Red (Heavy): ${redMarkers}`);
    console.log(`   Yellow (Moderate): ${yellowMarkers}`);
    console.log(`   Green (Light): ${greenMarkers}`);
    
    return redMarkers > 0 || yellowMarkers > 0 || greenMarkers > 0;
}

// Test 3: Check polyline curves
function checkPolylineCurves() {
    const map = document.querySelector('.leaflet-container')?._leaflet_map;
    if (!map) return false;
    
    let realisticCount = 0;
    let totalPolylines = 0;
    
    map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
            totalPolylines++;
            const positions = layer.getLatLngs();
            if (positions.length > 2) {
                realisticCount++;
                console.log(`   Polyline ${totalPolylines}: ${positions.length} points (Realistic)`);
            } else {
                console.log(`   Polyline ${totalPolylines}: ${positions.length} points (Straight)`);
            }
        }
    });
    
    console.log(`Polyline Summary: ${realisticCount}/${totalPolylines} realistic`);
    return realisticCount === totalPolylines;
}

// Run all tests
function runCleanMapTests() {
    console.log("Running Clean Map Tests...");
    
    const mapClean = checkMapCleanliness();
    const colorsOk = checkTrafficColors();
    const curvesOk = checkPolylineCurves();
    
    console.log("\\nResults:");
    console.log(`   Map Clean: ${mapClean ? '✅' : '❌'}`);
    console.log(`   Traffic Colors: ${colorsOk ? '✅' : '❌'}`);
    console.log(`   Polyline Curves: ${curvesOk ? '✅' : '❌'}`);
    
    if (mapClean && colorsOk && curvesOk) {
        console.log("🎉 All tests passed! Map is clean and working!");
    } else {
        console.log("⚠️ Some issues detected");
    }
}

// Auto-run
runCleanMapTests();
"""
    
    with open("browser_clean_map_test.js", "w", encoding="utf-8") as f:
        f.write(browser_test)
    
    print("✅ Browser test script created: browser_clean_map_test.js")
    print("   Copy and paste into browser console to test")
    
    print("\n📋 Instructions:")
    print("1. Refresh browser: http://localhost:3000")
    print("2. Open browser console (F12)")
    print("3. Copy and paste browser_clean_map_test.js content")
    print("4. Check results in console")
    
    return True

if __name__ == "__main__":
    test_clean_map() 