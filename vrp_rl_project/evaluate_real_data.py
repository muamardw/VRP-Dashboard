#!/usr/bin/env python3
"""
Script evaluasi DQN VRP menggunakan data real PT. Sanghiang Perkasa (4 destinasi).
Menghitung metrik evaluasi yang diminta: distance, time, completion rate, violations, utilization, efficiency.
"""

import os
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from utils import load_config, calculate_distance
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent


def _nearest_neighbor_baseline_real(customers_df: pd.DataFrame) -> Tuple[float, float]:
    """
    Compute nearest-neighbor baseline untuk data real (4 destinasi).
    
    Returns:
        total_distance_km, total_time_hours
    """
    if len(customers_df) <= 1:
        return 0.0, 0.0

    unvisited = set(range(1, len(customers_df)))  # Skip depot (index 0)
    current = 0
    total_distance = 0.0
    total_time = 0.0
    base_speed_kmh = 50.0  # same as used in the env

    while unvisited:
        curr_lat = customers_df.iloc[current]['latitude']
        curr_lon = customers_df.iloc[current]['longitude']

        # pick nearest by Haversine distance
        nearest = None
        nearest_dist = float('inf')
        for j in list(unvisited):
            dist = calculate_distance(
                curr_lat,
                curr_lon,
                customers_df.iloc[j]['latitude'],
                customers_df.iloc[j]['longitude'],
            )
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = j

        # move to nearest
        assert nearest is not None
        total_distance += nearest_dist
        service_time = float(customers_df.iloc[nearest]['service_time'])
        travel_time = nearest_dist / base_speed_kmh
        total_time += travel_time + service_time
        current = nearest
        unvisited.remove(nearest)

    return total_distance, total_time


def analyze_convergence(rewards: List[float], epsilons: List[float], window: int = 50) -> Dict:
    """
    Analyze convergence status based on reward stability and epsilon decay.
    
    Args:
        rewards: List of rewards per episode
        epsilons: List of epsilon values per episode
        window: Window size for moving average calculation
    
    Returns:
        Dictionary with convergence analysis
    """
    if len(rewards) < window:
        return {
            'convergence_status': 'Insufficient Data',
            'optimal_episode': 0,
            'convergence_episode': 0,
            'exploration_phase': 'Unknown',
            'exploitation_phase': 'Unknown'
        }
    
    # Calculate moving average of rewards
    rewards_series = pd.Series(rewards)
    moving_avg = rewards_series.rolling(window=window).mean()
    
    # Find optimal episode (highest moving average)
    optimal_episode = moving_avg.idxmax() + 1  # +1 because episode starts from 0
    
    # Find convergence episode (when reward stabilizes)
    # Consider converged when moving average doesn't change more than 5% for last 100 episodes
    if len(moving_avg) >= 100:
        last_100_avg = moving_avg.tail(100)
        mean_last_100 = last_100_avg.mean()
        std_last_100 = last_100_avg.std()
        
        # If standard deviation is less than 5% of mean, consider converged
        if std_last_100 < abs(mean_last_100 * 0.05):
            convergence_episode = len(rewards) - 100
        else:
            convergence_episode = len(rewards)  # Not converged yet
    else:
        convergence_episode = len(rewards)
    
    # Analyze exploration vs exploitation phases
    epsilon_series = pd.Series(epsilons)
    
    # Exploration phase: epsilon > 0.1
    exploration_episodes = (epsilon_series > 0.1).sum()
    
    # Exploitation phase: epsilon <= 0.1
    exploitation_episodes = (epsilon_series <= 0.1).sum()
    
    # Determine current phase
    current_epsilon = epsilons[-1] if epsilons else 1.0
    if current_epsilon > 0.1:
        current_phase = "Exploration"
    elif current_epsilon > 0.01:
        current_phase = "Mixed"
    else:
        current_phase = "Exploitation"
    
    # Determine convergence status
    if convergence_episode < len(rewards):
        convergence_status = "Converged"
    elif len(rewards) >= 500:  # If trained for many episodes but not converged
        convergence_status = "Stable but not converged"
    else:
        convergence_status = "Training"
    
    return {
        'convergence_status': convergence_status,
        'optimal_episode': int(optimal_episode),
        'convergence_episode': int(convergence_episode),
        'exploration_episodes': int(exploration_episodes),
        'exploitation_episodes': int(exploitation_episodes),
        'current_phase': current_phase,
        'final_epsilon': round(current_epsilon, 4),
        'reward_stability': round(std_last_100 if len(moving_avg) >= 100 else 0, 3)
    }


