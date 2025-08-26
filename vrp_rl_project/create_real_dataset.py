#!/usr/bin/env python3
"""
Script untuk mengkonversi data real PT. Sanghiang Perkasa (4 destinasi) 
menjadi format dataset yang dapat digunakan untuk training DQN VRP.
"""

import pandas as pd
import os

def create_real_dataset():
    """Buat dataset real dari data perusahaan"""
    
    # Data real PT. Sanghiang Perkasa (4 destinasi)
    real_data = [
        {"rute": "G-Bogor-G", "kode": "C25", "jarak_km": 60, "kapasitas_kg": 2000, "beban_kg": 2000, "utilitas_pct": 100},
        {"rute": "G-Tangerang-G", "kode": "C26", "jarak_km": 55, "kapasitas_kg": 1000, "beban_kg": 700, "utilitas_pct": 70},
        {"rute": "G-Jakarta-G", "kode": "C27", "jarak_km": 17, "kapasitas_kg": 2000, "beban_kg": 1700, "utilitas_pct": 85},
        {"rute": "G-Bekasi-G", "kode": "C28", "jarak_km": 10, "kapasitas_kg": 1000, "beban_kg": 500, "utilitas_pct": 50},
    ]
    
    # Koordinat GPS real (sesuai aplikasi)
    coords = {
        "Depot": {"lat": -6.1702, "lon": 106.9417},      # Pulo Gadung, Jakarta Timur
        "Bogor": {"lat": -6.5950, "lon": 106.8167},      # Jl. Wangun no. 216 Sindangsari Bogor Timur
        "Tangerang": {"lat": -6.1783, "lon": 106.6319},  # Jl. Serenade Lake No.15, Kelapa Dua
        "Jakarta": {"lat": -6.1702, "lon": 106.9417},    # Jl. Pulo Lentut no. 10, Pulo Gadung
        "Bekasi": {"lat": -6.2383, "lon": 106.9756},     # Jl. Jakasetia no. 27 B, Bekasi Selatan
    }
    
    # Mapping nama rute ke kota
    route_to_city = {
        "G-Bogor-G": "Bogor",
        "G-Tangerang-G": "Tangerang", 
        "G-Jakarta-G": "Jakarta",
        "G-Bekasi-G": "Bekasi",
    }
    
    print("🚚 Membuat Dataset Real PT. Sanghiang Perkasa")
    print("=" * 50)
    
    # Buat dataset untuk RL
    rows = []
    
    # Baris 0: Depot
    rows.append({
        "customer_id": 0,
        "latitude": coords["Depot"]["lat"],
        "longitude": coords["Depot"]["lon"],
        "demand": 0.0,  # Depot tidak punya demand
        "time_window_start": 8.0,
        "time_window_end": 24.0,
        "service_time": 0.0,
    })
    
    print("📍 Depot: Pulo Gadung, Jakarta Timur")
    print(f"   Koordinat: ({coords['Depot']['lat']}, {coords['Depot']['lon']})")
    print(f"   Demand: 0 kg")
    
    # Baris 1-4: Destinasi real
    for i, data in enumerate(real_data):
        city = route_to_city[data["rute"]]
        rows.append({
            "customer_id": i + 1,
            "latitude": coords[city]["lat"],
            "longitude": coords[city]["lon"],
            "demand": float(data["beban_kg"]),
            "time_window_start": 8.0,
            "time_window_end": 24.0,
            "service_time": 0.5,  # 30 menit per destinasi
        })
        
        print(f"\n📍 {city}: {data['rute']} ({data['kode']})")
        print(f"   Koordinat: ({coords[city]['lat']}, {coords[city]['lon']})")
        print(f"   Jarak: {data['jarak_km']} km")
        print(f"   Demand: {data['beban_kg']} kg")
        print(f"   Kapasitas: {data['kapasitas_kg']} kg")
        print(f"   Utilitas: {data['utilitas_pct']}%")
    
    # Simpan ke CSV
    real_customers_df = pd.DataFrame(rows)
    
    # Buat folder data jika belum ada
    os.makedirs("data", exist_ok=True)
    
    # Simpan dataset real
    real_customers_df.to_csv("data/real_shipments.csv", index=False)
    
    print(f"\n✅ Dataset real berhasil dibuat!")
    print(f"📁 File: data/real_shipments.csv")
    print(f"📊 Total baris: {len(real_customers_df)} (1 depot + 4 destinasi)")
    print(f"🎯 Format: Siap untuk training DQN VRP")
    
    print(f"\n📋 Ringkasan Dataset:")
    print(real_customers_df.to_string(index=False))
    
    return real_customers_df

def compare_datasets():
    """Bandingkan dataset real vs simulasi"""
    
    print("\n" + "="*60)
    print("📊 PERBANDINGAN DATASET")
    print("="*60)
    
    # Load dataset simulasi (jika ada)
    if os.path.exists("data/simulated_shipments.csv"):
        sim_df = pd.read_csv("data/simulated_shipments.csv")
        print(f"📈 Dataset Simulasi:")
        print(f"   - Jumlah customer: {len(sim_df)}")
        print(f"   - Range demand: {sim_df['demand'].min():.1f} - {sim_df['demand'].max():.1f} kg")
        print(f"   - Total demand: {sim_df['demand'].sum():.1f} kg")
    
    # Load dataset real
    if os.path.exists("data/real_shipments.csv"):
        real_df = pd.read_csv("data/real_shipments.csv")
        print(f"\n🎯 Dataset Real:")
        print(f"   - Jumlah customer: {len(real_df)} (1 depot + 4 destinasi)")
        print(f"   - Range demand: {real_df['demand'].min():.1f} - {real_df['demand'].max():.1f} kg")
        print(f"   - Total demand: {real_df['demand'].sum():.1f} kg")
        
        # Hitung total beban dari data real
        total_beban = 2000 + 700 + 1700 + 500  # dari tabel perusahaan
        print(f"   - Total beban (dari tabel): {total_beban} kg")
    
    print(f"\n💡 Keuntungan Dataset Real:")
    print(f"   ✅ Data operasional nyata")
    print(f"   ✅ Training lebih cepat (4 vs 50 customer)")
    print(f"   ✅ Koordinat GPS real")
    print(f"   ✅ Jarak antar kota real")
    print(f"   ✅ Langsung dapat diterapkan")

if __name__ == "__main__":
    # Buat dataset real
    real_df = create_real_dataset()
    
    # Bandingkan dengan dataset simulasi
    compare_datasets()
    
    print(f"\n🎉 Selesai! Dataset real siap untuk training DQN VRP.")
    print(f"📝 Selanjutnya: Gunakan 'data/real_shipments.csv' untuk training.") 