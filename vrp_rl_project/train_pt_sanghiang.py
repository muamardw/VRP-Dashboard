#!/usr/bin/env python3
"""
Training script untuk DQN dengan data PT. Sanghiang Perkasa
"""

import numpy as np
import torch
from dqn_model import DQNAgent, VRPEnvironment
from pt_sanghiang_data import PTSanghiangDataProcessor
from backend_api import get_weather_data
import matplotlib.pyplot as plt

def train_dqn_pt_sanghiang():
    """Train DQN model dengan data PT. Sanghiang Perkasa"""
    
    print("🚀 Training DQN Model dengan Data PT. Sanghiang Perkasa")
    print("=" * 60)
    
    # Load PT. Sanghiang Perkasa data
    processor = PTSanghiangDataProcessor()
    optimization_data = processor.get_optimization_data(jabodetabek_only=True)
    
    print(f"📊 Data: {len(optimization_data)} rute Jabodetabek")
    
    # Prepare training data
    vehicles = []
    destinations = []
    
    # Depot (Cikampek)
    depot = {"position": {"lat": -6.4194, "lng": 107.4515}}
    
    # Create vehicles
    for i, route in enumerate(optimization_data[:3]):  # Use 3 routes for training
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
            "route_id": route["route_id"]
        }
        destinations.append(destination)
    
    print(f"🚛 Vehicles: {len(vehicles)}")
    print(f"📍 Destinations: {len(destinations)}")
    
    # Get weather data
    weather_data = get_weather_data(depot["position"]["lat"], depot["position"]["lng"])
    traffic_data = {"factor": 1.2}  # Default traffic factor
    
    print(f"🌤️ Weather: {weather_data['description']}, {weather_data['temperature']}°C")
    
    # Create environment
    env = VRPEnvironment(vehicles, destinations, weather_data, traffic_data)
    
    # Initialize DQN agent
    state_size = len(env.current_state)
    action_size = len(vehicles) * len(destinations)
    
    print(f"🧠 State size: {state_size}")
    print(f"🎯 Action size: {action_size}")
    
    agent = DQNAgent(state_size, action_size)
    
    # Training parameters
    episodes = 1000
    max_steps = 50
    batch_size = 32
    
    # Training history
    episode_rewards = []
    episode_distances = []
    episode_utilization = []
    
    print("\n🎮 Starting Training...")
    print("-" * 40)
    
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
            total_distance += abs(reward)  # Approximate distance from reward
            steps += 1
            
            if done:
                break
        
        # Calculate utilization
        visited_count = sum(1 for dest in destinations if dest.get('visited', False))
        utilization = (visited_count / len(destinations)) * 100
        
        # Store metrics
        episode_rewards.append(total_reward)
        episode_distances.append(total_distance)
        episode_utilization.append(utilization)
        
        # Print progress
        if episode % 100 == 0:
            avg_reward = np.mean(episode_rewards[-100:])
            avg_utilization = np.mean(episode_utilization[-100:])
            print(f"Episode {episode:4d} | Reward: {total_reward:8.2f} | "
                  f"Distance: {total_distance:6.2f} | Utilization: {utilization:5.1f}% | "
                  f"Epsilon: {agent.epsilon:.3f}")
    
    print("\n✅ Training Completed!")
    
    # Save model
    model_path = "dqn_pt_sanghiang_model.pth"
    agent.save(model_path)
    print(f"💾 Model saved to: {model_path}")
    
    # Plot training results
    plot_training_results(episode_rewards, episode_distances, episode_utilization)
    
    # Test trained model
    test_trained_model(agent, env, destinations)
    
    return agent, env

def plot_training_results(rewards, distances, utilization):
    """Plot training results"""
    plt.figure(figsize=(15, 5))
    
    # Plot rewards
    plt.subplot(1, 3, 1)
    plt.plot(rewards)
    plt.title('Training Rewards')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    
    # Plot distances
    plt.subplot(1, 3, 2)
    plt.plot(distances)
    plt.title('Total Distance')
    plt.xlabel('Episode')
    plt.ylabel('Distance')
    
    # Plot utilization
    plt.subplot(1, 3, 3)
    plt.plot(utilization)
    plt.title('Route Utilization')
    plt.xlabel('Episode')
    plt.ylabel('Utilization (%)')
    
    plt.tight_layout()
    plt.savefig('training_results_pt_sanghiang.png')
    plt.close()
    print("📊 Training plots saved to: training_results_pt_sanghiang.png")

def test_trained_model(agent, env, destinations):
    """Test the trained model"""
    print("\n🧪 Testing Trained Model...")
    print("-" * 40)
    
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
        agent.epsilon = 0.0  # No exploration
        
        action = agent.act(state, valid_actions)
        vehicle_id, destination_id = action
        
        # Take action
        next_state, reward, done = env.step(action)
        
        # Record route
        route_order.append({
            'vehicle': vehicle_id,
            'destination': destinations[destination_id]['route_id'],
            'reward': reward
        })
        
        state = next_state
        total_reward += reward
        
        if done:
            break
    
    # Print results
    print(f"🎯 Final Reward: {total_reward:.2f}")
    print(f"📍 Route Order:")
    for i, step in enumerate(route_order):
        print(f"   {i+1}. Vehicle {step['vehicle']} → {step['destination']} (reward: {step['reward']:.2f})")
    
    # Calculate utilization
    visited_count = sum(1 for dest in destinations if dest.get('visited', False))
    utilization = (visited_count / len(destinations)) * 100
    print(f"📊 Final Utilization: {utilization:.1f}%")

if __name__ == "__main__":
    train_dqn_pt_sanghiang() 