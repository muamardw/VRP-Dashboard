#!/usr/bin/env python3
"""
Script untuk menjalankan aplikasi VRP dengan faktor dinamis real-time.
Mengintegrasikan cuaca, lalu lintas, dan variasi rute.
"""

import os
import time
import pandas as pd
from datetime import datetime
from utils import load_config
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent
from route_variations import RouteVariationSystem

class DynamicVRPApp:
    """Aplikasi VRP dengan faktor dinamis real-time."""
    
    def __init__(self):
        self.config = load_config()
        self.route_system = RouteVariationSystem()
        
        # Load data real
        if os.path.exists('data/real_shipments.csv'):
            self.customers_df = pd.read_csv('data/real_shipments.csv')
        else:
            print("❌ Data real tidak ditemukan! Jalankan create_real_dataset.py terlebih dahulu.")
            return
        
        # Initialize environment and agent
        self.env = VRPDynamicEnv(self.customers_df, n_vehicles=1)
        self.agent = DQNAgent(
            state_size=self.env.observation_space.shape[0],
            action_size=self.env.action_space.n,
            config=self.config
        )
        
        # Load trained model
        model_path = 'model/dqn_real_final.weights.h5'
        if os.path.exists(model_path):
            self.agent.load(model_path)
            print(f"✅ Model loaded: {model_path}")
        else:
            print(f"⚠️ Model {model_path} tidak ditemukan, menggunakan model random")
    
    def get_current_conditions(self):
        """Dapatkan kondisi cuaca dan lalu lintas saat ini."""
        
        print("🌤️ Mengambil data kondisi real-time...")
        
        # Simulasi data cuaca dan lalu lintas (dalam implementasi real akan menggunakan API)
        current_conditions = {
            'weather': {
                'condition': 'Cerah Berawan',
                'factor': 1.0,
                'description': 'Kondisi cuaca normal'
            },
            'traffic': {
                'condition': 'Sedang',
                'factor': 1.1,
                'description': 'Lalu lintas agak padat'
            },
            'time': datetime.now().strftime("%H:%M WIB"),
            'date': datetime.now().strftime("%d/%m/%Y")
        }
        
        return current_conditions
    
    def get_optimal_route_with_conditions(self, conditions):
        """Dapatkan rute optimal berdasarkan kondisi saat ini."""
        
        print("🗺️ Menghitung rute optimal berdasarkan kondisi dinamis...")
        
        # Hitung rute optimal dengan mempertimbangkan kondisi
        optimal_routes = {}
        
        for destination in self.route_system.destinations.keys():
            # Pilih rute berdasarkan kondisi lalu lintas
            if conditions['traffic']['factor'] > 1.2:  # Macet
                optimal_route, route_data = self.route_system.get_optimal_route(destination, 'time')
            elif conditions['traffic']['factor'] < 0.9:  # Lancar
                optimal_route, route_data = self.route_system.get_optimal_route(destination, 'distance')
            else:  # Sedang
                optimal_route, route_data = self.route_system.get_optimal_route(destination, 'efficiency')
            
            # Terapkan faktor cuaca dan lalu lintas
            adjusted_time = route_data['time'] * conditions['weather']['factor'] * conditions['traffic']['factor']
            
            optimal_routes[destination] = {
                'route': optimal_route,
                'route_name': route_data['name'],
                'base_distance': route_data['distance'],
                'base_time': route_data['time'],
                'adjusted_time': adjusted_time,
                'weather_factor': conditions['weather']['factor'],
                'traffic_factor': conditions['traffic']['factor']
            }
        
        return optimal_routes
    
    def run_dynamic_evaluation(self):
        """Jalankan evaluasi dengan faktor dinamis."""
        
        print("🚚 Menjalankan evaluasi VRP dengan faktor dinamis...")
        
        # Dapatkan kondisi saat ini
        conditions = self.get_current_conditions()
        
        # Dapatkan rute optimal
        optimal_routes = self.get_optimal_route_with_conditions(conditions)
        
        # Jalankan evaluasi dengan greedy policy
        self.agent.epsilon = 0.0  # Greedy
        
        state = self.env.reset()
        total_reward = 0
        route_taken = []
        
        while True:
            valid_actions = [i for i in range(self.env.n_customers) if i not in self.env.visited_customers]
            action = self.agent.act(state, valid_actions)
            
            next_state, reward, done, info = self.env.step(action)
            state = next_state
            total_reward += reward
            
            # Record route
            if action > 0:
                customer = self.env.customers_df.iloc[action]
                destination_name = list(self.route_system.destinations.keys())[action - 1]
                route_taken.append({
                    'destination': destination_name,
                    'route': optimal_routes[destination_name]['route_name'],
                    'distance': optimal_routes[destination_name]['base_distance'],
                    'time': optimal_routes[destination_name]['adjusted_time']
                })
            
            if done:
                break
        
        return {
            'conditions': conditions,
            'optimal_routes': optimal_routes,
            'route_taken': route_taken,
            'total_reward': total_reward,
            'total_distance': info.get('total_distance', 0),
            'total_time': info.get('total_time', 0),
            'visited_customers': info.get('visited_customers', 0)
        }
    
    def display_results(self, results):
        """Tampilkan hasil dengan format yang menarik."""
        
        print("\n" + "="*70)
        print("🚚 HASIL VRP DQN - FAKTOR DINAMIS")
        print("="*70)
        
        # Kondisi saat ini
        conditions = results['conditions']
        print(f"\n📍 KONDISI SAAT INI:")
        print(f"   Waktu: {conditions['time']} | Tanggal: {conditions['date']}")
        print(f"   Cuaca: {conditions['weather']['condition']} (Faktor: {conditions['weather']['factor']})")
        print(f"   Lalu Lintas: {conditions['traffic']['condition']} (Faktor: {conditions['traffic']['factor']})")
        
        # Rute optimal
        print(f"\n🎯 REKOMENDASI RUTE OPTIMAL:")
        print("-" * 50)
        
        total_distance = 0
        total_time = 0
        
        for destination, route_info in results['optimal_routes'].items():
            print(f"   {destination} ({self.route_system.destinations[destination]['code']}):")
            print(f"      Rute: {route_info['route_name']}")
            print(f"      Jarak: {route_info['base_distance']:.2f} km")
            print(f"      Waktu Dasar: {route_info['base_time']:.2f} jam")
            print(f"      Waktu Aktual: {route_info['adjusted_time']:.2f} jam")
            print(f"      Faktor Cuaca: {route_info['weather_factor']}")
            print(f"      Faktor Lalu Lintas: {route_info['traffic_factor']}")
            print()
            
            total_distance += route_info['base_distance']
            total_time += route_info['adjusted_time']
        
        # Hasil evaluasi
        print(f"📊 HASIL EVALUASI DQN:")
        print("-" * 30)
        print(f"   Total Reward: {results['total_reward']:.2f}")
        print(f"   Total Distance: {results['total_distance']:.2f} km")
        print(f"   Total Time: {results['total_time']:.2f} jam")
        print(f"   Visited Customers: {results['visited_customers']}/4")
        
        # Rute yang diambil
        print(f"\n🛣️ RUTE YANG DIIKUTI:")
        print("-" * 30)
        for i, route in enumerate(results['route_taken'], 1):
            print(f"   {i}. {route['destination']}: {route['route']}")
            print(f"      Jarak: {route['distance']:.2f} km | Waktu: {route['time']:.2f} jam")
        
        # Efisiensi
        efficiency = (results['visited_customers'] / 4) * 100
        print(f"\n📈 EFISIENSI:")
        print(f"   Completion Rate: {efficiency:.1f}%")
        print(f"   Average Time per Destination: {total_time/4:.2f} jam")
        print(f"   Distance per Destination: {total_distance/4:.2f} km")
        
        # Simpan hasil
        self.save_results(results)
    
    def save_results(self, results):
        """Simpan hasil ke file."""
        
        # Buat DataFrame untuk hasil
        route_data = []
        for route in results['route_taken']:
            route_data.append({
                'timestamp': datetime.now().isoformat(),
                'destination': route['destination'],
                'route': route['route'],
                'distance_km': route['distance'],
                'time_hours': route['time'],
                'weather_factor': results['conditions']['weather']['factor'],
                'traffic_factor': results['conditions']['traffic']['factor']
            })
        
        df = pd.DataFrame(route_data)
        
        # Simpan ke file
        os.makedirs('data', exist_ok=True)
        filename = f"data/dynamic_vrp_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        print(f"\n💾 Hasil disimpan: {filename}")
    
    def run_interactive_mode(self):
        """Mode interaktif untuk menjalankan aplikasi."""
        
        print("🚚 APLIKASI VRP DQN - FAKTOR DINAMIS")
        print("=" * 50)
        print("Aplikasi ini akan:")
        print("1. Mengambil data cuaca dan lalu lintas real-time")
        print("2. Menghitung rute optimal berdasarkan kondisi")
        print("3. Menjalankan evaluasi DQN")
        print("4. Menampilkan rekomendasi rute")
        print("=" * 50)
        
        while True:
            try:
                choice = input("\nPilih opsi:\n1. Jalankan evaluasi dinamis\n2. Lihat kondisi saat ini\n3. Keluar\nPilihan: ").strip()
                
                if choice == '1':
                    print("\n🔄 Menjalankan evaluasi dinamis...")
                    results = self.run_dynamic_evaluation()
                    self.display_results(results)
                    
                elif choice == '2':
                    conditions = self.get_current_conditions()
                    print(f"\n📍 Kondisi Saat Ini:")
                    print(f"   Waktu: {conditions['time']}")
                    print(f"   Cuaca: {conditions['weather']['condition']}")
                    print(f"   Lalu Lintas: {conditions['traffic']['condition']}")
                    
                elif choice == '3':
                    print("👋 Terima kasih!")
                    break
                    
                else:
                    print("❌ Pilihan tidak valid!")
                    
            except KeyboardInterrupt:
                print("\n👋 Terima kasih!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function."""
    
    app = DynamicVRPApp()
    
    if hasattr(app, 'env'):  # Check if initialization was successful
        app.run_interactive_mode()
    else:
        print("❌ Gagal menginisialisasi aplikasi!")

if __name__ == '__main__':
    main() 