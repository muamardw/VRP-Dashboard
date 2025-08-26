#!/usr/bin/env python3
"""
Sistem untuk menangani variasi rute ke setiap destinasi PT. Sanghiang Perkasa.
Destinasi tetap 4, tapi rute/jalur ke setiap destinasi bisa berubah-ubah.
"""

import pandas as pd
import numpy as np
from utils import calculate_distance

class RouteVariationSystem:
    """Sistem untuk mengelola variasi rute ke setiap destinasi."""
    
    def __init__(self):
        # Destinasi tetap (4 lokasi)
        self.destinations = {
            'Bogor': {
                'code': 'C25',
                'lat': -6.5950,
                'lon': 106.8167,
                'address': 'Jl. Wangun no. 216 Sindangsari Bogor Timur'
            },
            'Tangerang': {
                'code': 'C26', 
                'lat': -6.1783,
                'lon': 106.6319,
                'address': 'Jl. Serenade Lake No.15, Kelapa Dua'
            },
            'Jakarta': {
                'code': 'C27',
                'lat': -6.1702,
                'lon': 106.9417,
                'address': 'Jl. Pulo Lentut no. 10, Pulo Gadung'
            },
            'Bekasi': {
                'code': 'C28',
                'lat': -6.2383,
                'lon': 106.9756,
                'address': 'Jl. Jakasetia no. 27 B, Bekasi Selatan'
            }
        }
        
        # Depot
        self.depot = {
            'name': 'Depot Pulo Gadung',
            'lat': -6.1702,
            'lon': 106.9417,
            'address': 'Pulo Gadung, Jakarta Timur'
        }
        
        # Variasi rute untuk setiap destinasi
        self.route_variations = {
            'Bogor': {
                'route_1': {
                    'name': 'Tol Jagorawi',
                    'distance_factor': 1.0,  # Jarak normal
                    'time_factor': 1.0,      # Waktu normal
                    'traffic_factor': 0.8,   # Lalu lintas ringan
                    'description': 'Depot → Tol Jagorawi → Bogor'
                },
                'route_2': {
                    'name': 'Tol Cipularang',
                    'distance_factor': 1.2,  # 20% lebih jauh
                    'time_factor': 0.9,      # 10% lebih cepat
                    'traffic_factor': 0.7,   # Lalu lintas sangat ringan
                    'description': 'Depot → Tol Cipularang → Bogor'
                },
                'route_3': {
                    'name': 'Jalan Alternatif',
                    'distance_factor': 0.9,  # 10% lebih dekat
                    'time_factor': 1.3,      # 30% lebih lama
                    'traffic_factor': 1.2,   # Lalu lintas padat
                    'description': 'Depot → Jalan Alternatif → Bogor'
                }
            },
            'Tangerang': {
                'route_1': {
                    'name': 'Tol Jakarta-Tangerang',
                    'distance_factor': 1.0,
                    'time_factor': 1.0,
                    'traffic_factor': 1.1,
                    'description': 'Depot → Tol Jakarta-Tangerang → Tangerang'
                },
                'route_2': {
                    'name': 'Tol Serpong',
                    'distance_factor': 1.1,
                    'time_factor': 0.8,
                    'traffic_factor': 0.9,
                    'description': 'Depot → Tol Serpong → Tangerang'
                },
                'route_3': {
                    'name': 'Jalan Lokal',
                    'distance_factor': 0.8,
                    'time_factor': 1.4,
                    'traffic_factor': 1.3,
                    'description': 'Depot → Jalan Lokal → Tangerang'
                }
            },
            'Jakarta': {
                'route_1': {
                    'name': 'Tol Dalam Kota',
                    'distance_factor': 1.0,
                    'time_factor': 1.0,
                    'traffic_factor': 1.2,
                    'description': 'Depot → Tol Dalam Kota → Jakarta'
                },
                'route_2': {
                    'name': 'Jalan Arteri',
                    'distance_factor': 0.9,
                    'time_factor': 1.1,
                    'traffic_factor': 1.0,
                    'description': 'Depot → Jalan Arteri → Jakarta'
                },
                'route_3': {
                    'name': 'Tol Lingkar',
                    'distance_factor': 1.3,
                    'time_factor': 0.9,
                    'traffic_factor': 0.8,
                    'description': 'Depot → Tol Lingkar → Jakarta'
                }
            },
            'Bekasi': {
                'route_1': {
                    'name': 'Tol Jakarta-Cikampek',
                    'distance_factor': 1.0,
                    'time_factor': 1.0,
                    'traffic_factor': 1.1,
                    'description': 'Depot → Tol Jakarta-Cikampek → Bekasi'
                },
                'route_2': {
                    'name': 'Tol Bekasi',
                    'distance_factor': 1.1,
                    'time_factor': 0.9,
                    'traffic_factor': 0.9,
                    'description': 'Depot → Tol Bekasi → Bekasi'
                },
                'route_3': {
                    'name': 'Jalan Provinsi',
                    'distance_factor': 0.8,
                    'time_factor': 1.3,
                    'traffic_factor': 1.2,
                    'description': 'Depot → Jalan Provinsi → Bekasi'
                }
            }
        }
    
    def calculate_route_distance(self, from_location, to_destination, route_variation):
        """Hitung jarak dengan variasi rute."""
        
        # Jarak dasar (Haversine)
        base_distance = calculate_distance(
            from_location['lat'], from_location['lon'],
            self.destinations[to_destination]['lat'], 
            self.destinations[to_destination]['lon']
        )
        
        # Terapkan faktor variasi rute
        adjusted_distance = base_distance * self.route_variations[to_destination][route_variation]['distance_factor']
        
        return adjusted_distance
    
    def calculate_route_time(self, distance, route_variation, destination):
        """Hitung waktu tempuh dengan variasi rute."""
        
        base_speed = 50  # km/h (kecepatan dasar)
        
        # Terapkan faktor waktu dan lalu lintas
        time_factor = self.route_variations[destination][route_variation]['time_factor']
        traffic_factor = self.route_variations[destination][route_variation]['traffic_factor']
        
        effective_speed = base_speed / (time_factor * traffic_factor)
        travel_time = distance / effective_speed
        
        return travel_time
    
    def get_optimal_route(self, destination, criteria='distance'):
        """Dapatkan rute optimal untuk destinasi tertentu."""
        
        routes = self.route_variations[destination]
        base_distance = calculate_distance(
            self.depot['lat'], self.depot['lon'],
            self.destinations[destination]['lat'], 
            self.destinations[destination]['lon']
        )
        
        route_scores = {}
        
        for route_name, route_data in routes.items():
            distance = base_distance * route_data['distance_factor']
            time = self.calculate_route_time(distance, route_name, destination)
            
            if criteria == 'distance':
                score = distance
            elif criteria == 'time':
                score = time
            elif criteria == 'efficiency':
                score = distance * time  # Kombinasi jarak dan waktu
            else:
                score = distance
            
            route_scores[route_name] = {
                'name': route_data['name'],
                'distance': distance,
                'time': time,
                'score': score,
                'description': route_data['description']
            }
        
        # Pilih rute dengan score terbaik
        optimal_route = min(route_scores.items(), key=lambda x: x[1]['score'])
        
        return optimal_route[0], optimal_route[1]
    
    def generate_route_scenarios(self):
        """Generate berbagai skenario rute."""
        
        scenarios = []
        
        # Skenario 1: Semua rute optimal (jarak terpendek)
        scenario_1 = {}
        for destination in self.destinations.keys():
            optimal_route, route_data = self.get_optimal_route(destination, 'distance')
            scenario_1[destination] = {
                'route': optimal_route,
                'route_name': route_data['name'],
                'distance': route_data['distance'],
                'time': route_data['time']
            }
        
        # Skenario 2: Semua rute tercepat
        scenario_2 = {}
        for destination in self.destinations.keys():
            optimal_route, route_data = self.get_optimal_route(destination, 'time')
            scenario_2[destination] = {
                'route': optimal_route,
                'route_name': route_data['name'],
                'distance': route_data['distance'],
                'time': route_data['time']
            }
        
        # Skenario 3: Kombinasi optimal
        scenario_3 = {}
        for destination in self.destinations.keys():
            optimal_route, route_data = self.get_optimal_route(destination, 'efficiency')
            scenario_3[destination] = {
                'route': optimal_route,
                'route_name': route_data['name'],
                'distance': route_data['distance'],
                'time': route_data['time']
            }
        
        scenarios = [
            {'name': 'Jarak Terpendek', 'routes': scenario_1},
            {'name': 'Waktu Tercepat', 'routes': scenario_2},
            {'name': 'Efisiensi Optimal', 'routes': scenario_3}
        ]
        
        return scenarios
    
    def print_route_variations(self):
        """Print semua variasi rute."""
        
        print("🗺️ VARIASI RUTE PT. SANGHIANG PERKASA")
        print("=" * 60)
        print("Destinasi tetap 4, tapi rute ke setiap destinasi bisa berubah")
        print()
        
        for destination, routes in self.route_variations.items():
            print(f"📍 {destination} ({self.destinations[destination]['code']})")
            print(f"   Alamat: {self.destinations[destination]['address']}")
            print(f"   Koordinat: ({self.destinations[destination]['lat']}, {self.destinations[destination]['lon']})")
            print()
            
            for route_name, route_data in routes.items():
                print(f"   🛣️  {route_data['name']} ({route_name})")
                print(f"      Deskripsi: {route_data['description']}")
                print(f"      Faktor Jarak: {route_data['distance_factor']}x")
                print(f"      Faktor Waktu: {route_data['time_factor']}x")
                print(f"      Faktor Lalu Lintas: {route_data['traffic_factor']}x")
                print()
    
    def print_optimal_routes(self):
        """Print rute optimal untuk setiap destinasi."""
        
        print("🏆 RUTE OPTIMAL UNTUK SETIAP DESTINASI")
        print("=" * 50)
        
        scenarios = self.generate_route_scenarios()
        
        for scenario in scenarios:
            print(f"\n📊 {scenario['name']}:")
            print("-" * 30)
            
            total_distance = 0
            total_time = 0
            
            for destination, route_info in scenario['routes'].items():
                print(f"   {destination}: {route_info['route_name']}")
                print(f"      Jarak: {route_info['distance']:.2f} km")
                print(f"      Waktu: {route_info['time']:.2f} jam")
                
                total_distance += route_info['distance']
                total_time += route_info['time']
            
            print(f"\n   Total Jarak: {total_distance:.2f} km")
            print(f"   Total Waktu: {total_time:.2f} jam")

