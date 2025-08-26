#!/usr/bin/env python3
"""
Script untuk verifikasi jarak dari Cikampek ke 4 destinasi Jabodetabek
"""

import math

# Koordinat Depot (PT. Sanghiang Perkasa) - Jl. Raya Bekasi KM 25 Cakung Jakarta Timur
DEPOT_LAT = -6.1702  # Jakarta Timur area
DEPOT_LNG = 106.9417  # Jl. Raya Bekasi KM 25 Cakung

# Data destinasi dengan koordinat yang sudah diperbarui
DESTINATIONS = {
    'Bogor': {
        'coordinates': {'lat': -6.5950, 'lng': 106.8167},
        'address': 'Jl. Wangun no. 216 Sindangsari Bogor Timur 16720',
        'original_distance': 60
    },
    'Tangerang': {
        'coordinates': {'lat': -6.1783, 'lng': 106.6319},
        'address': 'Jl. Serenade Lake No.15, Pakulonan Bar., Kec. Klp. Dua, Kota Tangerang, Banten 15810',
        'original_distance': 55
    },
    'Jakarta': {
        'coordinates': {'lat': -6.1702, 'lng': 106.9417},
        'address': 'Jl. Pulo Lentut no. 10, Kawasan industri Pulo Gadung, Jakarta Timur 13920',
        'original_distance': 0.5
    },
    'Bekasi': {
        'coordinates': {'lat': -6.2383, 'lng': 106.9756},
        'address': 'Jl. Jakasetia no. 27 B, Kp. Poncol, Kel. Jakasetia, Bekasi Selatan 17423',
        'original_distance': 10
    }
}

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return distance

def main():
    print("🔍 VERIFIKASI JARAK DARI JAKARTA TIMUR KE 4 DESTINASI JABODETABEK")
    print("=" * 70)
    print(f"📍 Depot (Jakarta Timur): {DEPOT_LAT}, {DEPOT_LNG}")
    print(f"📍 Alamat Depot: Jl. Raya Bekasi KM 25, Cakung, Jakarta Timur")
    print()
    
    updated_data = {}
    
    for city, data in DESTINATIONS.items():
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']
        original_distance = data['original_distance']
        
        # Calculate actual distance
        actual_distance = calculate_distance(DEPOT_LAT, DEPOT_LNG, lat, lng)
        
        print(f"📍 {city}:")
        print(f"   Alamat: {data['address']}")
        print(f"   Koordinat: {lat}, {lng}")
        print(f"   Jarak asli: {original_distance} km")
        print(f"   Jarak aktual: {actual_distance:.1f} km")
        print(f"   Selisih: {abs(actual_distance - original_distance):.1f} km")
        
        if abs(actual_distance - original_distance) > 5:
            print(f"   ⚠️  PERLU UPDATE: Selisih > 5 km")
        else:
            print(f"   ✅ OK: Selisih < 5 km")
        
        print()
        
        # Store updated data
        updated_data[city] = {
            'coordinates': data['coordinates'],
            'address': data['address'],
            'distance': round(actual_distance, 1),
            'capacity': 2000 if city in ['Bogor', 'Jakarta'] else 1000,
            'load': 2000 if city == 'Bogor' else (1700 if city == 'Jakarta' else (700 if city == 'Tangerang' else 500)),
            'utilization': 100 if city == 'Bogor' else (85 if city == 'Jakarta' else (70 if city == 'Tangerang' else 50))
        }
    
    print("📊 HASIL VERIFIKASI:")
    print("=" * 50)
    for city, data in updated_data.items():
        print(f"{city}: {data['distance']} km")
    
    print("\n💡 REKOMENDASI UPDATE:")
    print("=" * 30)
    for city, data in updated_data.items():
        original = DESTINATIONS[city]['original_distance']
        actual = data['distance']
        if abs(actual - original) > 5:
            print(f"   {city}: {original} km → {actual} km")
    
    return updated_data

if __name__ == "__main__":
    updated_distances = main() 