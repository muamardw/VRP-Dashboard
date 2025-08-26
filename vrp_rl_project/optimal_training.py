#!/usr/bin/env python3
"""
Optimal Training Script untuk DQN VRP
Menggunakan fixed environment dan model optimal
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import random
import yaml
from fixed_vrp_env import FixedVRPEnvironment

class OptimalDQNAgent:
    """Optimal DQN Agent dengan arsitektur yang sudah dioptimasi"""
    
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        # Optimal hyperparameters
        self.learning_rate = 0.0003
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.005
        self.epsilon_decay = 0.999
        self.memory_size = 100000
        self.batch_size = 64
        self.target_update = 5
        
        # Memory
        self.memory = deque(maxlen=self.memory_size)
        
        # Model (simplified for demonstration)
        self.q_table = {}  # Simple Q-table for now
        
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, valid_actions=None):
        """Choose action using epsilon-greedy policy"""
        if np.random.rand() <= self.epsilon:
            if valid_actions:
                return random.choice(valid_actions)
            return random.randrange(self.action_size)
        
        # Simple Q-value lookup
        state_key = tuple(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        return np.argmax(self.q_table[state_key])
    
    def replay(self):
        """Train the agent"""
        if len(self.memory) < self.batch_size:
            return 0.0
        
        batch = random.sample(self.memory, self.batch_size)
        total_loss = 0.0
        
        for state, action, reward, next_state, done in batch:
            state_key = tuple(state)
            next_state_key = tuple(next_state)
            
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(self.action_size)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = np.zeros(self.action_size)
            
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.q_table[next_state_key])
            
            target_f = self.q_table[state_key].copy()
            target_f[action] = target
            
            loss = np.mean((target_f - self.q_table[state_key]) ** 2)
            total_loss += loss
            
            self.q_table[state_key] = target_f
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return total_loss / self.batch_size

def create_training_data():
    """Create training data for VRP"""
    
    customers_data = {
        'latitude': [-6.1702, -6.2383, -6.5950, -6.1783],
        'longitude': [106.9417, 106.9756, 106.8167, 106.6319],
        'demand': [1700, 500, 2000, 700],
        'time_window_start': [0, 0, 0, 0],
        'time_window_end': [24, 24, 24, 24],
        'service_time': [1, 1, 1, 1]
    }
    
    return pd.DataFrame(customers_data)

def train_optimal_model():
    """Train model dengan environment yang sudah di-fix"""
    
    print("🚀 Starting Optimal DQN Training...")
    
    # Create environment
    customers_df = create_training_data()
    env = FixedVRPEnvironment(customers_df, n_vehicles=1)
    
    # Create agent
    state_size = 9  # Based on debug results
    action_size = 4
    agent = OptimalDQNAgent(state_size, action_size)
    
    # Training parameters
    episodes = 1000
    max_steps = 100
    
    # Tracking
    rewards_history = []
    distances_history = []
    completion_rates = []
    epsilons = []
    
    print(f"✅ Environment: {env.n_customers} customers")
    print(f"✅ Agent: {state_size} states, {action_size} actions")
    print(f"✅ Training: {episodes} episodes")
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        total_distance = 0
        steps = 0
        
        for step in range(max_steps):
            # Get valid actions
            valid_actions = [i for i in range(env.n_customers) if i not in env.visited_customers]
            
            # Choose action
            action = agent.act(state, valid_actions)
            
            # Take action
            next_state, reward, done, info = env.step(action)
            
            # Store experience
            agent.remember(state, action, reward, next_state, done)
            
            # Update tracking
            total_reward += reward
            total_distance = info.get('total_distance', 0.0)
            state = next_state
            steps += 1
            
            # Train agent
            if len(agent.memory) > agent.batch_size:
                loss = agent.replay()
            
            if done:
                break
        
        # Calculate completion rate
        completion_rate = len(env.visited_customers) / env.n_customers
        
        # Store history
        rewards_history.append(total_reward)
        distances_history.append(total_distance)
        completion_rates.append(completion_rate)
        epsilons.append(agent.epsilon)
        
        # Print progress
        if episode % 100 == 0:
            avg_reward = np.mean(rewards_history[-100:])
            avg_completion = np.mean(completion_rates[-100:])
            print(f"Episode {episode}: Reward={total_reward:.2f}, "
                  f"Distance={total_distance:.2f}km, "
                  f"Completion={completion_rate:.2f}, "
                  f"Epsilon={agent.epsilon:.3f}")
            print(f"  Avg Reward: {avg_reward:.2f}, Avg Completion: {avg_completion:.2f}")
    
    return agent, rewards_history, distances_history, completion_rates, epsilons

def plot_training_results(rewards, distances, completions, epsilons):
    """Plot training results"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Optimal DQN VRP Training Results', fontsize=16, fontweight='bold')
    
    # Reward progression
    ax1.plot(rewards, color='blue', alpha=0.7)
    ax1.set_title('Total Reward per Episode')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Reward')
    ax1.grid(True, alpha=0.3)
    
    # Distance progression
    ax2.plot(distances, color='red', alpha=0.7)
    ax2.set_title('Total Distance per Episode')
    ax2.set_xlabel('Episode')
    ax2.set_ylabel('Distance (km)')
    ax2.grid(True, alpha=0.3)
    
    # Completion rate
    ax3.plot(completions, color='green', alpha=0.7)
    ax3.set_title('Completion Rate per Episode')
    ax3.set_xlabel('Episode')
    ax3.set_ylabel('Completion Rate')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)
    
    # Epsilon decay
    ax4.plot(epsilons, color='orange', alpha=0.7)
    ax4.set_title('Epsilon Decay')
    ax4.set_xlabel('Episode')
    ax4.set_ylabel('Epsilon')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('optimal_training_results.png', dpi=300, bbox_inches='tight')
    print("✅ Training results saved as 'optimal_training_results.png'")

