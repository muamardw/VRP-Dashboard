import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
import os

@dataclass
class RouteData:
    route_name: str
    branch_code: str
    distance_km: float
    capacity_kg: float
    load_kg: float
    remaining_capacity: float
    utilization_percent: float

class ImprovedDQN(nn.Module):
    def __init__(self, state_size: int, action_size: int):
        super(ImprovedDQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, action_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x

class ImprovedDQNAgent:
    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.0005
        self.batch_size = 64
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.q_network = ImprovedDQN(state_size, action_size).to(self.device)
        self.target_network = ImprovedDQN(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()
        
        self.update_target_network()
        
    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor)
        return np.argmax(q_values.cpu().data.numpy())
        
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
            
        batch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor([data[0] for data in batch]).to(self.device)
        actions = torch.LongTensor([data[1] for data in batch]).to(self.device)
        rewards = torch.FloatTensor([data[2] for data in batch]).to(self.device)
        next_states = torch.FloatTensor([data[3] for data in batch]).to(self.device)
        dones = torch.BoolTensor([data[4] for data in batch]).to(self.device)
        
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (self.gamma * next_q_values * ~dones)
        
        loss = self.criterion(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def save(self, filename):
        torch.save(self.q_network.state_dict(), filename)
        
    def load(self, filename):
        self.q_network.load_state_dict(torch.load(filename))

class ImprovedVRPEnvironment:
    def __init__(self, destinations: List[RouteData]):
        self.destinations = destinations
        self.reset()
        
    def reset(self):
        self.current_state = self._get_initial_state()
        self.visited = [False] * len(self.destinations)
        self.total_distance = 0
        self.total_reward = 0
        self.steps = 0
        return self.current_state
        
    def _get_initial_state(self):
        # State: [vehicle_pos_x, vehicle_pos_y, visited_status, distances, capacities]
        state = []
        
        # Vehicle position (depot at origin)
        state.extend([0.0, 0.0])
        
        # Visited status for each destination
        state.extend([0.0] * len(self.destinations))
        
        # Distances to each destination
        for dest in self.destinations:
            state.append(dest.distance_km)
            
        # Capacities and loads
        for dest in self.destinations:
            state.append(dest.capacity_kg)
            state.append(dest.load_kg)
            
        return np.array(state, dtype=np.float32)
        
    def step(self, action):
        self.steps += 1
        
        if action >= len(self.destinations):
            # Return to depot
            reward = -10  # Penalty for invalid action
            done = True
        else:
            if self.visited[action]:
                reward = -50  # Penalty for visiting same place
                done = True
            else:
                # Visit destination
                dest = self.destinations[action]
                self.visited[action] = True
                
                # Calculate reward based on distance and utilization
                distance_penalty = -dest.distance_km * 0.1
                utilization_bonus = dest.utilization_percent * 0.5
                reward = distance_penalty + utilization_bonus
                
                self.total_distance += dest.distance_km
                self.total_reward += reward
                
                # Check if all destinations visited
                if all(self.visited):
                    reward += 100  # Bonus for completing all routes
                    done = True
                else:
                    done = False
                    
        # Update state
        self.current_state = self._get_state()
        
        return self.current_state, reward, done
        
    def _get_state(self):
        state = []
        
        # Vehicle position (simplified)
        state.extend([0.0, 0.0])
        
        # Visited status
        state.extend([1.0 if visited else 0.0 for visited in self.visited])
        
        # Distances
        for dest in self.destinations:
            state.append(dest.distance_km)
            
        # Capacities and loads
        for dest in self.destinations:
            state.append(dest.capacity_kg)
            state.append(dest.load_kg)
            
        return np.array(state, dtype=np.float32)

def improved_training():
    """Improved training with better parameters and environment"""
    
    # PT. Sanghiang Perkasa data
    destinations = [
        RouteData("Jakarta", "C27", 0.5, 2000, 1700, 300, 85),
        RouteData("Bekasi", "C28", 10.0, 1000, 500, 500, 50),
        RouteData("Bogor", "C29", 60.0, 2000, 2000, 0, 100),
        RouteData("Tangerang", "C30", 55.0, 1000, 700, 300, 70)
    ]
    
    # Environment setup
    env = ImprovedVRPEnvironment(destinations)
    state_size = len(env.reset())
    action_size = len(destinations) + 1  # +1 for return to depot
    
    # Agent setup
    agent = ImprovedDQNAgent(state_size, action_size)
    
    # Training parameters
    episodes = 1000
    max_steps = 50
    
    # Results storage
    training_results = {
        'episode': [],
        'total_reward': [],
        'total_distance': [],
        'visited_customers': [],
        'epsilon': [],
        'completion_rate': []
    }
    
    print("🚀 Starting Improved DQN Training...")
    print(f"📊 Episodes: {episodes}")
    print(f"🎯 State Size: {state_size}, Action Size: {action_size}")
    print()
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        total_distance = 0
        visited_count = 0
        
        for step in range(max_steps):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            
            state = next_state
            total_reward += reward
            total_distance = env.total_distance
            visited_count = sum(env.visited)
            
            if done:
                break
                
        # Update target network every 10 episodes
        if episode % 10 == 0:
            agent.update_target_network()
            
        # Store results
        training_results['episode'].append(episode)
        training_results['total_reward'].append(total_reward)
        training_results['total_distance'].append(total_distance)
        training_results['visited_customers'].append(visited_count)
        training_results['epsilon'].append(agent.epsilon)
        training_results['completion_rate'].append(visited_count / len(destinations))
        
        # Print progress
        if episode % 100 == 0 or episode == episodes - 1:
            avg_reward = np.mean(training_results['total_reward'][-100:])
            avg_distance = np.mean(training_results['total_distance'][-100:])
            avg_completion = np.mean(training_results['completion_rate'][-100:])
            
            print(f"Episode {episode:4d} | Reward: {total_reward:8.2f} | "
                  f"Distance: {total_distance:6.2f} | Visited: {visited_count}/{len(destinations)} | "
                  f"Completion: {avg_completion:.2%} | Epsilon: {agent.epsilon:.3f}")
    
    print("\n✅ Training Completed!")
    
    # Save results
    df = pd.DataFrame(training_results)
    df.to_csv('improved_training_results.csv', index=False)
    print("💾 Results saved to: improved_training_results.csv")
    
    # Save model
    agent.save('improved_dqn_model.pth')
    print("💾 Model saved to: improved_dqn_model.pth")
    
    # Create plots
    create_improved_plots(training_results)
    
    return agent, env, training_results

def create_improved_plots(results):
    """Create improved training plots"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Reward over episodes
    ax1.plot(results['episode'], results['total_reward'])
    ax1.set_title('Total Reward per Episode')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Reward')
    ax1.grid(True)
    
    # Distance over episodes
    ax2.plot(results['episode'], results['total_distance'])
    ax2.set_title('Total Distance per Episode')
    ax2.set_xlabel('Episode')
    ax2.set_ylabel('Distance (km)')
    ax2.grid(True)
    
    # Completion rate over episodes
    ax3.plot(results['episode'], results['completion_rate'])
    ax3.set_title('Completion Rate per Episode')
    ax3.set_xlabel('Episode')
    ax3.set_ylabel('Completion Rate')
    ax3.grid(True)
    
    # Epsilon decay
    ax4.plot(results['episode'], results['epsilon'])
    ax4.set_title('Epsilon Decay')
    ax4.set_xlabel('Episode')
    ax4.set_ylabel('Epsilon')
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('improved_training_plots.png', dpi=300, bbox_inches='tight')
    print("📊 Plots saved to: improved_training_plots.png")

if __name__ == "__main__":
    improved_training() 