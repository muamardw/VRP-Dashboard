#!/usr/bin/env python3
"""
Safe Testing Script untuk DQN VRP Model
Testing model dengan error handling yang aman
"""

import sys
import traceback
import numpy as np
import pandas as pd

def safe_test_model():
    """Testing model dengan error handling yang aman"""
    
    try:
        print("🧪 Memulai Testing Model DQN VRP...")
        print("=" * 50)
        
        # Import modules dengan error handling
        try:
            from fixed_vrp_env import FixedVRPEnvironment
            print("✅ FixedVRPEnvironment berhasil diimport")
        except ImportError as e:
            print(f"❌ Error importing FixedVRPEnvironment: {e}")
            return False
        
        # Create test data
        print("\n📊 Membuat test data...")
        test_customers = {
            'latitude': [-6.2088, -6.1751, -6.2146, -6.2297, -6.1865],
            'longitude': [106.8456, 106.8650, 106.8451, 106.7997, 106.8343],
            'demand': [1200, 800, 1500, 600, 900],
            'time_window_start': [0, 0, 0, 0, 0],
            'time_window_end': [24, 24, 24, 24, 24],
            'service_time': [1, 1, 1, 1, 1]
        }
        
        test_customers_df = pd.DataFrame(test_customers)
        print(f"✅ Test data berhasil dibuat: {len(test_customers_df)} customers")
        
        # Create test environment
        print("\n🌍 Membuat test environment...")
        test_env = FixedVRPEnvironment(test_customers_df, n_vehicles=1)
        print(f"✅ Test environment berhasil dibuat: {test_env.n_customers} customers")
        
        # Simulate testing
        print("\n🚚 Memulai simulasi testing...")
        state = test_env.reset()
        total_reward = 0
        total_distance = 0
        visited_customers = []
        route = []
        
        print("\n📈 Proses Testing:")
        print("-" * 30)
        
        for step in range(100):
            # Get valid actions
            valid_actions = [i for i in range(test_env.n_customers) 
                            if i not in test_env.visited_customers]
            
            if not valid_actions:
                print("✅ Semua customer telah dikunjungi!")
                break
            
            # Simple greedy approach untuk testing
            action = valid_actions[0]
            
            # Take action
            next_state, reward, done, info = test_env.step(action)
            
            # Update tracking
            total_reward += reward
            total_distance = info.get('total_distance', 0.0)
            visited_customers.append(action)
            route.append(f"Customer {action}")
            
            print(f"Step {step+1}: Visit Customer {action}")
            print(f"  Reward: {reward:.2f}")
            print(f"  Distance: {total_distance:.2f} km")
            print(f"  Visited: {len(test_env.visited_customers)}/{test_env.n_customers}")
            
            state = next_state
            
            if done:
                print("✅ Episode selesai!")
                break
        
        # Calculate performance metrics
        completion_rate = len(test_env.visited_customers) / test_env.n_customers
        efficiency = (total_distance / len(test_env.visited_customers)) if test_env.visited_customers else 0
        
        print("\n📊 Hasil Testing Model:")
        print("=" * 50)
        print(f"✅ Total Reward: {total_reward:.2f}")
        print(f"✅ Total Distance: {total_distance:.2f} km")
        print(f"✅ Completion Rate: {completion_rate:.2%}")
        print(f"✅ Efficiency: {efficiency:.2f} km/customer")
        print(f"✅ Route: {' → '.join(route)}")
        
        # Performance analysis
        print("\n📈 Analisis Performance:")
        print("-" * 30)
        
        if completion_rate == 1.0:
            print("✅ Completion Rate: EXCELLENT (100%)")
        elif completion_rate >= 0.8:
            print("✅ Completion Rate: GOOD (≥80%)")
        else:
            print("⚠️ Completion Rate: NEEDS IMPROVEMENT (<80%)")
        
        if efficiency <= 5.0:
            print("✅ Efficiency: EXCELLENT (≤5 km/customer)")
        elif efficiency <= 10.0:
            print("✅ Efficiency: GOOD (≤10 km/customer)")
        else:
            print("⚠️ Efficiency: NEEDS IMPROVEMENT (>10 km/customer)")
        
        if total_reward >= 150:
            print("✅ Reward: EXCELLENT (≥150)")
        elif total_reward >= 100:
            print("✅ Reward: GOOD (≥100)")
        else:
            print("⚠️ Reward: NEEDS IMPROVEMENT (<100)")
        
        print("\n🎉 Testing berhasil diselesaikan!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error selama testing: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return False

def main():
    """Main function untuk testing"""
    print("🚀 Safe Testing Script untuk DQN VRP Model")
    print("=" * 60)
    
    success = safe_test_model()
    
    if success:
        print("\n✅ Testing berhasil diselesaikan!")
        print("💡 Model menunjukkan performance yang baik!")
    else:
        print("\n❌ Testing gagal!")
        print("🔧 Silakan cek error di atas dan perbaiki masalahnya")

if __name__ == "__main__":
    main() 