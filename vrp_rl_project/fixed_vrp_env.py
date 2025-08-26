import gym
import numpy as np
from gym import spaces
from typing import Dict, List, Tuple, Optional
import pandas as pd

class SimpleWeatherAPI:
    """Simple weather API without external calls"""
    def __init__(self):
        self.default_impact = 1.0
    
    def get_weather_impact(self, lat, lon):
        return self.default_impact

class SimpleTrafficAPI:
    """Simple traffic API without external calls"""
    def __init__(self):
        self.default_impact = 1.0
    
    def get_traffic_impact(self, origin, destination):
        return self.default_impact

class FixedVRPEnvironment(gym.Env):
    """
    Fixed VRP Environment with simple APIs and stable reward function.
    """
    
    def __init__(self, customers_df, n_vehicles: int = 1):
        super(FixedVRPEnvironment, self).__init__()
        
        self.customers_df = customers_df
        self.n_customers = len(customers_df)
        self.n_vehicles = n_vehicles
        self.max_capacity = 6000
        
        # Use simple APIs
        self.weather_api = SimpleWeatherAPI()
        self.traffic_api = SimpleTrafficAPI()
        
        # Define action and observation space
        self.action_space = spaces.Discrete(self.n_customers)
        
        # State space: [current_location, remaining_capacity, time, 
        #              weather_impact, traffic_impact, unvisited_customers]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0] + [0] * self.n_customers),
            high=np.array([self.n_customers, self.max_capacity, 24, 2, 2] + [1] * self.n_customers),
            dtype=np.float32
        )
        
        self.reset()

    def reset(self):
        """Reset the environment to initial state."""
        self.current_location = 0  # Start at depot
        self.remaining_capacity = self.max_capacity
        self.current_time = 0
        self.visited_customers = set()
        self.total_distance = 0
        self.total_time = 0
        
        return self._get_state()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """Take a step in the environment."""
        
        if action in self.visited_customers:
            return self._get_state(), -1000, True, {'error': 'Customer already visited'}
            
        customer = self.customers_df.iloc[action]
        
        # Check capacity constraint
        if customer['demand'] > self.remaining_capacity:
            return self._get_state(), -1000, True, {'error': 'Capacity exceeded'}
        
        # Calculate distance (simplified)
        if self.current_location == 0:  # From depot
            distance = np.sqrt((customer['latitude'] + 6.2088)**2 + (customer['longitude'] - 106.8456)**2) * 111  # km
        else:
            prev_customer = self.customers_df.iloc[self.current_location]
            distance = np.sqrt((customer['latitude'] - prev_customer['latitude'])**2 + 
                             (customer['longitude'] - prev_customer['longitude'])**2) * 111  # km
        
        # Calculate travel time (simplified)
        travel_time = distance / 50  # Assuming 50 km/h
        
        # Update state
        self.current_location = action
        self.remaining_capacity -= customer['demand']
        self.current_time += travel_time + customer['service_time']
        self.visited_customers.add(action)
        self.total_distance += distance
        self.total_time += travel_time
        
        # Calculate reward using simple function
        reward = self._calculate_simple_reward(distance, len(self.visited_customers))
        
        # Check if episode is done
        done = len(self.visited_customers) == self.n_customers
        
        return self._get_state(), reward, done, {
            'total_distance': self.total_distance,
            'total_time': self.total_time,
            'visited_customers': len(self.visited_customers)
        }

    def _get_state(self) -> np.ndarray:
        """Get current state representation."""
        state = [
            self.current_location,
            self.remaining_capacity,
            self.current_time,
            self.weather_api.get_weather_impact(0, 0),  # Simple
            self.traffic_api.get_traffic_impact((0, 0), (0, 0)),  # Simple
        ]
        
        # Add unvisited customers status
        for i in range(self.n_customers):
            state.append(1.0 if i not in self.visited_customers else 0.0)
        
        return np.array(state, dtype=np.float32)

    def _calculate_simple_reward(self, distance: float, visited_count: int) -> float:
        """Simple and stable reward function."""
        
        # Distance penalty (reduced)
        distance_penalty = -distance * 0.01
        
        # Progress bonus (encourage visiting customers)
        progress_bonus = visited_count * 10
        
        # Completion bonus (reduced)
        completion_bonus = 50 if visited_count == self.n_customers else 0
        
        # Total reward
        total_reward = distance_penalty + progress_bonus + completion_bonus
        
        return total_reward

    def render(self, mode='human'):
        """Render the environment."""
        print(f"Location: {self.current_location}")
        print(f"Visited: {self.visited_customers}")
        print(f"Distance: {self.total_distance:.2f} km")
        print(f"Time: {self.total_time:.2f} h")

def test_fixed_environment():
    """Test the fixed environment."""
    
    print("🧪 Testing Fixed VRP Environment...")
    
    # Create sample data
    customers_data = {
        'latitude': [-6.1702, -6.2383, -6.5950, -6.1783],
        'longitude': [106.9417, 106.9756, 106.8167, 106.6319],
        'demand': [1700, 500, 2000, 700],
        'time_window_start': [0, 0, 0, 0],
        'time_window_end': [24, 24, 24, 24],
        'service_time': [1, 1, 1, 1]
    }
    
    customers_df = pd.DataFrame(customers_data)
    
    # Create fixed environment
    env = FixedVRPEnvironment(customers_df, n_vehicles=1)
    
    print(f"✅ Environment created successfully")
    print(f"✅ Number of customers: {env.n_customers}")
    print(f"✅ Max capacity: {env.max_capacity}")
    
    # Test environment
    state = env.reset()
    print(f"✅ Initial state shape: {state.shape}")
    print(f"✅ Initial state values: {state}")
    
    # Test actions
    for action in range(env.n_customers):
        next_state, reward, done, info = env.step(action)
        print(f"✅ Action {action}: Reward={reward:.2f}, Done={done}, Info={info}")
        
        if done:
            print(f"✅ Episode completed successfully!")
            break
    
    return env

if __name__ == "__main__":
    test_fixed_environment() 