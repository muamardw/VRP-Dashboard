#!/usr/bin/env python3
"""
Debug Environment untuk VRP DQN
"""

import numpy as np
import pandas as pd
from env.vrp_env import VRPDynamicEnv

def debug_environment():
    """Debug environment untuk menemukan masalah"""
    
    print("🔍 Debugging VRP Environment...")
    
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
    
    # Create environment
    env = VRPDynamicEnv(customers_df, n_vehicles=1)
    
    print(f"✅ Environment created successfully")
    print(f"✅ Number of customers: {env.n_customers}")
    print(f"✅ Max capacity: {env.max_capacity}")
    
    # Test environment reset
    state = env.reset()
    print(f"✅ Initial state shape: {state.shape}")
    print(f"✅ Initial state values: {state}")
    
    # Test valid actions
    valid_actions = list(range(env.n_customers))
    print(f"✅ Valid actions: {valid_actions}")
    
    # Test environment step
    for action in valid_actions:
        try:
            next_state, reward, done, info = env.step(action)
            print(f"✅ Action {action}: Reward={reward:.2f}, Done={done}, Info={info}")
            
            if done:
                print(f"⚠️ Episode ended after action {action}")
                break
                
        except Exception as e:
            print(f"❌ Error with action {action}: {e}")
    
    return env

def test_reward_function():
    """Test reward function components"""
    
    print("\n🎯 Testing Reward Function Components...")
    
    # Simulate different scenarios
    scenarios = [
        {"distance": 10, "travel_time": 2, "service_time": 1, "remaining_capacity": 3000, "visited_count": 1},
        {"distance": 50, "travel_time": 5, "service_time": 1, "remaining_capacity": 2000, "visited_count": 2},
        {"distance": 100, "travel_time": 10, "service_time": 1, "remaining_capacity": 1000, "visited_count": 3},
        {"distance": 0, "travel_time": 0, "service_time": 0, "remaining_capacity": 6000, "visited_count": 0},
    ]
    
    for i, scenario in enumerate(scenarios):
        # Simulate reward calculation
        distance_penalty = -scenario["distance"] * 0.1
        time_efficiency = 1.0 / (scenario["travel_time"] + scenario["service_time"] + 1e-6)
        utilization_bonus = (6000 - scenario["remaining_capacity"]) / 6000
        completion_bonus = 100 if scenario["visited_count"] == 4 else 0
        
        total_reward = distance_penalty + time_efficiency + utilization_bonus + completion_bonus
        
        print(f"Scenario {i+1}:")
        print(f"  Distance: {scenario['distance']}km, Travel Time: {scenario['travel_time']}h")
        print(f"  Distance Penalty: {distance_penalty:.2f}")
        print(f"  Time Efficiency: {time_efficiency:.2f}")
        print(f"  Utilization Bonus: {utilization_bonus:.2f}")
        print(f"  Completion Bonus: {completion_bonus}")
        print(f"  Total Reward: {total_reward:.2f}")
        print()

def analyze_training_results():
    """Analyze training results patterns"""
    
    print("\n📊 Analyzing Training Results Patterns...")
    
    print("❌ Masalah yang teridentifikasi:")
    print("1. Reward sangat volatil (-25 hingga 250)")
    print("2. Distance sering 0 km (model gagal)")
    print("3. Completion rate rendah dan tidak konsisten")
    print("4. Epsilon decay terlalu cepat")
    
    print("\n🔧 Solusi yang disarankan:")
    print("1. Simplify reward function")
    print("2. Adjust hyperparameters")
    print("3. Debug environment constraints")
    print("4. Increase exploration time")

if __name__ == "__main__":
    print("🚀 Debug VRP Environment and Training Issues")
    print("=" * 60)
    
    # Debug environment
    env = debug_environment()
    
    # Test reward function
    test_reward_function()
    
    # Analyze results
    analyze_training_results()
    
    print("\n💡 Next Steps:")
    print("1. Fix environment issues")
    print("2. Simplify reward function")
    print("3. Adjust hyperparameters")
    print("4. Re-run training") 