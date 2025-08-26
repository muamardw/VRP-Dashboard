"""
Data Integration untuk PT. Sanghiang Perkasa
Mengintegrasikan data rute pengiriman dari PT. Sanghiang Perkasa ke dalam sistem VRP
"""

import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass
import numpy as np

@dataclass
class RouteData:
    """Struktur data untuk rute pengiriman PT. Sanghiang Perkasa"""
    route_name: str
    branch_code: str
    distance_km: float
    capacity_kg: float
    load_kg: float
    remaining_capacity: float
    utilization_percent: float

class PTSanghiangDataProcessor:
    """Processor untuk data PT. Sanghiang Perkasa"""
    
    def __init__(self):
        self.routes_data = self._load_pt_sanghiang_data()
        self.coordinates_mapping = self._get_coordinates_mapping()
    
    def _load_pt_sanghiang_data(self) -> List[RouteData]:
        """Load data rute dari PT. Sanghiang Perkasa"""
        # Data aktual PT. Sanghiang Perkasa - Updated dengan data Jabodetabek
        PT_SANGHIANG_ROUTES = {
            'G-Bogor-G': {
                'branch_code': 'C29', 'distance': 60, 'capacity': 2000, 'load': 2000, 'remaining_capacity': 0, 'utilization': 100,
                'address': 'Jl. Wangun no. 216 Sindangsari Bogor Timur 16720', 'coordinates': {'lat': -6.5950, 'lng': 106.8167}
            },
            'G-Tangerang-G': {
                'branch_code': 'C30', 'distance': 55, 'capacity': 1000, 'load': 700, 'remaining_capacity': 300, 'utilization': 70,
                'address': 'Jl. Serenade Lake No.15, Pakulonan Bar., Kec. Klp. Dua, Kota Tangerang, Banten 15810', 'coordinates': {'lat': -6.1783, 'lng': 106.6319}
            },
            'G-Jakarta-G': {
                'branch_code': 'C27', 'distance': 0.5, 'capacity': 2000, 'load': 1700, 'remaining_capacity': 300, 'utilization': 85,
                'address': 'Jl. Pulo Lentut no. 10, Kawasan industri Pulo Gadung, Jakarta Timur 13920', 'coordinates': {'lat': -6.1702, 'lng': 106.9417}
            },
            'G-Bekasi-G': {
                'branch_code': 'C28', 'distance': 10, 'capacity': 1000, 'load': 500, 'remaining_capacity': 500, 'utilization': 50,
                'address': 'Jl. Jakasetia no. 27 B, Kp. Poncol, Kel. Jakasetia, Bekasi Selatan 17423', 'coordinates': {'lat': -6.2383, 'lng': 106.9756}
            }
        }
        
        routes = []
        for route_name, route_info in PT_SANGHIANG_ROUTES.items():
            route = RouteData(
                route_name=route_name,
                branch_code=route_info['branch_code'],
                distance_km=route_info['distance'],
                capacity_kg=route_info['capacity'],
                load_kg=route_info['load'],
                remaining_capacity=route_info['remaining_capacity'],
                utilization_percent=route_info['utilization']
            )
            routes.append(route)
        return routes
    
    def _get_coordinates_mapping(self) -> Dict[str, Tuple[float, float]]:
        """Mapping koordinat untuk setiap cabang (estimasi berdasarkan lokasi)"""
        # Koordinat estimasi untuk setiap cabang
        coordinates = {
            "C6": (-8.1845, 113.6681),    # Jember
            "C7": (-7.9839, 112.6214),    # Malang
            "C9": (-7.2575, 112.7521),    # Surabaya
            "C16": (-7.5667, 110.8167),   # Solo
            "C27": (-6.1702, 106.9417),   # Jakarta - Updated coordinates
            "C28": (-6.2383, 106.9756),   # Bekasi - Updated coordinates
            "C29": (-6.5950, 106.8167),   # Bogor - Updated coordinates
            "C30": (-6.1783, 106.6319),   # Tangerang - Updated coordinates
            "C31": (-6.7324, 108.5523),   # Cirebon
            "C32": (-6.8694, 109.1402),   # Tegal
            "C33": (-6.8883, 109.6753),   # Pekalongan
            "C34": (-7.0051, 110.4381),   # Semarang
            "C35": (-6.8048, 110.8405),   # Kudus
            "C36": (-6.7489, 111.0382),   # Pati
            "C37": (-6.7083, 111.3417),   # Rembang
            "C38": (-6.8976, 112.0509),   # Tuban
            "C39": (-7.1167, 112.4167),   # Lamongan
            "C40": (-6.9083, 110.6000),   # Batang
        }
        return coordinates
    
    def get_vehicle_types(self) -> Dict[str, Dict]:
        """Mengklasifikasikan jenis kendaraan berdasarkan kapasitas"""
        vehicle_types = {
            "small_truck": {
                "capacity_kg": 1000,
                "description": "Truk Kecil",
                "routes": []
            },
            "medium_truck": {
                "capacity_kg": 2000,
                "description": "Truk Sedang", 
                "routes": []
            },
            "large_truck": {
                "capacity_kg": 3580,
                "description": "Truk Besar",
                "routes": []
            }
        }
        
        for route in self.routes_data:
            if route.capacity_kg == 1000:
                vehicle_types["small_truck"]["routes"].append(route)
            elif route.capacity_kg == 2000:
                vehicle_types["medium_truck"]["routes"].append(route)
            elif route.capacity_kg == 3580:
                vehicle_types["large_truck"]["routes"].append(route)
        
        return vehicle_types
    
    def get_route_statistics(self, jabodetabek_only: bool = False) -> Dict:
        """Statistik rute pengiriman"""
        # Filter rute Jabodetabek jika diminta
        jabodetabek_routes = ["C27", "C28", "C29", "C30"]  # Jakarta, Bekasi, Bogor, Tangerang
        
        if jabodetabek_only:
            filtered_routes = [r for r in self.routes_data if r.branch_code in jabodetabek_routes]
        else:
            filtered_routes = self.routes_data
            
        total_routes = len(filtered_routes)
        total_distance = sum(route.distance_km for route in filtered_routes)
        total_capacity = sum(route.capacity_kg for route in filtered_routes)
        total_load = sum(route.load_kg for route in filtered_routes)
        avg_utilization = np.mean([route.utilization_percent for route in filtered_routes]) if filtered_routes else 0
        
        # Rute dengan utilitas tinggi (>= 90%)
        high_utilization_routes = [r for r in filtered_routes if r.utilization_percent >= 90]
        
        # Rute dengan kapasitas tersisa
        available_routes = [r for r in filtered_routes if r.remaining_capacity > 0]
        
        return {
            "total_routes": total_routes,
            "total_distance_km": total_distance,
            "total_capacity_kg": total_capacity,
            "total_load_kg": total_load,
            "average_utilization_percent": round(avg_utilization, 2),
            "high_utilization_routes": len(high_utilization_routes),
            "available_capacity_routes": len(available_routes),
            "total_remaining_capacity": sum(r.remaining_capacity for r in filtered_routes),
            "jabodetabek_only": jabodetabek_only
        }
    
    def get_optimization_data(self, jabodetabek_only: bool = False) -> List[Dict]:
        """Data untuk optimasi VRP"""
        optimization_data = []
        
        # Filter rute Jabodetabek
        jabodetabek_routes = ["C27", "C28", "C29", "C30"]  # Jakarta, Bekasi, Bogor, Tangerang
        
        for route in self.routes_data:
            if route.branch_code in self.coordinates_mapping:
                # Filter hanya rute Jabodetabek jika diminta
                if jabodetabek_only and route.branch_code not in jabodetabek_routes:
                    continue
                    
                lat, lng = self.coordinates_mapping[route.branch_code]
                
                # Estimasi jenis barang berdasarkan pola
                cargo_type = self._estimate_cargo_type(route)
                
                optimization_data.append({
                    "route_id": route.branch_code,
                    "route_name": route.route_name,
                    "location": {
                        "lat": lat,
                        "lng": lng,
                        "name": route.route_name.split('-')[1] if '-' in route.route_name else route.route_name
                    },
                    "capacity": route.capacity_kg,
                    "current_load": route.load_kg,
                    "remaining_capacity": route.remaining_capacity,
                    "distance_km": route.distance_km,
                    "utilization_percent": route.utilization_percent,
                    "cargo_type": cargo_type,
                    "vehicle_type": self._get_vehicle_type_by_capacity(route.capacity_kg),
                    "priority": self._calculate_priority(route),
                    "is_jabodetabek": route.branch_code in jabodetabek_routes
                })
        
        return optimization_data
    
    def _estimate_cargo_type(self, route: RouteData) -> str:
        """Estimasi jenis barang berdasarkan pola rute dan kapasitas"""
        # PT. Sanghiang Perkasa (Kalbe Nutritionals) - produk makanan bernutrisi
        route_name = route.route_name.lower()
        
        # Fokus pada produk makanan bernutrisi
        if "jakarta" in route_name or "bekasi" in route_name or "bogor" in route_name or "tangerang" in route_name:
            return "Produk Nutrisi (Chil-kid, Entrasol, dll)"  # Jabodetabek - produk utama
        elif "jember" in route_name or "malang" in route_name:
            return "Produk Nutrisi Regional"  # Jawa Timur
        elif "surabaya" in route_name:
            return "Produk Nutrisi Regional"   # Surabaya
        elif "solo" in route_name:
            return "Produk Nutrisi Regional"  # Solo
        elif "cirebon" in route_name:
            return "Produk Nutrisi Regional"    # Cirebon
        else:
            return "Produk Nutrisi Umum"
    
    def _get_vehicle_type_by_capacity(self, capacity: float) -> str:
        """Menentukan jenis kendaraan berdasarkan kapasitas"""
        if capacity == 1000:
            return "Truk Kecil (1 Ton)"
        elif capacity == 2000:
            return "Truk Sedang (2 Ton)"
        elif capacity == 3580:
            return "Truk Besar (3.5 Ton)"
        else:
            return "Truk Tidak Diketahui"
    
    def _calculate_priority(self, route: RouteData) -> int:
        """Menghitung prioritas rute berdasarkan berbagai faktor"""
        priority = 0
        
        # Prioritas berdasarkan utilitas (semakin tinggi semakin prioritas)
        priority += route.utilization_percent * 0.5
        
        # Prioritas berdasarkan jarak (semakin jauh semakin prioritas untuk optimasi)
        priority += min(route.distance_km / 100, 5) * 10
        
        # Prioritas berdasarkan kapasitas tersisa (semakin sedikit semakin prioritas)
        if route.remaining_capacity == 0:
            priority += 20  # Rute penuh - prioritas tinggi untuk optimasi
        
        return int(priority)
    
    def export_to_csv(self, filename: str = "pt_sanghiang_routes.csv"):
        """Export data ke CSV untuk analisis lebih lanjut"""
        data = []
        for route in self.routes_data:
            if route.branch_code in self.coordinates_mapping:
                lat, lng = self.coordinates_mapping[route.branch_code]
                data.append({
                    "route_name": route.route_name,
                    "branch_code": route.branch_code,
                    "latitude": lat,
                    "longitude": lng,
                    "distance_km": route.distance_km,
                    "capacity_kg": route.capacity_kg,
                    "load_kg": route.load_kg,
                    "remaining_capacity": route.remaining_capacity,
                    "utilization_percent": route.utilization_percent,
                    "cargo_type": self._estimate_cargo_type(route),
                    "vehicle_type": self._get_vehicle_type_by_capacity(route.capacity_kg),
                    "priority": self._calculate_priority(route)
                })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Data exported to {filename}")
        return df

# Contoh penggunaan
if __name__ == "__main__":
    processor = PTSanghiangDataProcessor()
    
    print("📊 Statistik Rute PT. Sanghiang Perkasa:")
    stats = processor.get_route_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n🚛 Jenis Kendaraan:")
    vehicle_types = processor.get_vehicle_types()
    for vtype, info in vehicle_types.items():
        print(f"  {info['description']} ({info['capacity_kg']} kg): {len(info['routes'])} rute")
    
    print("\n📋 Data Optimasi (5 pertama):")
    opt_data = processor.get_optimization_data()
    for i, route in enumerate(opt_data[:5]):
        print(f"  {i+1}. {route['route_name']} - {route['cargo_type']} - {route['vehicle_type']}")
    
    # Export ke CSV
    processor.export_to_csv() 