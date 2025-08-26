#!/usr/bin/env python3
"""
Test script untuk memverifikasi filter Jabodetabek
"""

from pt_sanghiang_data import PTSanghiangDataProcessor

def test_jabodetabek_filter():
    """Test filter Jabodetabek"""
    processor = PTSanghiangDataProcessor()
    
    print("🏙️ TEST FILTER JABODETABEK - PT. Sanghiang Perkasa (Kalbe Nutritionals)")
    print("=" * 70)
    
    # Test semua rute
    print("\n📊 SEMUA RUTE (18 rute):")
    all_routes = processor.get_optimization_data(jabodetabek_only=False)
    print(f"Total rute: {len(all_routes)}")
    for route in all_routes:
        print(f"  - {route['route_name']} ({route['route_id']}) - {route['cargo_type']}")
    
    # Test hanya Jabodetabek
    print("\n🏙️ RUTE JABODETABEK SAJA (4 rute):")
    jabodetabek_routes = processor.get_optimization_data(jabodetabek_only=True)
    print(f"Total rute Jabodetabek: {len(jabodetabek_routes)}")
    
    for route in jabodetabek_routes:
        print(f"  - {route['route_name']} ({route['route_id']})")
        print(f"    Jarak: {route['distance_km']} km")
        print(f"    Kapasitas: {route['capacity']} kg")
        print(f"    Beban: {route['current_load']} kg")
        print(f"    Utilitas: {route['utilization_percent']}%")
        print(f"    Produk: {route['cargo_type']}")
        print(f"    Kendaraan: {route['vehicle_type']}")
        print(f"    Prioritas: {route['priority']}")
        print()
    
    # Test statistik
    print("📈 STATISTIK SEMUA RUTE:")
    all_stats = processor.get_route_statistics(jabodetabek_only=False)
    for key, value in all_stats.items():
        print(f"  {key}: {value}")
    
    print("\n📈 STATISTIK JABODETABEK SAJA:")
    jabodetabek_stats = processor.get_route_statistics(jabodetabek_only=True)
    for key, value in jabodetabek_stats.items():
        print(f"  {key}: {value}")
    
    # Test jenis kendaraan
    print("\n🚛 JENIS KENDARAAN JABODETABEK:")
    vehicle_types = processor.get_vehicle_types()
    for vtype, info in vehicle_types.items():
        jabodetabek_count = sum(1 for route in info['routes'] 
                               if route.branch_code in ['C27', 'C28', 'C29', 'C30'])
        if jabodetabek_count > 0:
            print(f"  {info['description']} ({info['capacity_kg']} kg): {jabodetabek_count} rute Jabodetabek")
    
    print("\n✅ TEST SELESAI!")
    print("\n🎯 KESIMPULAN:")
    print(f"  - Total rute: {len(all_routes)}")
    print(f"  - Rute Jabodetabek: {len(jabodetabek_routes)}")
    print(f"  - Fokus optimasi: Distribusi produk nutrisi Kalbe")
    print(f"  - Area utama: Jakarta, Bekasi, Bogor, Tangerang")

if __name__ == "__main__":
    test_jabodetabek_filter() 