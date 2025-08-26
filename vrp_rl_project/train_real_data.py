#!/usr/bin/env python3
"""
Script training DQN VRP menggunakan data real PT. Sanghiang Perkasa (4 destinasi).
Menggantikan training dengan data simulasi 50 customer.
"""

import argparse
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import os

from utils import load_config, save_results, plot_route
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent

def train_model_real_data(env: VRPDynamicEnv, agent: DQNAgent, config: Dict) -> Dict:
    """
    Train DQN agent dengan data real (4 destinasi).
    
    Args:
        env: VRP environment dengan data real
        agent: DQN agent
        config: Configuration dictionary
        
    Returns:
        Dictionary containing training results
    """
    episodes = config['training']['episodes']
    max_steps = config['training']['max_steps']
    save_interval = config['training']['save_interval']
    
    results = {
        'episode': [],
        'total_reward': [],
        'total_distance': [],
        'total_time': [],
        'visited_customers': [],
        'epsilon': []
    }
    
    print(f"🚚 Training DQN VRP dengan Data Real PT. Sanghiang Perkasa")
    print(f"📊 Episodes: {episodes}")
    print(f"🎯 Destinasi: 4 (Bogor, Tangerang, Jakarta, Bekasi)")
    print(f"🏢 Depot: Pulo Gadung, Jakarta Timur")
    print("=" * 60)
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        
        for step in range(max_steps):
            # Get valid actions (unvisited customers)
            valid_actions = [i for i in range(env.n_customers) 
                           if i not in env.visited_customers]
            
            # Choose action
            action = agent.act(state, valid_actions)
            
            # Take action
            next_state, reward, done, info = env.step(action)
            
            # Store experience
            agent.remember(state, action, reward, next_state, done)
            
            # Train agent
            loss = agent.replay()
            
            state = next_state
            total_reward += reward
            
            if done:
                break
        
        # Update target network
        if episode % agent.target_update == 0:
            agent.update_target_model()
        
        # Save results
        results['episode'].append(episode)
        results['total_reward'].append(total_reward)
        results['total_distance'].append(info.get('total_distance', 0))
        results['total_time'].append(info.get('total_time', 0))
        results['visited_customers'].append(info.get('visited_customers', 0))
        results['epsilon'].append(agent.epsilon)
        
        # Save model
        if episode % save_interval == 0:
            agent.save(f'model/checkpoints/dqn_real_episode_{episode}.weights.h5')
        
        # Print progress
        if episode % 50 == 0 or episode == episodes - 1:
            print(f"Episode: {episode:4d} | Reward: {total_reward:8.2f} | "
                  f"Distance: {info.get('total_distance', 0):6.2f} km | "
                  f"Time: {info.get('total_time', 0):5.2f} jam | "
                  f"Visited: {info.get('visited_customers', 0):2d}/4 | "
                  f"Epsilon: {agent.epsilon:.3f}")
    
    return results

