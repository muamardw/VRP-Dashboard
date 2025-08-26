#!/usr/bin/env python3
"""
Compute per-episode Mean Squared Error (MSE) for saved DQN checkpoints.

This script loads the DQN agent and environment per project config, builds a fixed
validation set of transitions, and evaluates TD-target MSE for checkpoints:
episodes [0,100,200,300,400,500,600,700,800,900] and final (1000 if available).

Output: prints a compact table and writes CSV to data/mse_checkpoints.csv
"""

import os
import numpy as np
import pandas as pd

from typing import List, Tuple

from utils import load_config
from env.vrp_env import VRPDynamicEnv
from model.dqn_model import DQNAgent


def build_env_and_agent() -> Tuple[VRPDynamicEnv, DQNAgent, dict]:
    config = load_config()

    # Load customers data (use simulated if available)
    data_path = os.path.join('data', 'simulated_shipments.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Validation data not found: {data_path}. Run data generation first.")

    customers_df = pd.read_csv(data_path)

    env = VRPDynamicEnv(customers_df, config['environment']['max_vehicles'])
    agent = DQNAgent(
        state_size=env.observation_space.shape[0],
        action_size=env.action_space.n,
        config=config,
    )

    return env, agent, config


def collect_validation_transitions(env: VRPDynamicEnv, num_episodes: int = 5, max_steps: int = 150, seed: int = 42):
    rng = np.random.default_rng(seed)
    transitions: List[Tuple[np.ndarray, int, float, np.ndarray, bool]] = []

    for _ in range(num_episodes):
        state = env.reset()
        for _ in range(max_steps):
            # valid actions = unvisited customers
            valid_actions = [i for i in range(env.n_customers) if i not in env.visited_customers]
            if not valid_actions:
                break
            action = int(rng.choice(valid_actions))
            next_state, reward, done, _info = env.step(action)
            transitions.append((state.astype(np.float32), action, float(reward), next_state.astype(np.float32), bool(done)))
            state = next_state
            if done:
                break
    return transitions


def compute_td_mse(agent: DQNAgent, transitions: List[Tuple[np.ndarray, int, float, np.ndarray, bool]], gamma: float) -> float:
    if not transitions:
        return float('nan')

    states = np.stack([t[0] for t in transitions], axis=0)
    actions = np.array([t[1] for t in transitions], dtype=np.int64)
    rewards = np.array([t[2] for t in transitions], dtype=np.float32)
    next_states = np.stack([t[3] for t in transitions], axis=0)
    dones = np.array([t[4] for t in transitions], dtype=bool)

    # Predict Q(s,·) and Q_target(s',·)
    q_states = agent.model.predict(states, verbose=0)
    # Use target network as in training; keep it synced with current weights for evaluation
    agent.update_target_model()
    q_next = agent.target_model.predict(next_states, verbose=0)

    q_pred_taken = q_states[np.arange(len(actions)), actions]
    max_q_next = np.max(q_next, axis=1)
    targets = np.where(dones, rewards, rewards + gamma * max_q_next)

    mse = float(np.mean((targets - q_pred_taken) ** 2))
    return mse


def main():
    env, agent, config = build_env_and_agent()
    transitions = collect_validation_transitions(env, num_episodes=8, max_steps=config['training']['max_steps'])

    # Checkpoints to evaluate
    ckpt_dir = os.path.join('model', 'checkpoints')
    episodes = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]

    rows = []

    for ep in episodes:
        ckpt_path = os.path.join(ckpt_dir, f'dqn_episode_{ep}.weights.h5')
        if not os.path.exists(ckpt_path):
            continue
        agent.load(ckpt_path)
        mse = compute_td_mse(agent, transitions, gamma=config['model']['gamma'])
        rows.append({'episode': ep, 'mse': mse})

    # Evaluate final model if present (label as episode 1000)
    final_path = os.path.join('model', 'dqn_final.weights.h5')
    if os.path.exists(final_path):
        agent.load(final_path)
        mse = compute_td_mse(agent, transitions, gamma=config['model']['gamma'])
        rows.append({'episode': 1000, 'mse': mse})

    # Save and print
    df = pd.DataFrame(rows).sort_values('episode')
    out_path = os.path.join('data', 'mse_checkpoints.csv')
    df.to_csv(out_path, index=False)

    print('\nMSE per Checkpoint (TD target):')
    for _, r in df.iterrows():
        print(f"Episode {int(r['episode']):4d} | MSE: {r['mse']:.6f}")
    print(f"\nSaved to: {out_path}")


if __name__ == '__main__':
    main()

