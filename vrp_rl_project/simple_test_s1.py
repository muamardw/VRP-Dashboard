#!/usr/bin/env python3
"""
Simple Test Script untuk S1 Skripsi
Test basic functionality tanpa PyTorch
"""

import json
import math
from datetime import datetime

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points"""
    R = 6371  # Earth's radius in km
    
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def simple_vrp_test():
    """Simple VRP test untuk S1 skripsi"""
    
    print("🧪 SIMPLE VRP TEST - S1 SKRIPSI")
    print("=" * 50)
    print("4 Titik Tujuan: Jakarta, Bekasi, Bogor, Tangerang")
    print(f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Depot (Cikampek)
    depot = {"lat": -6.4194, "lng": 107.4515}
    
    # 4 Titik Tujuan
    destinations = [
        {
            "name": "Jakarta",
            "lat": -6.2088,
            "lng": 106.8456,
            "distance_km": 45.0,
            "capacity": 1000,
            "current_load": 850,
            "utilization": 85.0
        },
        {
            "name": "Bekasi", 
            "lat": -6.2349,
            "lng": 106.9896,
            "distance_km": 35.0,
            "capacity": 1200,
            "current_load": 936,
            "utilization": 78.0
        },
        {
            "name": "Bogor",
            "lat": -6.5950,
            "lng": 106.8166,
            "distance_km": 55.0,
            "capacity": 800,
            "current_load": 736,
            "utilization": 92.0
        },
        {
            "name": "Tangerang",
            "lat": -6.2024,
            "lng": 106.6527,
            "distance_km": 40.0,
            "capacity": 900,
            "current_load": 792,
            "utilization": 88.0
        }
    ]
    
    print("📊 Data Analysis:")
    print("-" * 30)
    
    total_distance = 0
    total_capacity = 0
    total_load = 0
    avg_utilization = 0
    
    for i, dest in enumerate(destinations):
        # Calculate actual distance
        actual_distance = calculate_distance(depot["lat"], depot["lng"], dest["lat"], dest["lng"])
        
        print(f"{i+1}. {dest['name']}:")
        print(f"   📍 Distance: {actual_distance:.1f} km")
        print(f"   📦 Capacity: {dest['capacity']} kg")
        print(f"   🚛 Current Load: {dest['current_load']} kg")
        print(f"   📊 Utilization: {dest['utilization']}%")
        print()
        
        total_distance += actual_distance
        total_capacity += dest['capacity']
        total_load += dest['current_load']
        avg_utilization += dest['utilization']
    
    avg_utilization /= len(destinations)
    
    print("📈 Summary Statistics:")
    print("-" * 30)
    print(f"📍 Total Distance: {total_distance:.1f} km")
    print(f"📦 Total Capacity: {total_capacity} kg")
    print(f"🚛 Total Load: {total_load} kg")
    print(f"📊 Average Utilization: {avg_utilization:.1f}%")
    print()
    
    # Simple optimization simulation
    print("🎯 Simple Route Optimization:")
    print("-" * 30)
    
    # Sort by distance (nearest first)
    sorted_by_distance = sorted(destinations, key=lambda x: x['distance_km'])
    
    print("📍 Route by Distance (Nearest First):")
    total_route_distance = 0
    for i, dest in enumerate(sorted_by_distance):
        if i == 0:
            distance = dest['distance_km']
        else:
            # Simple: add distance from previous destination
            prev_dest = sorted_by_distance[i-1]
            distance = dest['distance_km'] - prev_dest['distance_km']
            if distance < 0:
                distance = abs(distance)
        
        total_route_distance += distance
        print(f"   {i+1}. {dest['name']} ({distance:.1f} km)")
    
    print(f"   📍 Total Route Distance: {total_route_distance:.1f} km")
    print()
    
    # Sort by utilization (highest first)
    sorted_by_utilization = sorted(destinations, key=lambda x: x['utilization'], reverse=True)
    
    print("📊 Route by Utilization (Highest First):")
    for i, dest in enumerate(sorted_by_utilization):
        print(f"   {i+1}. {dest['name']} ({dest['utilization']}%)")
    
    print()
    
    # Weather simulation
    print("🌤️ Weather Impact Simulation:")
    print("-" * 30)
    
    weather_conditions = [
        {"name": "Clear Sky", "factor": 1.0},
        {"name": "Light Rain", "factor": 1.2},
        {"name": "Heavy Rain", "factor": 1.5},
        {"name": "Traffic Jam", "factor": 1.8}
    ]
    
    for weather in weather_conditions:
        adjusted_distance = total_distance * weather['factor']
        print(f"🌤️ {weather['name']}: {adjusted_distance:.1f} km (x{weather['factor']})")
    
    print()
    
    # Save results
    print("💾 Saving Results...")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "depot": depot,
        "destinations": destinations,
        "summary": {
            "total_distance": total_distance,
            "total_capacity": total_capacity,
            "total_load": total_load,
            "avg_utilization": avg_utilization
        },
        "optimization": {
            "route_by_distance": [d['name'] for d in sorted_by_distance],
            "route_by_utilization": [d['name'] for d in sorted_by_utilization],
            "total_route_distance": total_route_distance
        },
        "weather_impact": weather_conditions
    }
    
    with open('simple_vrp_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Results saved: simple_vrp_results.json")
    print()
    
    print("🎓 S1 Skripsi Analysis Complete!")
    print("📋 Key Findings:")
    print("   - 4 titik tujuan berhasil dianalisis")
    print("   - Route optimization berdasarkan jarak dan utilization")
    print("   - Weather impact pada total distance")
    print("   - Data siap untuk DQN training")

if __name__ == "__main__":
    simple_vrp_test() 