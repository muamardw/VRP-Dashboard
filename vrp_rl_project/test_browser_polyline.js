// Test Browser Polyline - PT. Sanghiang Perkasa VRP
// Script untuk test polyline di browser console

console.log("🚀 Test Browser Polyline - PT. Sanghiang Perkasa VRP");
console.log("=" * 60);

// Function to test API response
async function testAPIPolyline() {
    try {
        console.log("🔍 Testing API Polyline Response...");
        
        const response = await fetch('http://localhost:8000/api/simple-pt-sanghiang-data');
        const data = await response.json();
        
        console.log("✅ API Response received");
        console.log("📊 Data:", data);
        
        if (data.routes && data.routes.length > 0) {
            data.routes.forEach((route, index) => {
                console.log(`\n📍 Route ${index + 1} (${route.destination}):`);
                console.log(`   Polyline points: ${route.route_polyline?.length || 0}`);
                
                if (route.route_polyline && route.route_polyline.length > 0) {
                    console.log(`   First point:`, route.route_polyline[0]);
                    console.log(`   Middle point:`, route.route_polyline[Math.floor(route.route_polyline.length/2)]);
                    console.log(`   Last point:`, route.route_polyline[route.route_polyline.length-1]);
                    
                    // Check if polyline is realistic (more than 2 points)
                    if (route.route_polyline.length > 2) {
                        console.log(`   ✅ Realistic polyline detected`);
                        
                        // Check format for Leaflet
                        const validPoints = route.route_polyline.filter(p => 
                            p && typeof p.lat === 'number' && typeof p.lng === 'number'
                        );
                        console.log(`   Valid points: ${validPoints.length}/${route.route_polyline.length}`);
                        
                        if (validPoints.length === route.route_polyline.length) {
                            console.log(`   ✅ All points valid for Leaflet Polyline`);
                        } else {
                            console.log(`   ❌ Some points invalid for Leaflet Polyline`);
                        }
                    } else {
                        console.log(`   ❌ Still straight line`);
                    }
                } else {
                    console.log(`   ❌ No polyline data`);
                }
                
                // Check road segments
                if (route.road_segments && route.road_segments.length > 0) {
                    console.log(`   🛣️ Road segments: ${route.road_segments.length}`);
                    route.road_segments.slice(0, 2).forEach((segment, i) => {
                        console.log(`      ${i+1}. ${segment.road_name}`);
                        console.log(`         Length: ${segment.length_km} km`);
                        console.log(`         Traffic: ${segment.traffic_level}`);
                    });
                }
            });
        }
        
        return data;
    } catch (error) {
        console.error("❌ Error testing API:", error);
        return null;
    }
}

// Function to test Leaflet Polyline rendering
function testLeafletPolyline() {
    console.log("\n🔄 Testing Leaflet Polyline Rendering...");
    
    // Get map instance
    const map = window.map || document.querySelector('.leaflet-container')?._leaflet_map;
    
    if (!map) {
        console.log("❌ No map instance found");
        return;
    }
    
    console.log("✅ Map instance found");
    
    // Get all polylines on map
    const polylines = [];
    map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
            polylines.push(layer);
        }
    });
    
    console.log(`📍 Found ${polylines.length} polylines on map`);
    
    polylines.forEach((polyline, index) => {
        const positions = polyline.getLatLngs();
        console.log(`   Polyline ${index + 1}:`);
        console.log(`      Points: ${positions.length}`);
        console.log(`      Color: ${polyline.options.color}`);
        console.log(`      Weight: ${polyline.options.weight}`);
        
        if (positions.length > 2) {
            console.log(`      ✅ Realistic polyline with curves`);
            console.log(`      📍 Start:`, positions[0]);
            console.log(`      📍 Middle:`, positions[Math.floor(positions.length/2)]);
            console.log(`      📍 End:`, positions[positions.length-1]);
        } else {
            console.log(`      ❌ Still straight line`);
        }
    });
}