def analyze_results(rewards, distances, completions):
    """Analyze training results"""
    
    print("\n📊 Training Results Analysis:")
    print("=" * 50)
    
    # Final performance
    final_rewards = rewards[-100:]
    final_distances = distances[-100:]
    final_completions = completions[-100:]
    
    print(f"✅ Final 100 Episodes Performance:")
    print(f"  - Avg Reward: {np.mean(final_rewards):.2f}")
    print(f"  - Avg Distance: {np.mean(final_distances):.2f} km")
    print(f"  - Avg Completion Rate: {np.mean(final_completions):.2f}")
    print(f"  - Max Reward: {np.max(rewards):.2f}")
    print(f"  - Min Distance: {np.min(distances):.2f} km")
    print(f"  - Max Completion Rate: {np.max(completions):.2f}")
    
    # Convergence analysis
    early_rewards = rewards[:100]
    late_rewards = rewards[-100:]
    
    print(f"\n📈 Convergence Analysis:")
    print(f"  - Early Avg Reward: {np.mean(early_rewards):.2f}")
    print(f"  - Late Avg Reward: {np.mean(late_rewards):.2f}")
    print(f"  - Improvement: {np.mean(late_rewards) - np.mean(early_rewards):.2f}")
    
    if np.mean(late_rewards) > np.mean(early_rewards):
        print("  ✅ Model shows improvement!")
    else:
        print("  ⚠️ Model needs more training")

if __name__ == "__main__":
    print("🚀 Optimal DQN VRP Training")
    print("=" * 50)
    
    # Train model
    agent, rewards, distances, completions, epsilons = train_optimal_model()
    
    # Plot results
    plot_training_results(rewards, distances, completions, epsilons)
    
    # Analyze results
    analyze_results(rewards, distances, completions)
    
    print("\n🎉 Training completed!")
    print("💡 Check 'optimal_training_results.png' for visualizations") 