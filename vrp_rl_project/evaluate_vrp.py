import os
import argparse
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from utils import load_config, calculate_distance
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent


def _nearest_neighbor_baseline(customers_df: pd.DataFrame) -> Tuple[float, float]:
    """
    Compute a simple nearest-neighbor baseline distance and time starting from index 0 (depot).

    Returns:
        total_distance_km, total_time_hours
    """
    if len(customers_df) <= 1:
        return 0.0, 0.0

    unvisited = set(range(1, len(customers_df)))
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


def evaluate_agent(
    customers_df: pd.DataFrame,
    config: Dict,
    episodes: int = 50,
    checkpoint_path: str = "model/dqn_final.weights.h5",
) -> Dict:
    """
    Run greedy evaluation and compute requested metrics.
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

    # Force greedy for evaluation
    agent.epsilon = 0.0

    baseline_distance_km, baseline_time_h = _nearest_neighbor_baseline(customers_df)

    total_rewards: List[float] = []
    total_distances: List[float] = []
    total_times: List[float] = []
    completion_rates: List[float] = []
    capacity_violations = 0
    time_window_violations = 0
    utilizations: List[float] = []

    for _ in range(episodes):
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
    }

    # Save per-episode raw metrics for traceability
    per_episode = pd.DataFrame({
        'reward': total_rewards,
        'distance_km': total_distances,
        'time_hours': total_times,
        'completion_rate_percent': completion_rates,
        'utilization_percent': utilizations,
    })
    os.makedirs('data', exist_ok=True)
    per_episode.to_csv('data/evaluation_episodes.csv', index=False)
    pd.DataFrame([results]).to_csv('data/evaluation_summary.csv', index=False)

    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate DQN VRP agent")
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Path to CSV dataset (e.g., data/prepared_shipments.csv)",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=50,
        help="Number of evaluation episodes",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="model/dqn_final.weights.h5",
        help="Path to model weights checkpoint",
    )
    args = parser.parse_args()

    # Resolve data path priority: CLI > prepared_shipments.csv > simulated_shipments.csv
    if args.data_path is not None:
        data_path = args.data_path
    else:
        default_prepared = os.path.join("data", "prepared_shipments.csv")
        default_simulated = os.path.join("data", "simulated_shipments.csv")
        if os.path.exists(default_prepared):
            data_path = default_prepared
        else:
            data_path = default_simulated

    config = load_config()
    customers_df = pd.read_csv(data_path)
    results = evaluate_agent(
        customers_df,
        config,
        episodes=args.episodes,
        checkpoint_path=args.checkpoint,
    )

    print("\nEvaluation Summary (greedy):")
    print(f"- data_path: {data_path}")
    print(f"- checkpoint: {args.checkpoint}")
    for k, v in results.items():
        print(f"- {k}: {v}")


if __name__ == '__main__':
    main()