// Function to force realistic polyline
function forceRealisticPolyline() {
    console.log("\n🔧 Forcing Realistic Polyline...");
    
    // Get map instance
    const map = window.map || document.querySelector('.leaflet-container')?._leaflet_map;
    
    if (!map) {
        console.log("❌ No map instance found");
        return;
    }
    
    // Remove existing polylines
    map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
            map.removeLayer(layer);
        }
    });
    
    console.log("✅ Removed existing polylines");
    
    // Create realistic polyline data
    const realisticPolyline = [
        {lat: -6.2088, lng: 106.8456},  // Jakarta
        {lat: -6.25, lng: 106.85},      // Curve 1
        {lat: -6.30, lng: 106.86},      // Curve 2
        {lat: -6.35, lng: 106.87},      // Curve 3
        {lat: -6.40, lng: 106.88},      // Curve 4
        {lat: -6.45, lng: 106.89},      // Curve 5
        {lat: -6.50, lng: 106.90},      // Curve 6
        {lat: -6.55, lng: 106.91},      // Curve 7
        {lat: -6.595, lng: 106.8167}    // Bogor
    ];
    
    // Add realistic polyline to map
    const polyline = L.polyline(realisticPolyline.map(p => [p.lat, p.lng]), {
        color: '#ff0000',
        weight: 4,
        opacity: 0.8
    }).addTo(map);
    
    console.log("✅ Added realistic polyline with curves");
    console.log(`   Points: ${realisticPolyline.length}`);
    console.log(`   Color: Red`);
    console.log(`   Weight: 4`);
}

// Function to debug current polyline data
function debugCurrentPolyline() {
    console.log("\n🔍 Debugging Current Polyline Data...");
    
    // Check if React component has polyline data
    const reactComponent = document.querySelector('[data-testid="pt-sanghiang-dashboard"]') || 
                          document.querySelector('.dashboard-container');
    
    if (reactComponent) {
        console.log("✅ React component found");
        
        // Try to access component state
        const componentState = reactComponent._reactInternalFiber || 
                             reactComponent._reactInternalInstance;
        
        if (componentState) {
            console.log("✅ Component state accessible");
            console.log("📊 Component state:", componentState);
        } else {
            console.log("❌ Component state not accessible");
        }
    } else {
        console.log("❌ React component not found");
    }
    
    // Check for any polyline data in global scope
    if (window.ptSanghiangData) {
        console.log("✅ Global data found:", window.ptSanghiangData);
    }
    
    // Check for any polyline elements
    const polylineElements = document.querySelectorAll('.leaflet-interactive');
    console.log(`📍 Found ${polylineElements.length} polyline elements`);
}

// Main test function
async function runPolylineTests() {
    console.log("🚀 Running Polyline Tests...");
    console.log("=" * 40);
    
    // Test 1: API Response
    const apiData = await testAPIPolyline();
    
    // Test 2: Leaflet Rendering
    testLeafletPolyline();
    
    // Test 3: Debug Current Data
    debugCurrentPolyline();
    
    // Test 4: Force Realistic (optional)
    console.log("\n🔧 To force realistic polyline, run:");
    console.log("   forceRealisticPolyline()");
    
    console.log("\n" + "=" * 40);
    console.log("🎯 Test Summary:");
    console.log(`   ✅ API Response: ${apiData ? 'OK' : 'FAILED'}`);
    console.log(`   ✅ Leaflet Rendering: Checked`);
    console.log(`   ✅ Debug Data: Checked`);
    
    if (apiData && apiData.routes && apiData.routes.length > 0) {
        const firstRoute = apiData.routes[0];
        const polylinePoints = firstRoute.route_polyline?.length || 0;
        
        if (polylinePoints > 2) {
            console.log("🎉 Realistic polyline detected in API!");
            console.log("🔧 If frontend still shows straight lines:");
            console.log("   1. Clear browser cache (Ctrl+Shift+R)");
            console.log("   2. Check browser console for errors");
            console.log("   3. Verify polyline data in Network tab");
            console.log("   4. Check if Leaflet Polyline is rendering correctly");
        } else {
            console.log("❌ Still straight line in API");
            console.log("🔧 Backend needs to be updated");
        }
    }
}

// Export functions for manual testing
window.testAPIPolyline = testAPIPolyline;
window.testLeafletPolyline = testLeafletPolyline;
window.forceRealisticPolyline = forceRealisticPolyline;
window.debugCurrentPolyline = debugCurrentPolyline;
window.runPolylineTests = runPolylineTests;

// Auto-run tests
console.log("🔧 Auto-running polyline tests...");
runPolylineTests();

console.log("\n🔧 Manual test commands:");
console.log("   runPolylineTests() - Run all tests");
console.log("   testAPIPolyline() - Test API response");
console.log("   testLeafletPolyline() - Test Leaflet rendering");
console.log("   forceRealisticPolyline() - Force realistic polyline");
console.log("   debugCurrentPolyline() - Debug current data"); 