def evaluate_agent_real(
    customers_df: pd.DataFrame,
    config: Dict,
    episodes: int = 50,
    checkpoint_path: str = "model/dqn_real_final.weights.h5",
) -> Dict:
    """
    Run greedy evaluation untuk data real dan compute metrik yang diminta.
    """
    env = VRPDynamicEnv(customers_df)

    agent = DQNAgent(
        state_size=env.observation_space.shape[0],
        action_size=env.action_space.n,
        config=config,
    )

    # Load weights if available
    if os.path.exists(checkpoint_path):
        agent.load(checkpoint_path)
        print(f"✅ Loaded model: {checkpoint_path}")
    else:
        print(f"⚠️ Model {checkpoint_path} tidak ditemukan, menggunakan model random")

    # Force greedy for evaluation
    agent.epsilon = 0.0

    baseline_distance_km, baseline_time_h = _nearest_neighbor_baseline_real(customers_df)

    print(f"\n🚚 Evaluasi DQN VRP - Data Real PT. Sanghiang Perkasa")
    print(f"📊 Episodes: {episodes}")
    print(f"🎯 Destinasi: 4 (Bogor, Tangerang, Jakarta, Bekasi)")
    print(f"🏢 Depot: Pulo Gadung, Jakarta Timur")
    print(f"📏 Baseline NN Distance: {baseline_distance_km:.2f} km")
    print(f"⏱️ Baseline NN Time: {baseline_time_h:.2f} jam")
    print("=" * 60)

    total_rewards: List[float] = []
    total_distances: List[float] = []
    total_times: List[float] = []
    completion_rates: List[float] = []
    capacity_violations = 0
    time_window_violations = 0
    utilizations: List[float] = []

    for episode in range(episodes):
        state = env.reset()
        episode_reward = 0.0

        # Run until done
        while True:
            valid_actions = [i for i in range(env.n_customers) if i not in env.visited_customers]
            action = agent.act(state, valid_actions)
            next_state, reward, done, info = env.step(action)
            state = next_state
            episode_reward += reward
            if done:
                # Constraint violation counting
                err = info.get('error')
                if err:
                    if 'Capacity' in err or 'Capacity exceeded' in err:
                        capacity_violations += 1
                    if 'Time window' in err:
                        time_window_violations += 1
                break

        total_rewards.append(episode_reward)
        total_distances.append(info.get('total_distance', 0.0))
        total_times.append(info.get('total_time', 0.0))
        completion_rates.append(100.0 * info.get('visited_customers', 0) / float(env.n_customers))
        utilizations.append(
            100.0 * (env.max_capacity - env.remaining_capacity) / float(env.max_capacity)
            if env.max_capacity > 0
            else 0.0
        )

        # Print progress setiap 10 episode
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1:3d}/{episodes} | "
                  f"Distance: {info.get('total_distance', 0):6.2f} km | "
                  f"Time: {info.get('total_time', 0):5.2f} jam | "
                  f"Visited: {info.get('visited_customers', 0):2d}/4")

    # Aggregated metrics
    avg_reward = float(np.mean(total_rewards)) if total_rewards else 0.0
    avg_distance = float(np.mean(total_distances)) if total_distances else 0.0
    avg_time = float(np.mean(total_times)) if total_times else 0.0
    avg_completion = float(np.mean(completion_rates)) if completion_rates else 0.0
    avg_utilization = float(np.mean(utilizations)) if utilizations else 0.0

    # Route efficiency and distance optimization (vs nearest-neighbor baseline)
    route_efficiency_pct = (baseline_distance_km / avg_distance * 100.0) if avg_distance > 0 else 0.0
    distance_optimization_pct = (
        (baseline_distance_km - avg_distance) / baseline_distance_km * 100.0
        if baseline_distance_km > 0
        else 0.0
    )

    # Load training history for convergence analysis (if available)
    convergence_analysis = {
        'convergence_status': 'No Training Data',
        'optimal_episode': 0,
        'convergence_episode': 0,
        'exploration_episodes': 0,
        'exploitation_episodes': 0,
        'current_phase': 'Unknown',
        'final_epsilon': 0.0,
        'reward_stability': 0.0
    }
    
    # Try to load training results for convergence analysis
    training_file = 'data/training_results_real.csv'
    if os.path.exists(training_file):
        try:
            training_df = pd.read_csv(training_file)
            if 'total_reward' in training_df.columns and 'epsilon' in training_df.columns:
                convergence_analysis = analyze_convergence(
                    training_df['total_reward'].tolist(),
                    training_df['epsilon'].tolist()
                )
                print(f"📈 Convergence Analysis: {convergence_analysis['convergence_status']}")
        except Exception as e:
            print(f"⚠️ Could not analyze convergence: {e}")

    results = {
        'episodes': episodes,
        'average_reward': round(avg_reward, 3),
        'average_distance_km': round(avg_distance, 2),
        'average_time_hours': round(avg_time, 2),
        'average_completion_rate_percent': round(avg_completion, 1),
        'capacity_violations': int(capacity_violations),
        'time_window_violations': int(time_window_violations),
        'average_utilization_percent': round(avg_utilization, 1),
        'baseline_distance_km': round(baseline_distance_km, 2),
        'baseline_time_hours': round(baseline_time_h, 2),
        'route_efficiency_percent': round(route_efficiency_pct, 1),
        'distance_optimization_percent_vs_baseline': round(distance_optimization_pct, 1),
        # Convergence and exploration metrics
        'convergence_status': convergence_analysis['convergence_status'],
        'optimal_episode': convergence_analysis['optimal_episode'],
        'convergence_episode': convergence_analysis['convergence_episode'],
        'exploration_episodes': convergence_analysis['exploration_episodes'],
        'exploitation_episodes': convergence_analysis['exploitation_episodes'],
        'current_phase': convergence_analysis['current_phase'],
        'final_epsilon': convergence_analysis['final_epsilon'],
        'reward_stability': convergence_analysis['reward_stability']
    }

    # Save per-episode raw metrics for traceability
    per_episode = pd.DataFrame({
        'episode': range(1, episodes + 1),
        'reward': total_rewards,
        'distance_km': total_distances,
        'time_hours': total_times,
        'completion_rate_percent': completion_rates,
        'utilization_percent': utilizations,
    })
    os.makedirs('data', exist_ok=True)
    per_episode.to_csv('data/evaluation_real_episodes.csv', index=False)
    pd.DataFrame([results]).to_csv('data/evaluation_real_summary.csv', index=False)

    return results


