#!/usr/bin/env python3
"""
🚛 VRP State Examples Generator
Menampilkan berbagai contoh state untuk sistem VRP DQN
"""

import random
from datetime import datetime, timedelta

class VRPStateGenerator:
    def __init__(self):
        # Weather conditions mapping
        self.weather_conditions = {
            'clear': 0,
            'clouds': 1, 
            'rain': 2,
            'storm': 3,
            'fog': 4
        }
        
        # Traffic conditions mapping
        self.traffic_conditions = {
            'low': 0,
            'medium': 1,
            'high': 2,
            'very_high': 3
        }
        
        # Time periods mapping
        self.time_periods = {
            'early_morning': 0,    # 00:00-06:00
            'morning_rush': 1,     # 06:00-09:00
            'mid_morning': 2,      # 09:00-12:00
            'lunch_time': 3,       # 12:00-14:00
            'afternoon': 4,        # 14:00-17:00
            'evening_rush': 5,     # 17:00-19:00
            'evening': 6,          # 19:00-22:00
            'late_night': 7        # 22:00-24:00
        }
    
    def generate_state(self, weather, traffic, time_period, customer_count, 
                      vehicle_capacity, current_load, distance_to_next, 
                      remaining_time, fuel_level, priority_level):
        """
        Generate state vector untuk VRP DQN
        
        State format: [weather, traffic, time_period, customer_count, 
                      vehicle_capacity, current_load, distance_to_next, 
                      remaining_time, fuel_level, priority_level]
        """
        return [
            self.weather_conditions[weather],
            self.traffic_conditions[traffic],
            self.time_periods[time_period],
            customer_count,
            vehicle_capacity,
            current_load,
            distance_to_next,
            remaining_time,
            fuel_level,
            priority_level
        ]
    
    def explain_state(self, state):
        """Menjelaskan makna setiap elemen dalam state"""
        weather_names = {v: k for k, v in self.weather_conditions.items()}
        traffic_names = {v: k for k, v in self.traffic_conditions.items()}
        time_names = {v: k for k, v in self.time_periods.items()}
        
        print(f"🌤️ Weather: {weather_names[state[0]]} ({state[0]})")
        print(f"🚦 Traffic: {traffic_names[state[1]]} ({state[1]})")
        print(f"⏰ Time Period: {time_names[state[2]]} ({state[2]})")
        print(f"👥 Customer Count: {state[3]}")
        print(f"🚛 Vehicle Capacity: {state[4]}")
        print(f"📦 Current Load: {state[5]}")
        print(f"📍 Distance to Next: {state[6]} km")
        print(f"⏱️ Remaining Time: {state[7]} minutes")
        print(f"⛽ Fuel Level: {state[8]}%")
        print(f"⭐ Priority Level: {state[9]}")
    
    def generate_scenario_examples(self):
        """Generate berbagai skenario state"""
        
        scenarios = []
        
        # Skenario 1: Pagi hari, hujan, macet
        print("=" * 60)
        print("🌧️ SKENARIO 1: PAGI HARI, HUJAN, MACET")
        print("=" * 60)
        state1 = self.generate_state(
            weather='rain',
            traffic='very_high', 
            time_period='morning_rush',
            customer_count=15,
            vehicle_capacity=100,
            current_load=75,
            distance_to_next=8,
            remaining_time=120,
            fuel_level=85,
            priority_level=3
        )
        print(f"State Vector: {state1}")
        self.explain_state(state1)
        scenarios.append(("Skenario 1: Pagi Hujan Macet", state1))
        
        # Skenario 2: Siang hari, cerah, lancar
        print("\n" + "=" * 60)
        print("🌞 SKENARIO 2: SIANG HARI, CERAH, LANCAR")
        print("=" * 60)
        state2 = self.generate_state(
            weather='clear',
            traffic='low',
            time_period='afternoon',
            customer_count=8,
            vehicle_capacity=100,
            current_load=45,
            distance_to_next=5,
            remaining_time=90,
            fuel_level=70,
            priority_level=1
        )
        print(f"State Vector: {state2}")
        self.explain_state(state2)
        scenarios.append(("Skenario 2: Siang Cerah Lancar", state2))
        
        # Skenario 3: Sore hari, berawan, sedang
        print("\n" + "=" * 60)
        print("☁️ SKENARIO 3: SORE HARI, BERAWAN, SEDANG")
        print("=" * 60)
        state3 = self.generate_state(
            weather='clouds',
            traffic='medium',
            time_period='evening_rush',
            customer_count=12,
            vehicle_capacity=100,
            current_load=60,
            distance_to_next=6,
            remaining_time=100,
            fuel_level=60,
            priority_level=2
        )
        print(f"State Vector: {state3}")
        self.explain_state(state3)
        scenarios.append(("Skenario 3: Sore Berawan Sedang", state3))
        
        # Skenario 4: Malam hari, kabut, rendah
        print("\n" + "=" * 60)
        print("🌫️ SKENARIO 4: MALAM HARI, KABUT, RENDAH")
        print("=" * 60)
        state4 = self.generate_state(
            weather='fog',
            traffic='low',
            time_period='late_night',
            customer_count=3,
            vehicle_capacity=100,
            current_load=20,
            distance_to_next=12,
            remaining_time=60,
            fuel_level=40,
            priority_level=1
        )
        print(f"State Vector: {state4}")
        self.explain_state(state4)
        scenarios.append(("Skenario 4: Malam Kabut Rendah", state4))
        
        # Skenario 5: Badai, sangat macet, prioritas tinggi
        print("\n" + "=" * 60)
        print("⛈️ SKENARIO 5: BADAI, SANGAT MACET, PRIORITAS TINGGI")
        print("=" * 60)
        state5 = self.generate_state(
            weather='storm',
            traffic='very_high',
            time_period='evening_rush',
            customer_count=20,
            vehicle_capacity=100,
            current_load=90,
            distance_to_next=15,
            remaining_time=150,
            fuel_level=30,
            priority_level=5
        )
        print(f"State Vector: {state5}")
        self.explain_state(state5)
        scenarios.append(("Skenario 5: Badai Macet Prioritas", state5))
        
        return scenarios
    
    def generate_random_states(self, count=10):
        """Generate state acak untuk testing"""
        
        print("\n" + "=" * 60)
        print(f"🎲 GENERATING {count} RANDOM STATES")
        print("=" * 60)
        
        random_states = []
        
        for i in range(count):
            weather = random.choice(list(self.weather_conditions.keys()))
            traffic = random.choice(list(self.traffic_conditions.keys()))
            time_period = random.choice(list(self.time_periods.keys()))
            
            state = self.generate_state(
                weather=weather,
                traffic=traffic,
                time_period=time_period,
                customer_count=random.randint(1, 25),
                vehicle_capacity=100,
                current_load=random.randint(10, 95),
                distance_to_next=random.randint(1, 20),
                remaining_time=random.randint(30, 180),
                fuel_level=random.randint(20, 100),
                priority_level=random.randint(1, 5)
            )
            
            print(f"\n🎯 Random State {i+1}: {state}")
            self.explain_state(state)
            random_states.append(state)
        
        return random_states
    
    def analyze_state_patterns(self, states):
        """Analisis pola dari kumpulan state"""
        
        print("\n" + "=" * 60)
        print("📊 ANALISIS POLA STATE")
        print("=" * 60)
        
        weather_counts = {}
        traffic_counts = {}
        time_counts = {}
        
        for state in states:
            # Count weather patterns
            weather = state[0]
            weather_counts[weather] = weather_counts.get(weather, 0) + 1
            
            # Count traffic patterns
            traffic = state[1]
            traffic_counts[traffic] = traffic_counts.get(traffic, 0) + 1
            
            # Count time patterns
            time_period = state[2]
            time_counts[time_period] = time_counts.get(time_period, 0) + 1
        
        print("\n🌤️ Weather Distribution:")
        for weather, count in weather_counts.items():
            weather_names = {v: k for k, v in self.weather_conditions.items()}
            print(f"  {weather_names[weather]}: {count} states")
        
        print("\n🚦 Traffic Distribution:")
        for traffic, count in traffic_counts.items():
            traffic_names = {v: k for k, v in self.traffic_conditions.items()}
            print(f"  {traffic_names[traffic]}: {count} states")
        
        print("\n⏰ Time Period Distribution:")
        for time_period, count in time_counts.items():
            time_names = {v: k for k, v in self.time_periods.items()}
            print(f"  {time_names[time_period]}: {count} states")

def main():
    """Main function"""
    
    print("🚛 VRP STATE EXAMPLES GENERATOR")
    print("=" * 60)
    print("Menampilkan berbagai contoh state untuk sistem VRP DQN")
    print("=" * 60)
    
    # Buat generator
    generator = VRPStateGenerator()
    
    # Generate skenario contoh
    scenarios = generator.generate_scenario_examples()
    
    # Generate state acak
    random_states = generator.generate_random_states(10)
    
    # Analisis pola
    all_states = [scenario[1] for scenario in scenarios] + random_states
    generator.analyze_state_patterns(all_states)
    
    # Tampilkan ringkasan
    print("\n" + "=" * 60)
    print("📋 RINGKASAN STATE FORMAT")
    print("=" * 60)
    print("State Vector Format: [weather, traffic, time_period, customer_count,")
    print("                     vehicle_capacity, current_load, distance_to_next,")
    print("                     remaining_time, fuel_level, priority_level]")
    print("\nState yang Anda berikan: [0, 6000, 8, 1.2, 1.5, 1, 1, 1, 1]")
    print("Format ini tampaknya berbeda dengan format standar VRP DQN.")
    print("Format standar memiliki 10 elemen, bukan 9 elemen.")

if __name__ == "__main__":
    main() 