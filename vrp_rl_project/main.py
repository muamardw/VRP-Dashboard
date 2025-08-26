import argparse
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_config, generate_simulated_data, save_results, plot_route
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent

def train_model(env: VRPDynamicEnv, agent: DQNAgent, config: Dict) -> Dict:
    """
    Train the DQN agent.
    
    Args:
        env: VRP environment
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
        'visited_customers': []
    }
    
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
        
        # Save model
        if episode % save_interval == 0:
            agent.save(f'model/checkpoints/dqn_episode_{episode}.weights.h5')
        
        # Print progress
        if episode % 10 == 0:
            print(f"Episode: {episode}")
            print(f"Total Reward: {total_reward}")
            print(f"Total Distance: {info.get('total_distance', 0):.2f}")
            print(f"Total Time: {info.get('total_time', 0):.2f}")
            print(f"Visited Customers: {info.get('visited_customers', 0)}")
            print("------------------------")
    
    return results

def evaluate_model(env: VRPDynamicEnv, agent: DQNAgent) -> Dict:
    """
    Evaluate the trained DQN agent.
    
    Args:
        env: VRP environment
        agent: DQN agent
        
    Returns:
        Dictionary containing evaluation results
    """
    state = env.reset()
    total_reward = 0
    route = []
    
    while True:
        # Get valid actions
        valid_actions = [i for i in range(env.n_customers) 
                        if i not in env.visited_customers]
        
        # Choose action
        action = agent.act(state, valid_actions)
        
        # Take action
        next_state, reward, done, info = env.step(action)
        
        # Update state and reward
        state = next_state
        total_reward += reward
        
        # Record route
        route.append((env.customers_df.iloc[action]['latitude'],
                     env.customers_df.iloc[action]['longitude']))
        
        if done:
            break
    
    return {
        'total_reward': total_reward,
        'total_distance': info.get('total_distance', 0),
        'total_time': info.get('total_time', 0),
        'visited_customers': info.get('visited_customers', 0),
        'route': route
    }

def plot_training_results(results: Dict):
    """
    Plot training results.
    
    Args:
        results: Dictionary containing training results
    """
    plt.figure(figsize=(15, 10))
    
    # Plot total reward
    plt.subplot(2, 2, 1)
    plt.plot(results['episode'], results['total_reward'])
    plt.title('Total Reward per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    
    # Plot total distance
    plt.subplot(2, 2, 2)
    plt.plot(results['episode'], results['total_distance'])
    plt.title('Total Distance per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Distance (km)')
    
    # Plot total time
    plt.subplot(2, 2, 3)
    plt.plot(results['episode'], results['total_time'])
    plt.title('Total Time per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Time (hours)')
    
    # Plot visited customers
    plt.subplot(2, 2, 4)
    plt.plot(results['episode'], results['visited_customers'])
    plt.title('Visited Customers per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Number of Customers')
    
    plt.tight_layout()
    plt.savefig('data/training_results.png')
    plt.close()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='VRP with RL')
    parser.add_argument('--generate-data', action='store_true',
                       help='Generate simulated data')
    parser.add_argument('--train', action='store_true',
                       help='Train the model')
    parser.add_argument('--evaluate', action='store_true',
                       help='Evaluate the model')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    if args.generate_data:
        # Generate simulated data
        customers_df = generate_simulated_data(
            n_customers=50,
            n_vehicles=config['environment']['max_vehicles'],
            max_capacity=config['environment']['max_capacity']
        )
        customers_df.to_csv('data/simulated_shipments.csv', index=False)
        print("Generated simulated data")
    
    if args.train:
        # Load data
        customers_df = pd.read_csv('data/simulated_shipments.csv')
        
        # Create environment and agent
        env = VRPDynamicEnv(customers_df, config['environment']['max_vehicles'])
        agent = DQNAgent(
            state_size=env.observation_space.shape[0],
            action_size=env.action_space.n,
            config=config
        )
        
        # Train model
        results = train_model(env, agent, config)
        
        # Save results
        save_results(results, 'training_results.csv')
        plot_training_results(results)
        
        # Save final model
        agent.save('model/dqn_final.weights.h5')
        print("Training completed")
    
    if args.evaluate:
        # Load data and model
        customers_df = pd.read_csv('data/simulated_shipments.csv')
        env = VRPDynamicEnv(customers_df, config['environment']['max_vehicles'])
        agent = DQNAgent(
            state_size=env.observation_space.shape[0],
            action_size=env.action_space.n,
            config=config
        )
        agent.load('model/checkpoints/dqn_episode_900.weights.h5')
        
        # Evaluate model
        results = evaluate_model(env, agent)
        
        # Plot route
        plot_route(results['route'], customers_df, "Optimal Route")
        
        print("\nEvaluation Results:")
        print(f"Total Reward: {results['total_reward']}")
        print(f"Total Distance: {results['total_distance']:.2f} km")
        print(f"Total Time: {results['total_time']:.2f} hours")
        print(f"Visited Customers: {results['visited_customers']}")

if __name__ == '__main__':
    main() 