def plot_training_results_real(results: Dict):
    """
    Plot training results untuk data real.
    
    Args:
        results: Dictionary containing training results
    """
    plt.figure(figsize=(15, 12))
    
    # Plot total reward
    plt.subplot(3, 2, 1)
    plt.plot(results['episode'], results['total_reward'])
    plt.title('Total Reward per Episode (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True)
    
    # Plot total distance
    plt.subplot(3, 2, 2)
    plt.plot(results['episode'], results['total_distance'])
    plt.title('Total Distance per Episode (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Total Distance (km)')
    plt.grid(True)
    
    # Plot total time
    plt.subplot(3, 2, 3)
    plt.plot(results['episode'], results['total_time'])
    plt.title('Total Time per Episode (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Total Time (hours)')
    plt.grid(True)
    
    # Plot visited customers
    plt.subplot(3, 2, 4)
    plt.plot(results['episode'], results['visited_customers'])
    plt.title('Visited Customers per Episode (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Number of Customers')
    plt.ylim(0, 4)
    plt.grid(True)
    
    # Plot epsilon decay
    plt.subplot(3, 2, 5)
    plt.plot(results['episode'], results['epsilon'])
    plt.title('Epsilon Decay (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Epsilon')
    plt.grid(True)
    
    # Plot reward moving average
    plt.subplot(3, 2, 6)
    window = 50
    moving_avg = pd.Series(results['total_reward']).rolling(window=window).mean()
    plt.plot(results['episode'], results['total_reward'], alpha=0.3, label='Raw')
    plt.plot(results['episode'], moving_avg, label=f'{window}-episode MA')
    plt.title('Reward Moving Average (Data Real)')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('data/training_results_real.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Grafik training disimpan: data/training_results_real.png")

def evaluate_model_real(env: VRPDynamicEnv, agent: DQNAgent) -> Dict:
    """
    Evaluate trained DQN agent dengan data real.
    
    Args:
        env: VRP environment dengan data real
        agent: DQN agent
        
    Returns:
        Dictionary containing evaluation results
    """
    state = env.reset()
    total_reward = 0
    route = []
    
    print(f"\n🔍 Evaluasi Model (Greedy Policy)")
    print("=" * 40)
    
    while True:
        # Get valid actions
        valid_actions = [i for i in range(env.n_customers) 
                        if i not in env.visited_customers]
        
        # Choose action (greedy)
        action = agent.act(state, valid_actions)
        
        # Take action
        next_state, reward, done, info = env.step(action)
        
        # Update state and reward
        state = next_state
        total_reward += reward
        
        # Record route
        if action > 0:  # Skip depot
            customer = env.customers_df.iloc[action]
            route.append((customer['latitude'], customer['longitude']))
            print(f"📍 Customer {action}: ({customer['latitude']:.4f}, {customer['longitude']:.4f})")
        
        if done:
            break
    
    return {
        'total_reward': total_reward,
        'total_distance': info.get('total_distance', 0),
        'total_time': info.get('total_time', 0),
        'visited_customers': info.get('visited_customers', 0),
        'route': route
    }

def main():
    """Main function untuk training dengan data real."""
    parser = argparse.ArgumentParser(description='VRP with RL - Data Real')
    parser.add_argument('--train', action='store_true',
                       help='Train the model dengan data real')
    parser.add_argument('--evaluate', action='store_true',
                       help='Evaluate the model dengan data real')
    parser.add_argument('--episodes', type=int, default=1000,
                       help='Number of training episodes')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Override episodes if specified
    if args.episodes:
        config['training']['episodes'] = args.episodes
    
    if args.train:
        # Load data real
        if not os.path.exists('data/real_shipments.csv'):
            print("❌ File data/real_shipments.csv tidak ditemukan!")
            print("💡 Jalankan dulu: python create_real_dataset.py")
            return
        
        customers_df = pd.read_csv('data/real_shipments.csv')
        print(f"✅ Loaded data real: {len(customers_df)} baris (1 depot + 4 destinasi)")
        
        # Create environment and agent
        env = VRPDynamicEnv(customers_df, n_vehicles=1)  # 1 kendaraan untuk 4 destinasi
        agent = DQNAgent(
            state_size=env.observation_space.shape[0],  # 9 dimensi
            action_size=env.action_space.n,             # 4 aksi (destinasi)
            config=config
        )
        
        # Train model
        results = train_model_real_data(env, agent, config)
        
        # Save results
        save_results(results, 'training_results_real.csv')
        plot_training_results_real(results)
        
        # Save final model
        agent.save('model/dqn_real_final.weights.h5')
        print(f"\n✅ Training selesai!")
        print(f"💾 Model disimpan: model/dqn_real_final.weights.h5")
    
    if args.evaluate:
        # Load data real
        customers_df = pd.read_csv('data/real_shipments.csv')
        env = VRPDynamicEnv(customers_df, n_vehicles=1)
        agent = DQNAgent(
            state_size=env.observation_space.shape[0],
            action_size=env.action_space.n,
            config=config
        )
        
        # Load trained model
        model_path = 'model/dqn_real_final.weights.h5'
        if os.path.exists(model_path):
            agent.load(model_path)
            print(f"✅ Loaded model: {model_path}")
        else:
            print(f"⚠️ Model {model_path} tidak ditemukan, menggunakan model random")
        
        # Evaluate model
        results = evaluate_model_real(env, agent)
        
        print(f"\n📊 Hasil Evaluasi (Data Real):")
        print(f"   Total Reward: {results['total_reward']:.2f}")
        print(f"   Total Distance: {results['total_distance']:.2f} km")
        print(f"   Total Time: {results['total_time']:.2f} jam")
        print(f"   Visited Customers: {results['visited_customers']}/4")
        
        # Plot route
        if results['route']:
            plot_route(results['route'], customers_df, "Optimal Route (Data Real)")

if __name__ == '__main__':
    main() 