def print_evaluation_summary(results: Dict):
    """Print ringkasan evaluasi dengan format yang rapi."""
    
    print(f"\n" + "="*60)
    print(f"�� HASIL EVALUASI DQN VRP - DATA REAL")
    print(f"="*60)
    
    print(f"\n🎯 METRIK UTAMA:")
    print(f"   • Total Distance: {results['average_distance_km']} km")
    print(f"   • Total Time: {results['average_time_hours']} jam")
    print(f"   • Completion Rate: {results['average_completion_rate_percent']}%")
    print(f"   • Average Reward: {results['average_reward']}")
    
    print(f"\n⚠️ PELANGGARAN KENDALA:")
    print(f"   • Capacity Violations: {results['capacity_violations']}")
    print(f"   • Time Window Violations: {results['time_window_violations']}")
    
    print(f"\n📈 EFISIENSI:")
    print(f"   • Capacity Utilization: {results['average_utilization_percent']}%")
    print(f"   • Route Efficiency: {results['route_efficiency_percent']}%")
    print(f"   • Distance Optimization vs Baseline: {results['distance_optimization_percent_vs_baseline']}%")
    
    print(f"\n📏 BASELINE COMPARISON:")
    print(f"   • Nearest Neighbor Distance: {results['baseline_distance_km']} km")
    print(f"   • Nearest Neighbor Time: {results['baseline_time_hours']} jam")
    
    print(f"\n🔄 CONVERGENCE & EXPLORATION:")
    print(f"   • Convergence Status: {results['convergence_status']}")
    print(f"   • Optimal Episode: {results['optimal_episode']}")
    print(f"   • Convergence Episode: {results['convergence_episode']}")
    print(f"   • Exploration Episodes: {results['exploration_episodes']}")
    print(f"   • Exploitation Episodes: {results['exploitation_episodes']}")
    print(f"   • Current Phase: {results['current_phase']}")
    print(f"   • Final Epsilon: {results['final_epsilon']}")
    print(f"   • Reward Stability: {results['reward_stability']}")
    
    print(f"\n💾 File Output:")
    print(f"   • data/evaluation_real_summary.csv")
    print(f"   • data/evaluation_real_episodes.csv")


def main():
    """Main function untuk evaluasi data real."""
    
    # Load configuration dan data
    config = load_config()
    
    # Check if real dataset exists
    if not os.path.exists('data/real_shipments.csv'):
        print("❌ File data/real_shipments.csv tidak ditemukan!")
        print("💡 Jalankan dulu: python create_real_dataset.py")
        return
    
    customers_df = pd.read_csv('data/real_shipments.csv')
    print(f"✅ Loaded data real: {len(customers_df)} baris (1 depot + 4 destinasi)")
    
    # Run evaluation
    results = evaluate_agent_real(customers_df, config, episodes=50)
    
    # Print summary
    print_evaluation_summary(results)


if __name__ == '__main__':
    main() 