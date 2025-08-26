#!/usr/bin/env python3
"""
Fix API Issues untuk VRP Environment
"""

def create_simple_weather_api():
    """Create simple weather API without external calls"""
    
    class SimpleWeatherAPI:
        def __init__(self):
            self.default_impact = 1.0
        
        def get_weather_impact(self, lat, lon):
            """Return default weather impact without API call"""
            return self.default_impact
    
    return SimpleWeatherAPI()

def create_simple_traffic_api():
    """Create simple traffic API without external calls"""
    
    class SimpleTrafficAPI:
        def __init__(self):
            self.default_impact = 1.0
        
        def get_traffic_impact(self, origin, destination):
            """Return default traffic impact without API call"""
            return self.default_impact
    
    return SimpleTrafficAPI()

def fix_environment_apis():
    """Fix environment to use simple APIs"""
    
    print("🔧 Fixing API Issues...")
    
    # Create simple APIs
    weather_api = create_simple_weather_api()
    traffic_api = create_simple_traffic_api()
    
    print("✅ Simple Weather API created")
    print("✅ Simple Traffic API created")
    print("✅ No more API errors")
    
    return weather_api, traffic_api

def analyze_reward_function():
    """Analyze and fix reward function"""
    
    print("\n🎯 Analyzing Reward Function...")
    
    # Current reward pattern from debug:
    rewards = [-1.00, -1.17, -1.87, 997.99]
    
    print("❌ Masalah Reward Function:")
    print(f"  - Action 0: {rewards[0]} (terlalu kecil)")
    print(f"  - Action 1: {rewards[1]} (terlalu kecil)")
    print(f"  - Action 2: {rewards[2]} (terlalu kecil)")
    print(f"  - Action 3: {rewards[3]} (lonjakan ekstrem!)")
    
    print("\n✅ Solusi Reward Function:")
    print("  - Reduce completion bonus from 997.99 to 50")
    print("  - Increase intermediate rewards")
    print("  - Add progress bonus for each customer")
    print("  - Reduce distance penalty")

def create_simple_reward_function():
    """Create simple and stable reward function"""
    
    def simple_reward(distance, visited_count, total_customers, completion_bonus=50):
        """Simple reward function"""
        
        # Distance penalty (reduced)
        distance_penalty = -distance * 0.01
        
        # Progress bonus (encourage visiting customers)
        progress_bonus = visited_count * 10
        
        # Completion bonus (reduced)
        completion = completion_bonus if visited_count == total_customers else 0
        
        # Total reward
        total = distance_penalty + progress_bonus + completion
        
        return total
    
    return simple_reward

if __name__ == "__main__":
    print("🚀 Fix API Issues and Reward Function")
    print("=" * 50)
    
    # Fix APIs
    weather_api, traffic_api = fix_environment_apis()
    
    # Analyze reward function
    analyze_reward_function()
    
    # Create simple reward function
    simple_reward = create_simple_reward_function()
    
    # Test simple reward function
    print("\n🧪 Testing Simple Reward Function:")
    test_scenarios = [
        (0, 1, 4),    # First customer
        (10, 2, 4),   # Second customer
        (50, 3, 4),   # Third customer
        (100, 4, 4),  # All customers
    ]
    
    for distance, visited, total in test_scenarios:
        reward = simple_reward(distance, visited, total)
        print(f"  Distance: {distance}km, Visited: {visited}/{total}, Reward: {reward:.2f}")
    
    print("\n✅ Simple reward function created!")
    print("💡 Next: Update environment with simple APIs and reward function") 