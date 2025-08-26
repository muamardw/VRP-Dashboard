#!/usr/bin/env python3
"""
Traffic Simulation Demo untuk PT. Sanghiang Perkasa
Menampilkan data traffic simulasi dengan berbagai skenario
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

class TrafficSimulationDemo:
    def __init__(self):
        self.locations = {
            "Jakarta": (-6.2088, 106.8456),
            "Bogor": (-6.5950, 106.8167),
            "Tangerang": (-6.1783, 106.6319),
            "Bekasi": (-6.2383, 106.9756),
            "Depok": (-6.4025, 106.7942),
            "Bandung": (-6.9175, 107.6191)
        }
        
        self.traffic_scenarios = {
            "low": {
                "ratio_range": (1.0, 1.19),
                "description": "Lancar",
                "color": "🟢",
                "impact_factor": 1.0
            },
            "medium": {
                "ratio_range": (1.2, 1.49),
                "description": "Sedang",
                "color": "🟡", 
                "impact_factor": 1.3
            },
            "high": {
                "ratio_range": (1.5, 2.5),
                "description": "Macet",
                "color": "🔴",
                "impact_factor": 1.8
            }
        }

    def simulate_traffic_data(self, origin: str, destination: str, scenario: str = "medium") -> Dict:
        """Simulasi data traffic antara dua lokasi"""
        
        # Base travel times (menit)
        base_times = {
            ("Jakarta", "Bogor"): 60,
            ("Jakarta", "Tangerang"): 45,
            ("Jakarta", "Bekasi"): 30,
            ("Jakarta", "Depok"): 40,
            ("Jakarta", "Bandung"): 120,
            ("Bogor", "Bandung"): 90,
            ("Tangerang", "Bekasi"): 75
        }
        
        # Get base time or calculate from distance
        route_key = (origin, destination)
        if route_key in base_times:
            base_time = base_times[route_key]
        else:
            # Calculate approximate time based on distance
            distance = self._calculate_distance(
                self.locations[origin], 
                self.locations[destination]
            )
            base_time = distance * 2  # 2 menit per km
        
        # Apply traffic scenario
        scenario_data = self.traffic_scenarios[scenario]
        ratio = scenario_data["ratio_range"][0] + (scenario_data["ratio_range"][1] - scenario_data["ratio_range"][0]) * 0.5
        
        traffic_time = int(base_time * ratio)
        
        return {
            "origin": origin,
            "destination": destination,
            "base_time_minutes": base_time,
            "traffic_time_minutes": traffic_time,
            "traffic_ratio": round(ratio, 2),
            "traffic_level": scenario,
            "traffic_description": scenario_data["description"],
            "traffic_color": scenario_data["color"],
            "impact_factor": scenario_data["impact_factor"],
            "distance_km": round(self._calculate_distance(
                self.locations[origin], 
                self.locations[destination]
            ), 1)
        }

    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Hitung jarak antara dua koordinat (km)"""
        import math
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        # Haversine formula
        R = 6371  # Earth's radius in km
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c

    def run_traffic_simulation(self):
        """Jalankan simulasi traffic untuk semua rute"""
        
        print("🚗 SIMULASI TRAFFIC PT. SANGHIANG PERKASA 🚗")
        print("=" * 60)
        print(f"Waktu Simulasi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Test semua skenario traffic
        scenarios = ["low", "medium", "high"]
        
        for scenario in scenarios:
            print(f"\n📊 SKENARIO TRAFFIC: {scenario.upper()}")
            print("-" * 40)
            
            # Test beberapa rute utama
            routes = [
                ("Jakarta", "Bogor"),
                ("Jakarta", "Tangerang"), 
                ("Jakarta", "Bekasi"),
                ("Jakarta", "Bandung")
            ]
            
            for origin, destination in routes:
                traffic_data = self.simulate_traffic_data(origin, destination, scenario)
                
                print(f"{traffic_data['traffic_color']} {origin} → {destination}")
                print(f"   Jarak: {traffic_data['distance_km']} km")
                print(f"   Waktu Normal: {traffic_data['base_time_minutes']} menit")
                print(f"   Waktu dengan Traffic: {traffic_data['traffic_time_minutes']} menit")
                print(f"   Traffic Ratio: {traffic_data['traffic_ratio']}x")
                print(f"   Level: {traffic_data['traffic_description']}")
                print(f"   Impact Factor: {traffic_data['impact_factor']}")
                print()

    def show_realistic_traffic_example(self):
        """Tampilkan contoh data traffic yang realistis"""
        
        print("\n🎯 CONTOH DATA TRAFFIC REALISTIS")
        print("=" * 50)
        
        # Simulasi traffic jam sibuk
        print("🌆 JAM SIBUK (07:00 - 09:00)")
        print("-" * 30)
        
        rush_hour_data = {
            "Jakarta → Bogor": self.simulate_traffic_data("Jakarta", "Bogor", "high"),
            "Jakarta → Tangerang": self.simulate_traffic_data("Jakarta", "Tangerang", "high"),
            "Jakarta → Bekasi": self.simulate_traffic_data("Jakarta", "Bekasi", "medium"),
            "Bogor → Bandung": self.simulate_traffic_data("Bogor", "Bandung", "low")
        }
        
        for route, data in rush_hour_data.items():
            print(f"{data['traffic_color']} {route}")
            print(f"   Waktu: {data['base_time_minutes']} → {data['traffic_time_minutes']} menit")
            print(f"   Delay: +{data['traffic_time_minutes'] - data['base_time_minutes']} menit")
            print(f"   Status: {data['traffic_description']}")
            print()
        
        # Simulasi traffic normal
        print("🌅 JAM NORMAL (10:00 - 16:00)")
        print("-" * 30)
        
        normal_data = {
            "Jakarta → Bogor": self.simulate_traffic_data("Jakarta", "Bogor", "medium"),
            "Jakarta → Tangerang": self.simulate_traffic_data("Jakarta", "Tangerang", "low"),
            "Jakarta → Bekasi": self.simulate_traffic_data("Jakarta", "Bekasi", "low"),
            "Bogor → Bandung": self.simulate_traffic_data("Bogor", "Bandung", "low")
        }
        
        for route, data in normal_data.items():
            print(f"{data['traffic_color']} {route}")
            print(f"   Waktu: {data['base_time_minutes']} → {data['traffic_time_minutes']} menit")
            print(f"   Delay: +{data['traffic_time_minutes'] - data['base_time_minutes']} menit")
            print(f"   Status: {data['traffic_description']}")
            print()

    def generate_traffic_json_data(self):
        """Generate data traffic dalam format JSON untuk testing"""
        
        print("\n📄 GENERATING TRAFFIC JSON DATA")
        print("=" * 40)
        
        traffic_data = {
            "simulation_time": datetime.now().isoformat(),
            "traffic_scenarios": {},
            "route_analysis": []
        }
        
        # Generate data untuk semua kombinasi rute dan skenario
        for scenario in ["low", "medium", "high"]:
            traffic_data["traffic_scenarios"][scenario] = []
            
            for origin in self.locations.keys():
                for destination in self.locations.keys():
                    if origin != destination:
                        route_data = self.simulate_traffic_data(origin, destination, scenario)
                        traffic_data["traffic_scenarios"][scenario].append(route_data)
        
        # Simpan ke file
        filename = f"traffic_simulation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(traffic_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data traffic disimpan ke: {filename}")
        print(f"📊 Total routes: {len(traffic_data['traffic_scenarios']['medium'])}")
        
        return traffic_data

def main():
    """Main function untuk menjalankan demo"""
    
    demo = TrafficSimulationDemo()
    
    print("🚗 TRAFFIC SIMULATION DEMO - PT. SANGHIANG PERKASA 🚗")
    print("=" * 60)
    
    # Jalankan simulasi traffic
    demo.run_traffic_simulation()
    
    # Tampilkan contoh realistis
    demo.show_realistic_traffic_example()
    
    # Generate JSON data
    demo.generate_traffic_json_data()
    
    print("\n🎉 SIMULASI TRAFFIC SELESAI!")
    print("=" * 60)

if __name__ == "__main__":
    main() 