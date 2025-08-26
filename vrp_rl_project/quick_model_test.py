#!/usr/bin/env python3
"""
Quick Test untuk Model DQN VRP Advanced yang Dioptimasi
"""

import numpy as np
import yaml

def test_advanced_model():
    """Test model DQN advanced dengan parameter optimal"""
    
    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Model parameters
    state_size = 19
    action_size = 4
    hidden_layers = config['model']['hidden_layers']
    learning_rate = config['model']['learning_rate']
    
    print("🧪 Testing Advanced DQN Model Configuration...")
    print(f"State Size: {state_size}")
    print(f"Action Size: {action_size}")
    print(f"Hidden Layers: {hidden_layers}")
    print(f"Learning Rate: {learning_rate}")
    
    # Calculate total parameters (simulation)
    total_params = 0
    prev_layer = state_size
    
    for i, layer_size in enumerate(hidden_layers):
        params = prev_layer * layer_size + layer_size  # weights + biases
        total_params += params
        print(f"Hidden Layer {i+1} ({layer_size} neurons): {params:,} parameters")
        prev_layer = layer_size
    
    # Output layer
    output_params = prev_layer * action_size + action_size
    total_params += output_params
    print(f"Output Layer ({action_size} neurons): {output_params:,} parameters")
    
    print(f"✅ Total parameters: {total_params:,}")
    
    # Test with sample data
    sample_state = np.random.rand(1, state_size)
    print(f"✅ Sample state shape: {sample_state.shape}")
    print(f"✅ Sample state values: {sample_state[0][:5]}...")  # Show first 5 values
    
    return total_params

def test_advanced_hyperparameters():
    """Test hyperparameters advanced optimal"""
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    print("\n🔧 Advanced Hyperparameters Test:")
    print(f"✅ Learning Rate: {config['model']['learning_rate']}")
    print(f"✅ Memory Size: {config['model']['memory_size']:,}")
    print(f"✅ Batch Size: {config['model']['batch_size']}")
    print(f"✅ Episodes: {config['training']['episodes']}")
    print(f"✅ Hidden Layers: {config['model']['hidden_layers']}")
    print(f"✅ Gamma: {config['model']['gamma']}")
    print(f"✅ Epsilon Start: {config['model']['epsilon_start']}")
    print(f"✅ Epsilon End: {config['model']['epsilon_end']}")
    print(f"✅ Epsilon Decay: {config['model']['epsilon_decay']}")
    print(f"✅ Target Update: {config['model']['target_update']}")
    print(f"✅ Dropout Rate: {config['model']['dropout_rate']}")
    print(f"✅ Max Steps: {config['training']['max_steps']}")
    print(f"✅ Early Stopping Patience: {config['training']['early_stopping_patience']}")
    
    # Validate advanced parameters
    assert config['model']['learning_rate'] == 0.0003, "Learning rate harus 0.0003"
    assert config['model']['memory_size'] == 100000, "Memory size harus 100000"
    assert config['model']['batch_size'] == 64, "Batch size harus 64"
    assert config['training']['episodes'] == 3000, "Episodes harus 3000"
    assert config['model']['hidden_layers'] == [512, 256, 256, 128], "Hidden layers harus [512, 256, 256, 128]"
    assert config['model']['epsilon_end'] == 0.005, "Epsilon end harus 0.005"
    assert config['model']['epsilon_decay'] == 0.999, "Epsilon decay harus 0.999"
    assert config['model']['target_update'] == 5, "Target update harus 5"
    
    print("✅ Semua advanced hyperparameters optimal!")

def test_advanced_features():
    """Test advanced DQN features"""
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    print("\n🚀 Advanced DQN Features Test:")
    print(f"✅ Double DQN: {config['advanced_dqn']['double_dqn']}")
    print(f"✅ Dueling DQN: {config['advanced_dqn']['dueling_dqn']}")
    print(f"✅ Prioritized Replay: {config['advanced_dqn']['prioritized_replay']}")
    print(f"✅ N-step Learning: {config['advanced_dqn']['n_step_learning']}")
    
    # Validate advanced features
    assert config['advanced_dqn']['double_dqn'] == True, "Double DQN harus True"
    assert config['advanced_dqn']['dueling_dqn'] == True, "Dueling DQN harus True"
    assert config['advanced_dqn']['prioritized_replay'] == True, "Prioritized Replay harus True"
    
    print("✅ Semua advanced features aktif!")

def test_reward_function():
    """Test reward function configuration"""
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    print("\n🎯 Reward Function Configuration Test:")
    print(f"✅ Distance Penalty Weight: {config['reward_function']['distance_penalty_weight']}")
    print(f"✅ Time Efficiency Weight: {config['reward_function']['time_efficiency_weight']}")
    print(f"✅ Utilization Bonus Weight: {config['reward_function']['utilization_bonus_weight']}")
    print(f"✅ Completion Bonus Weight: {config['reward_function']['completion_bonus_weight']}")
    print(f"✅ Efficiency Threshold: {config['reward_function']['efficiency_threshold']}")
    print(f"✅ Time Window Bonus: {config['reward_function']['time_window_bonus']}")
    
    # Validate reward weights
    total_weight = (config['reward_function']['distance_penalty_weight'] +
                   config['reward_function']['time_efficiency_weight'] +
                   config['reward_function']['utilization_bonus_weight'] +
                   config['reward_function']['completion_bonus_weight'])
    
    assert abs(total_weight - 1.0) < 0.01, "Total reward weights harus 1.0"
    print("✅ Reward function weights valid!")

def test_environment_config():
    """Test environment configuration"""
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    print("\n🌍 Environment Configuration Test:")
    print(f"✅ Max Capacity: {config['environment']['max_capacity']} kg")
    print(f"✅ Time Window: {config['environment']['time_window']} hours")
    print(f"✅ Depot Location: {config['environment']['depot_location']}")
    
    # Validate environment parameters
    assert config['environment']['max_capacity'] == 6000, "Max capacity harus 6000"
    assert config['environment']['time_window'] == 24, "Time window harus 24"
    
    print("✅ Environment configuration optimal!")

if __name__ == "__main__":
    print("🚀 Quick Test Model DQN VRP Advanced Optimal")
    print("=" * 60)
    
    # Test advanced model configuration
    total_params = test_advanced_model()
    
    # Test advanced hyperparameters
    test_advanced_hyperparameters()
    
    # Test advanced features
    test_advanced_features()
    
    # Test reward function
    test_reward_function()
    
    # Test environment
    test_environment_config()
    
    print("\n🎉 Model DQN VRP Advanced Optimal siap untuk training!")
    print(f"📊 Model complexity: {total_params:,} parameters")
    print("💡 Advanced features: Double DQN, Dueling DQN, Prioritized Replay")
    print("💡 Anda bisa lanjut ke proses training sekarang.")
    print("\n📋 Next Steps:")
    print("1. Run advanced training script")
    print("2. Monitor training progress with advanced features")
    print("3. Analyze advanced results")
    print("4. Update BAB IV with advanced model") 