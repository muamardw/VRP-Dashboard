#!/usr/bin/env python3
"""
Script untuk menampilkan semua kombinasi rute yang mungkin untuk 4 destinasi PT. Sanghiang Perkasa.
"""

import itertools
import pandas as pd
from utils import calculate_distance

def generate_all_routes():
    """Generate all possible route combinations for 4 destinations."""
    
    # Data lokasi
    locations = {
        0: {
            'name': 'Depot (Pulo Gadung, Jakarta Timur)',
            'code': 'DEPOT',
            'lat': -6.1702,
            'lon': 106.9417
        },
        1: {
            'name': 'Bogor (Jl. Wangun no. 216 Sindangsari Bogor Timur)',
            'code': 'C25',
            'lat': -6.5950,
            'lon': 106.8167
        },
        2: {
            'name': 'Tangerang (Jl. Serenade Lake No.15, Kelapa Dua)',
            'code': 'C26',
            'lat': -6.1783,
            'lon': 106.6319
        },
        3: {
            'name': 'Jakarta (Jl. Pulo Lentut no. 10, Pulo Gadung)',
            'code': 'C27',
            'lat': -6.1702,
            'lon': 106.9417
        },
        4: {
            'name': 'Bekasi (Jl. Jakasetia no. 27 B, Bekasi Selatan)',
            'code': 'C28',
            'lat': -6.2383,
            'lon': 106.9756
        }
    }
    
    # Generate all permutations of destinations (1,2,3,4)
    destinations = [1, 2, 3, 4]
    all_permutations = list(itertools.permutations(destinations))
    
    print(f"🚚 SEMUA KOMBINASI RUTE PT. SANGHIANG PERKASA")
    print(f"📊 Total kombinasi: {len(all_permutations)} rute")
    print(f"🎯 Destinasi: 4 (Bogor, Tangerang, Jakarta, Bekasi)")
    print(f"🏢 Depot: Pulo Gadung, Jakarta Timur")
    print("=" * 80)
    
    routes_data = []
    
    for i, route in enumerate(all_permutations, 1):
        # Add depot at start and end
        full_route = [0] + list(route) + [0]
        
        # Calculate total distance
        total_distance = 0
        route_names = []
        route_codes = []
        
        for j in range(len(full_route) - 1):
            current = full_route[j]
            next_stop = full_route[j + 1]
            
            # Calculate distance between current and next
            dist = calculate_distance(
                locations[current]['lat'], locations[current]['lon'],
                locations[next_stop]['lat'], locations[next_stop]['lon']
            )
            total_distance += dist
            
            # Add route info
            if j == 0:  # Start from depot
                route_names.append(f"G → {locations[next_stop]['name']}")
                route_codes.append(f"G-{locations[next_stop]['code']}-G")
            elif j == len(full_route) - 2:  # End at depot
                route_names.append(f"{locations[current]['name']} → G")
                route_codes.append(f"G-{locations[current]['code']}-G")
            else:
                route_names.append(f"{locations[current]['name']} → {locations[next_stop]['name']}")
                route_codes.append(f"{locations[current]['code']}-{locations[next_stop]['code']}")
        
        # Create route description
        route_description = " → ".join([locations[stop]['code'] if stop != 0 else 'G' for stop in full_route])
        
        routes_data.append({
            'No': i,
            'Route': route_description,
            'Total Distance (km)': round(total_distance, 2),
            'Route Names': ' | '.join(route_names),
            'Route Codes': ' | '.join(route_codes)
        })
        
        # Print first 10 and last 10 routes
        if i <= 10 or i > len(all_permutations) - 10:
            print(f"{i:2d}. {route_description}")
            print(f"    Jarak: {total_distance:.2f} km")
            print(f"    Rute: {' → '.join(route_names)}")
            print()
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(routes_data)
    df.to_csv('data/all_possible_routes.csv', index=False)
    
    print(f"💾 Semua {len(all_permutations)} rute disimpan di: data/all_possible_routes.csv")
    
    # Find optimal route (shortest distance)
    optimal_route = df.loc[df['Total Distance (km)'].idxmin()]
    print(f"\n🏆 RUTE OPTIMAL (Jarak Terpendek):")
    print(f"   No: {optimal_route['No']}")
    print(f"   Route: {optimal_route['Route']}")
    print(f"   Distance: {optimal_route['Total Distance (km)']} km")
    print(f"   Names: {optimal_route['Route Names']}")
    
    # Find worst route (longest distance)
    worst_route = df.loc[df['Total Distance (km)'].idxmax()]
    print(f"\n⚠️ RUTE TERBURUK (Jarak Terpanjang):")
    print(f"   No: {worst_route['No']}")
    print(f"   Route: {worst_route['Route']}")
    print(f"   Distance: {worst_route['Total Distance (km)']} km")
    print(f"   Names: {worst_route['Route Names']}")
    
    # Statistics
    print(f"\n📊 STATISTIK RUTE:")
    print(f"   Rata-rata jarak: {df['Total Distance (km)'].mean():.2f} km")
    print(f"   Jarak minimum: {df['Total Distance (km)'].min():.2f} km")
    print(f"   Jarak maksimum: {df['Total Distance (km)'].max():.2f} km")
    print(f"   Standar deviasi: {df['Total Distance (km)'].std():.2f} km")
    
    return df

def show_route_details(route_number):
    """Show detailed information for a specific route."""
    
    df = pd.read_csv('data/all_possible_routes.csv')
    
    if route_number < 1 or route_number > len(df):
        print(f"❌ Route number {route_number} tidak valid!")
        return
    
    route = df.iloc[route_number - 1]
    
    print(f"\n📋 DETAIL RUTE #{route_number}")
    print("=" * 50)
    print(f"Route: {route['Route']}")
    print(f"Total Distance: {route['Total Distance (km)']} km")
    print(f"Route Names: {route['Route Names']}")
    print(f"Route Codes: {route['Route Codes']}")

def main():
    """Main function."""
    
    print("🗺️ MENAMPILKAN SEMUA KOMBINASI RUTE")
    print("=" * 50)
    
    # Generate all routes
    df = generate_all_routes()
    
    # Ask user if they want to see specific route details
    while True:
        try:
            choice = input(f"\nMasukkan nomor rute (1-{len(df)}) untuk detail, atau 'q' untuk keluar: ").strip()
            
            if choice.lower() == 'q':
                break
            
            route_num = int(choice)
            show_route_details(route_num)
            
        except ValueError:
            print("❌ Input tidak valid!")
        except KeyboardInterrupt:
            break
    
    print("\n🎉 Selesai!")

if __name__ == '__main__':
    main() 