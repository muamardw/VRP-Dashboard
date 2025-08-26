#!/usr/bin/env python3
"""
Script untuk menghasilkan tabel perjalanan dari depot ke Tangerang
dengan interval 3 jam sekali untuk hari ini
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import json

def generate_tangerang_schedule():
    """Generate schedule table for depot to Tangerang trips"""
    
    # Koordinat depot dan Tangerang
    depot_coords = [-6.1857, 106.9367]  # Pulogadung, Jakarta Timur
    tangerang_coords = [-6.1783, 106.6319]  # Tangerang
    
    # Jarak tetap (55 km)
    distance_km = 55
    
    # Rute yang mungkin dilewati
    possible_routes = [
        "Tol Jakarta-Tangerang → Jl. Daan Mogot → Jl. Pajajaran",
        "Tol Jakarta-Tangerang → Jl. Raya Serpong → Jl. Pajajaran", 
        "Jl. Raya Bekasi → Jl. Raya Cikarang → Jl. Pajajaran",
        "Tol Jagorawi → Jl. Raya Bogor → Jl. Pajajaran"
    ]
    
    # Kondisi cuaca yang mungkin
    weather_conditions = [
        {"condition": "Cerah Berawan", "temp": 28, "humidity": 75},
        {"condition": "Hujan Ringan", "temp": 25, "humidity": 85},
        {"condition": "Cerah", "temp": 30, "humidity": 70},
        {"condition": "Berawan", "temp": 27, "humidity": 80},
        {"condition": "Hujan Sedang", "temp": 24, "humidity": 90},
        {"condition": "Mendung", "temp": 26, "humidity": 82}
    ]
    
    # Kondisi traffic yang mungkin
    traffic_conditions = [
        {"level": "Lancar", "color": "🟢", "eta_multiplier": 1.0},
        {"level": "Sedang", "color": "🟡", "eta_multiplier": 1.3},
        {"level": "Macet", "color": "🔴", "eta_multiplier": 1.8},
        {"level": "Sangat Macet", "color": "🔴", "eta_multiplier": 2.2}
    ]
    
    # Generate schedule untuk hari ini (24 jam, setiap 3 jam)
    today = datetime.now().date()
    schedule_data = []
    
    for hour in range(0, 24, 3):
        departure_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=hour)
        
        # Pilih kondisi cuaca dan traffic secara random
        weather = random.choice(weather_conditions)
        traffic = random.choice(traffic_conditions)
        route = random.choice(possible_routes)
        
        # Hitung ETA berdasarkan traffic
        base_eta_hours = distance_km / 45  # Kecepatan rata-rata 45 km/jam
        eta_hours = base_eta_hours * traffic["eta_multiplier"]
        
        # Format ETA
        if eta_hours < 1:
            eta_display = f"{int(eta_hours * 60)} menit"
        else:
            hours = int(eta_hours)
            minutes = int((eta_hours - hours) * 60)
            if minutes == 0:
                eta_display = f"{hours} jam"
            else:
                eta_display = f"{hours} jam {minutes} menit"
        
        schedule_data.append({
            "Jam": departure_time.strftime("%H:%M"),
            "ETA": eta_display,
            "Cuaca": f"{weather['condition']} ({weather['temp']}°C, {weather['humidity']}%)",
            "Traffic": f"{traffic['color']} {traffic['level']}",
            "Jarak": f"{distance_km} km",
            "Jalan yang Dilewati": route
        })
    
    return schedule_data

def create_schedule_table():
    """Create and display the schedule table"""
    
    print("=" * 80)
    print("📋 TABEL PERJALANAN DEPOT KE TANGERANG - HARI INI")
    print("=" * 80)
    print(f"🏢 Depot: Pulogadung, Jakarta Timur")
    print(f"📍 Tujuan: Tangerang (Jl. Pajajaran)")
    print(f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}")
    print(f"🛣️ Jarak: 55 km")
    print("=" * 80)
    
    schedule_data = generate_tangerang_schedule()
    
    # Create DataFrame
    df = pd.DataFrame(schedule_data)
    
    # Display table
    print(df.to_string(index=False, justify='left'))
    
    # Save to CSV
    filename = f"tangerang_schedule_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"\n💾 Tabel disimpan ke: {filename}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("📊 RINGKASAN PERJALANAN")
    print("=" * 80)
    
    # Count traffic conditions
    traffic_counts = {}
    for row in schedule_data:
        traffic = row['Traffic'].split(' ')[1]  # Extract traffic level
        traffic_counts[traffic] = traffic_counts.get(traffic, 0) + 1
    
    print("🚦 Kondisi Traffic:")
    for traffic, count in traffic_counts.items():
        print(f"   {traffic}: {count} kali")
    
    # Count weather conditions
    weather_counts = {}
    for row in schedule_data:
        weather = row['Cuaca'].split(' ')[0]  # Extract weather condition
        weather_counts[weather] = weather_counts.get(weather, 0) + 1
    
    print("\n🌤️ Kondisi Cuaca:")
    for weather, count in weather_counts.items():
        print(f"   {weather}: {count} kali")
    
    print(f"\n⏱️ Total Perjalanan: {len(schedule_data)} kali")
    print(f"🕐 Interval: Setiap 3 jam")
    print("=" * 80)

if __name__ == "__main__":
    create_schedule_table() 