import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

class VRPEnvironment:
    def __init__(self, num_destinations=4):  # Changed from 7 to 4
        self.num_destinations = num_destinations
        self.reset()
        
        # State space: vehicle positions (4) + destination status (4) + weather (5) + traffic (2) + current load (2) + time (2) = 19
        self.state_size = 19  # Updated for 4 destinations
        # Action space: 4 destinations + 1 depot = 5 actions
        self.action_size = 5  # Changed from 8 to 5
        
        # PT. Sanghiang Perkasa data - 4 destinations Jabodetabek
        self.destinations = [
            {'name': 'Bogor', 'distance': 60, 'capacity': 2000, 'load': 2000, 'utilization': 100},
            {'name': 'Tangerang', 'distance': 55, 'capacity': 1000, 'load': 700, 'utilization': 70},
            {'name': 'Jakarta', 'distance': 17, 'capacity': 2000, 'load': 1700, 'utilization': 85},
            {'name': 'Bekasi', 'distance': 10, 'capacity': 1000, 'load': 500, 'utilization': 50}
        ]

    def _get_initial_state(self):
        # State: [vehicle_positions, weather_conditions, traffic_conditions, remaining_destinations]
        state = []
        # Vehicle positions (lat, lng for each vehicle)
        for vehicle in self.vehicles:
            state.extend([vehicle['position']['lat'], vehicle['position']['lng']])
        # Weather conditions
        state.extend([
            self.weather_data['temperature'],
            self.weather_data['humidity'],
            self.weather_data['wind_speed'],
            self.weather_data['rain']
        ])
        # Traffic conditions (simplified)
        state.append(self.traffic_data.get('factor', 1.0))
        # Remaining destinations (binary: 1 if not visited)
        for dest in self.destinations:
            state.append(1 if not dest.get('visited', False) else 0)
        return np.array(state)
    
    def step(self, action):
        # Action: [vehicle_id, destination_id]
        vehicle_id, destination_id = action
        
        # Calculate reward based on:
        # - Distance to destination
        # - Traffic conditions
        # - Weather impact
        # - Time efficiency
        
        reward = self._calculate_reward(vehicle_id, destination_id)
        
        # Update state
        self._update_state(vehicle_id, destination_id)
        
        # Check if episode is done
        done = self._is_episode_done()
        
        return self.current_state, reward, done
    
    def _calculate_reward(self, vehicle_id, destination_id):
        # Base reward: negative distance
        distance = self._calculate_distance(vehicle_id, destination_id)
        base_reward = -distance
        
        # Traffic penalty
        traffic_penalty = self.traffic_data.get('factor', 1.0) * 0.1
        
        # Weather penalty
        weather_penalty = 0
        if self.weather_data['rain'] > 0:
            weather_penalty = 0.2
        if self.weather_data['wind_speed'] > 20:
            weather_penalty += 0.1
            
        total_reward = base_reward - traffic_penalty - weather_penalty
        return total_reward
    
    def _calculate_distance(self, vehicle_id, destination_id):
        # Simplified distance calculation
        vehicle = self.vehicles[vehicle_id]
        destination = self.destinations[destination_id]
        
        lat1, lng1 = vehicle['position']['lat'], vehicle['position']['lng']
        lat2, lng2 = destination['lat'], destination['lng']
        
        # Haversine distance
        R = 6371  # Earth's radius in km
        dlat = np.radians(lat2 - lat1)
        dlng = np.radians(lng2 - lng1)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlng/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def _update_state(self, vehicle_id, destination_id):
        # Update vehicle position
        self.vehicles[vehicle_id]['position'] = {
            'lat': self.destinations[destination_id]['lat'],
            'lng': self.destinations[destination_id]['lng']
        }
        
        # Mark destination as visited
        self.destinations[destination_id]['visited'] = True
        
        # Update current state
        self.current_state = self._get_initial_state()
    
    def _is_episode_done(self):
        # Check if all destinations are visited
        return all(dest.get('visited', False) for dest in self.destinations)
    
    def reset(self):
        # Reset environment to initial state
        for dest in self.destinations:
            dest['visited'] = False
        self.current_state = self._get_initial_state()
        return self.current_state

class DQNAgent:
    def __init__(self, state_size, action_size, num_destinations=4):  # Changed from 7 to 4
        self.state_size = state_size
        self.action_size = action_size
        self.num_destinations = num_destinations
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def act(self, state, valid_actions):
        if np.random.random() <= self.epsilon:
            return random.choice(valid_actions)
        
        # Convert state to tensor and get Q-values
        state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Add batch dimension
        act_values = self.model(state_tensor).squeeze(0)  # Remove batch dimension
        
        # Convert action tuples to indices
        action_indices = []
        for vehicle_id, destination_id in valid_actions:
            action_idx = vehicle_id * self.num_destinations + destination_id
            action_indices.append(action_idx)
        
        # Get Q-values for valid actions
        valid_q_values = [act_values[idx].item() for idx in action_indices]
        
        # Return the action with highest Q-value
        best_idx = np.argmax(valid_q_values)
        return valid_actions[best_idx]
        
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            # Convert action tuple to index
            vehicle_id, destination_id = action
            action_idx = vehicle_id * self.num_destinations + destination_id
            
            target = reward
            if not done:
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * torch.max(self.target_model(next_state_tensor)).item()
            
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state_tensor).squeeze(0)
            target_f[action_idx] = target
            
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(self.model(state_tensor).squeeze(0), target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        self.model.load_state_dict(torch.load(name))
        
    def save(self, name):
        torch.save(self.model.state_dict(), name) 