#!/usr/bin/env python3
"""
Simple Training Script untuk S1 Skripsi - PT. Sanghiang Perkasa
IMPLEMENTASI SISTEM VEHICLE ROUTING PROBLEM (VRP) MENGGUNAKAN REINFORCEMENT LEARNING
Fokus pada 4 titik tujuan Jabodetabek: Bogor, Tangerang, Jakarta, Bekasi
"""

import numpy as np
import torch
from dqn_model import DQNAgent, VRPEnvironment
from pt_sanghiang_data import PTSanghiangDataProcessor
from backend_api import get_weather_data
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def simple_training_s1():
    """Training sederhana untuk S1 skripsi"""
    
    print("🎓 TRAINING DQN UNTUK S1 SKRIPSI - PT. Sanghiang Perkasa")
    print("=" * 60)
    print(f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Load Data PT. Sanghiang Perkasa (4 titik tujuan Jabodetabek)
    print("📊 1. Loading Data PT. Sanghiang Perkasa...")
    processor = PTSanghiangDataProcessor()
    optimization_data = processor.get_optimization_data(jabodetabek_only=True)  # Changed to True for Jabodetabek focus
    
    # Filter untuk 4 titik tujuan Jabodetabek
    jabodetabek_routes = []
    target_cities = ['Bogor', 'Tangerang', 'Jakarta', 'Bekasi']
    
    for route in optimization_data:
        if any(city in route['route_name'] for city in target_cities):
            jabodetabek_routes.append(route)
    
    # Jika data tidak cukup, buat data dummy untuk 4 kota
    if len(jabodetabek_routes) < 4:
        print("   ⚠️ Data tidak lengkap, menggunakan data default untuk 4 kota Jabodetabek")
        jabodetabek_routes = [
            {
                'route_name': 'Bogor Route',
                'distance_km': 60.0,
                'utilization_percent': 100.0,
                'capacity': 2000,
                'current_load': 2000,
                'route_id': 'BGR001',
                'location': {'lat': -6.595, 'lng': 106.8167}
            },
            {
                'route_name': 'Tangerang Route',
                'distance_km': 55.0,
                'utilization_percent': 70.0,
                'capacity': 1000,
                'current_load': 700,
                'route_id': 'TGR001',
                'location': {'lat': -6.1783, 'lng': 106.6319}
            },
            {
                'route_name': 'Jakarta Route',
                'distance_km': 17.0,
                'utilization_percent': 85.0,
                'capacity': 2000,
                'current_load': 1700,
                'route_id': 'JKT001',
                'location': {'lat': -6.1702, 'lng': 106.6417}
            },
            {
                'route_name': 'Bekasi Route',
                'distance_km': 10.0,
                'utilization_percent': 50.0,
                'capacity': 1000,
                'current_load': 500,
                'route_id': 'BKS001',
                'location': {'lat': -6.2383, 'lng': 106.9756}
            }
        ]
    
    print(f"   ✅ Data loaded: {len(jabodetabek_routes)} rute Jabodetabek")
    for i, route in enumerate(jabodetabek_routes):
        print(f"      {i+1}. {route['route_name']} - {route['distance_km']} km - {route['utilization_percent']}%")
    print()
    
    # 2. Prepare Training Data
    print("🚛 2. Preparing Training Data...")
    
    # Depot (Cikampek)
    depot = {"position": {"lat": -6.4194, "lng": 107.4515}}
    
    # Create vehicles and destinations
    vehicles = []
    destinations = []
    
    for i, route in enumerate(jabodetabek_routes):
        vehicle = {
            "position": {"lat": depot["position"]["lat"], "lng": depot["position"]["lng"]},
            "capacity": route["capacity"],
            "vehicle_id": i
        }
        vehicles.append(vehicle)
        
        destination = {
            "lat": route["location"]["lat"],
            "lng": route["location"]["lng"],
            "visited": False,
            "demand": route["current_load"],
            "route_id": route["route_id"],
            "route_name": route["route_name"]
        }
        destinations.append(destination)
    
    print(f"   ✅ Vehicles: {len(vehicles)}")
    print(f"   ✅ Destinations: {len(destinations)}")
    print("   📍 4 Titik Tujuan: Bogor, Tangerang, Jakarta, Bekasi")
    print()
    
    # 3. Get Real-time Weather Data
    print("🌤️ 3. Getting Real-time Weather Data...")
    try:
        weather_data = get_weather_data(depot["position"]["lat"], depot["position"]["lng"])
        print(f"   ✅ Weather: {weather_data['description']}, {weather_data['temperature']}°C")
    except:
        weather_data = {
            'temperature': 28.0,
            'humidity': 75.0,
            'wind_speed': 10.0,
            'rain': 0.0,
            'description': 'clear sky'
        }
        print(f"   ⚠️ Using default weather data")
    print()
    
    # 4. Create Environment
    print("🎮 4. Creating VRP Environment...")
    traffic_data = {"factor": 1.2}
    env = VRPEnvironment(vehicles, destinations, weather_data, traffic_data)
    
    # Initialize DQN agent
    state_size = len(env.current_state)
    action_size = len(vehicles) * len(destinations)
    
    print(f"   ✅ State size: {state_size}")
    print(f"   ✅ Action size: {action_size}")
    print()
    
    agent = DQNAgent(state_size, action_size, num_destinations=len(destinations))
    
    # 5. Training Parameters (Sesuai S1 Skripsi)
    print("⚙️ 5. Training Parameters...")
    episodes = 500  # Reduced for S1
    max_steps = 20
    batch_size = 16
    
    print(f"   📈 Episodes: {episodes}")
    print(f"   🎯 Max steps per episode: {max_steps}")
    print(f"   📦 Batch size: {batch_size}")
    print()
    
    # 6. Training
    print("🎮 6. Starting Training...")
    print("-" * 50)
    
    # Training history
    training_results = {
        'episode': [],
        'total_reward': [],
        'total_distance': [],
        'utilization': [],
        'epsilon': []
    }
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        total_distance = 0
        steps = 0
        
        while steps < max_steps:
            # Get valid actions
            valid_actions = []
            for i in range(len(vehicles)):
                for j in range(len(destinations)):
                    if not destinations[j].get('visited', False):
                        valid_actions.append((i, j))
            
            if not valid_actions:
                break
            
            # Choose action
            action = agent.act(state, valid_actions)
            
            # Take action
            next_state, reward, done = env.step(action)
            
            # Store experience
            agent.remember(state, action, reward, next_state, done)
            
            # Train agent
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            
            state = next_state
            total_reward += reward
            total_distance += abs(reward)
            steps += 1
            
            if done:
                break
        
        # Calculate utilization
        visited_count = sum(1 for dest in destinations if dest.get('visited', False))
        utilization = (visited_count / len(destinations)) * 100
        
        # Store results
        training_results['episode'].append(episode)
        training_results['total_reward'].append(total_reward)
        training_results['total_distance'].append(total_distance)
        training_results['utilization'].append(utilization)
        training_results['epsilon'].append(agent.epsilon)
        
        # Print progress
        if episode % 50 == 0 or episode == episodes - 1:
            avg_reward = np.mean(training_results['total_reward'][-50:])
            avg_utilization = np.mean(training_results['utilization'][-50:])
            print(f"Episode {episode:3d} | Reward: {total_reward:8.2f} | "
                  f"Distance: {total_distance:6.2f} | Utilization: {utilization:5.1f}% | "
                  f"Epsilon: {agent.epsilon:.3f}")
    
    print("\n✅ Training Completed!")
    print()
    
    # 7. Save Results
    print("💾 7. Saving Results...")
    
    # Save model
    model_path = "dqn_s1_skripsi_model.pth"
    agent.save(model_path)
    print(f"   ✅ Model saved: {model_path}")
    
    # Save training data
    df = pd.DataFrame(training_results)
    csv_path = "training_results_s1.csv"
    df.to_csv(csv_path, index=False)
    print(f"   ✅ Training data saved: {csv_path}")
    
    # 8. Plot Results
    print("📊 8. Creating Plots...")
    create_s1_plots(training_results)
    print("   ✅ Plots saved: training_plots_s1.png")
    print()
    
    # 9. Test Model
    print("🧪 9. Testing Trained Model...")
    test_results = test_s1_model(agent, env, destinations)
    print()
    
    # 10. Summary
    print("📋 10. Training Summary...")
    print_summary(training_results, test_results)
    
    return agent, env, training_results, test_results

def create_s1_plots(results):
    """Create plots for S1 skripsi"""
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('DQN Training Results - PT. Sanghiang Perkasa (S1 Skripsi)\n4 Titik Tujuan: Bogor, Tangerang, Jakarta, Bekasi', 
                fontsize=16, fontweight='bold')
    
    # Plot 1: Total Reward
    axes[0, 0].plot(results['episode'], results['total_reward'], 'b-', linewidth=1)
    axes[0, 0].set_title('Total Reward per Episode', fontweight='bold')
    axes[0, 0].set_xlabel('Episode')
    axes[0, 0].set_ylabel('Total Reward')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Total Distance
    axes[0, 1].plot(results['episode'], results['total_distance'], 'r-', linewidth=1)
    axes[0, 1].set_title('Total Distance per Episode', fontweight='bold')
    axes[0, 1].set_xlabel('Episode')
    axes[0, 1].set_ylabel('Total Distance')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Utilization
    axes[1, 0].plot(results['episode'], results['utilization'], 'g-', linewidth=1)
    axes[1, 0].set_title('Route Utilization per Episode', fontweight='bold')
    axes[1, 0].set_xlabel('Episode')
    axes[1, 0].set_ylabel('Utilization (%)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Epsilon
    axes[1, 1].plot(results['episode'], results['epsilon'], 'orange', linewidth=1)
    axes[1, 1].set_title('Exploration Rate (Epsilon)', fontweight='bold')
    axes[1, 1].set_xlabel('Episode')
    axes[1, 1].set_ylabel('Epsilon')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_plots_s1.png', dpi=300, bbox_inches='tight')
    plt.close()

def test_s1_model(agent, env, destinations):
    """Test the trained model"""
    print("   🧪 Testing trained model...")
    
    # Reset environment
    state = env.reset()
    total_reward = 0
    route_order = []
    
    while True:
        # Get valid actions
        valid_actions = []
        for i in range(len(env.vehicles)):
            for j in range(len(destinations)):
                if not destinations[j].get('visited', False):
                    valid_actions.append((i, j))
        
        if not valid_actions:
            break
        
        # Choose action (no exploration)
        original_epsilon = agent.epsilon
        agent.epsilon = 0.0
        
        action = agent.act(state, valid_actions)
        vehicle_id, destination_id = action
        
        # Take action
        next_state, reward, done = env.step(action)
        
        # Record route
        route_order.append({
            'vehicle': vehicle_id,
            'destination': destinations[destination_id]['route_name'],
            'reward': reward
        })
        
        state = next_state
        total_reward += reward
        
        if done:
            break
    
    # Print results
    print(f"   🎯 Final Reward: {total_reward:.2f}")
    print(f"   📍 Optimal Route untuk 4 Kota:")
    for i, step in enumerate(route_order):
        print(f"      {i+1}. Vehicle {step['vehicle']} → {step['destination']}")
    
    # Calculate utilization
    visited_count = sum(1 for dest in destinations if dest.get('visited', False))
    utilization = (visited_count / len(destinations)) * 100
    print(f"   📊 Final Utilization: {utilization:.1f}%")
    
    return {
        'final_reward': total_reward,
        'route_order': route_order,
        'utilization': utilization
    }

def print_summary(training_results, test_results):
    """Print training summary"""
    print("   📊 TRAINING SUMMARY:")
    print("   " + "-" * 40)
    
    # Training statistics
    final_rewards = training_results['total_reward'][-100:]  # Last 100 episodes
    final_utilization = training_results['utilization'][-100:]
    
    print(f"   🎯 Average Final Reward: {np.mean(final_rewards):.2f}")
    print(f"   📈 Average Utilization: {np.mean(final_utilization):.1f}%")
    print(f"   🧠 Final Epsilon: {training_results['epsilon'][-1]:.3f}")
    print(f"   📊 Test Results:")
    print(f"      - Final Reward: {test_results['final_reward']:.2f}")
    print(f"      - Route Utilization: {test_results['utilization']:.1f}%")
    print(f"      - Optimal Route Found: {'Yes' if test_results['utilization'] > 90 else 'Partial'}")
    
    print()
    print("   ✅ Training completed successfully!")
    print("   📝 Results ready for S1 skripsi analysis")

if __name__ == "__main__":
    simple_training_s1() 