def main():
    """Main function."""
    
    route_system = RouteVariationSystem()
    
    print("🚚 SISTEM VARIASI RUTE PT. SANGHIANG PERKASA")
    print("=" * 60)
    print("Destinasi: 4 (Bogor, Tangerang, Jakarta, Bekasi)")
    print("Variasi Rute: 3 rute per destinasi")
    print("=" * 60)
    
    # Print semua variasi rute
    route_system.print_route_variations()
    
    # Print rute optimal
    route_system.print_optimal_routes()
    
    # Save to CSV
    scenarios = route_system.generate_route_scenarios()
    
    # Create DataFrame for scenarios
    scenario_data = []
    for scenario in scenarios:
        for destination, route_info in scenario['routes'].items():
            scenario_data.append({
                'Scenario': scenario['name'],
                'Destination': destination,
                'Route': route_info['route'],
                'Route_Name': route_info['route_name'],
                'Distance_km': round(route_info['distance'], 2),
                'Time_hours': round(route_info['time'], 2)
            })
    
    df = pd.DataFrame(scenario_data)
    df.to_csv('data/route_variations.csv', index=False)
    
    print(f"\n💾 Data variasi rute disimpan: data/route_variations.csv")
    print(f"📊 Total skenario: {len(scenarios)}")
    print(f"🎯 Total kombinasi rute: {len(scenario_data)}")

if __name__ == '__main__':
    main() 