#!/usr/bin/env python3
"""
Script untuk membuat tabel ringkasan training DQN VRP dengan data real.
Menampilkan episode optimal, reward, epsilon, exploration vs exploitation, convergence status, dan completion rate.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List

def analyze_training_progress(training_file: str = 'data/training_results_real.csv') -> pd.DataFrame:
    """
    Analyze training progress and create summary table.
    
    Args:
        training_file: Path to training results CSV file
        
    Returns:
        DataFrame with training summary
    """
    if not os.path.exists(training_file):
        print(f"❌ File {training_file} tidak ditemukan!")
        print("💡 Jalankan training terlebih dahulu: python train_real_data.py --train")
        return pd.DataFrame()
    
    # Load training data
    df = pd.read_csv(training_file)
    
    if len(df) == 0:
        print("❌ Training data kosong!")
        return pd.DataFrame()
    
    # Calculate moving average for reward stability
    window = 50
    df['reward_ma'] = df['total_reward'].rolling(window=window).mean()
    df['reward_std'] = df['total_reward'].rolling(window=window).std()
    
    # Find key episodes
    episodes_to_analyze = []
    
    # Episode 0 (start)
    episodes_to_analyze.append(0)
    
    # Episode 100 (early training)
    if len(df) > 100:
        episodes_to_analyze.append(100)
    
    # Episode 200 (mid training)
    if len(df) > 200:
        episodes_to_analyze.append(200)
    
    # Episode 300 (convergence check)
    if len(df) > 300:
        episodes_to_analyze.append(300)
    
    # Episode 500 (stable check)
    if len(df) > 500:
        episodes_to_analyze.append(500)
    
    # Episode 700 (late training)
    if len(df) > 700:
        episodes_to_analyze.append(700)
    
    # Episode 900 (near end)
    if len(df) > 900:
        episodes_to_analyze.append(900)
    
    # Final episode
    episodes_to_analyze.append(len(df) - 1)
    
    # Find optimal episode (highest moving average reward)
    if 'reward_ma' in df.columns:
        optimal_episode = df['reward_ma'].idxmax()
        if optimal_episode not in episodes_to_analyze:
            episodes_to_analyze.append(optimal_episode)
    
    # Find convergence episode (when reward stabilizes)
    convergence_episode = None
    if len(df) >= 100:
        last_100_std = df['reward_std'].tail(100).mean()
        last_100_mean = df['reward_ma'].tail(100).mean()
        
        if last_100_std < abs(last_100_mean * 0.05):  # 5% stability threshold
            convergence_episode = len(df) - 100
            if convergence_episode not in episodes_to_analyze:
                episodes_to_analyze.append(convergence_episode)
    
    # Sort episodes
    episodes_to_analyze = sorted(list(set(episodes_to_analyze)))
    
    # Create summary table
    summary_data = []
    
    for episode in episodes_to_analyze:
        if episode >= len(df):
            continue
            
        row = df.iloc[episode]
        
        # Determine exploration vs exploitation phase
        epsilon = row['epsilon']
        if epsilon > 0.1:
            phase = "Exploration"
        elif epsilon > 0.01:
            phase = "Mixed"
        else:
            phase = "Exploitation"
        
        # Determine convergence status
        if episode == 0:
            status = "Start"
        elif episode == optimal_episode:
            status = "Optimal"
        elif episode == convergence_episode:
            status = "Convergence"
        elif episode == len(df) - 1:
            status = "Final"
        else:
            status = "Training"
        
        # Calculate completion rate (assuming 4 destinations)
        visited = row['visited_customers']
        completion_rate = (visited / 4) * 100 if 'visited_customers' in row else 0
        
        summary_data.append({
            'Episode': episode,
            'Reward': round(row['total_reward'], 2),
            'Distance (km)': round(row['total_distance'], 2),
            'Time (jam)': round(row['total_time'], 2),
            'Epsilon': round(epsilon, 4),
            'Exploration vs Exploitation': phase,
            'Convergence Status': status,
            'Completion Rate (%)': round(completion_rate, 1),
            'Visited Customers': visited if 'visited_customers' in row else 0
        })
    
    return pd.DataFrame(summary_data)

def create_detailed_summary(training_file: str = 'data/training_results_real.csv') -> Dict:
    """
    Create detailed training summary statistics.
    
    Args:
        training_file: Path to training results CSV file
        
    Returns:
        Dictionary with detailed summary
    """
    if not os.path.exists(training_file):
        return {}
    
    df = pd.read_csv(training_file)
    
    if len(df) == 0:
        return {}
    
    # Calculate moving averages
    window = 50
    df['reward_ma'] = df['total_reward'].rolling(window=window).mean()
    df['reward_std'] = df['total_reward'].rolling(window=window).std()
    
    # Find optimal episode
    optimal_episode = df['reward_ma'].idxmax() if 'reward_ma' in df.columns else 0
    
    # Analyze exploration vs exploitation
    exploration_episodes = (df['epsilon'] > 0.1).sum()
    exploitation_episodes = (df['epsilon'] <= 0.1).sum()
    
    # Determine convergence
    convergence_episode = len(df)
    if len(df) >= 100:
        last_100_std = df['reward_std'].tail(100).mean()
        last_100_mean = df['reward_ma'].tail(100).mean()
        
        if last_100_std < abs(last_100_mean * 0.05):
            convergence_episode = len(df) - 100
    
    # Calculate completion rates
    if 'visited_customers' in df.columns:
        completion_rates = (df['visited_customers'] / 4) * 100
        avg_completion = completion_rates.mean()
        perfect_completion_episodes = (completion_rates == 100).sum()
    else:
        avg_completion = 0
        perfect_completion_episodes = 0
    
    return {
        'total_episodes': len(df),
        'optimal_episode': int(optimal_episode),
        'convergence_episode': int(convergence_episode),
        'exploration_episodes': int(exploration_episodes),
        'exploitation_episodes': int(exploitation_episodes),
        'final_epsilon': round(df['epsilon'].iloc[-1], 4),
        'best_reward': round(df['total_reward'].max(), 2),
        'avg_reward': round(df['total_reward'].mean(), 2),
        'best_distance': round(df['total_distance'].min(), 2),
        'avg_distance': round(df['total_distance'].mean(), 2),
        'avg_completion_rate': round(avg_completion, 1),
        'perfect_completion_episodes': int(perfect_completion_episodes),
        'reward_stability': round(df['reward_std'].tail(100).mean() if len(df) >= 100 else 0, 3)
    }

def main():
    """Main function to create training summary."""
    
    print("📊 Membuat Tabel Ringkasan Training DQN VRP")
    print("=" * 50)
    
    # Create episode summary table
    summary_df = analyze_training_progress()
    
    if len(summary_df) > 0:
        print("\n📋 Tabel Ringkasan Training:")
        print("=" * 80)
        print(summary_df.to_string(index=False))
        
        # Save to CSV
        output_file = 'data/training_summary_table.csv'
        summary_df.to_csv(output_file, index=False)
        print(f"\n💾 Tabel disimpan: {output_file}")
        
        # Create detailed summary
        detailed = create_detailed_summary()
        
        if detailed:
            print(f"\n📈 Ringkasan Detail Training:")
            print("=" * 40)
            print(f"Total Episodes: {detailed['total_episodes']}")
            print(f"Optimal Episode: {detailed['optimal_episode']}")
            print(f"Convergence Episode: {detailed['convergence_episode']}")
            print(f"Exploration Episodes: {detailed['exploration_episodes']}")
            print(f"Exploitation Episodes: {detailed['exploitation_episodes']}")
            print(f"Final Epsilon: {detailed['final_epsilon']}")
            print(f"Best Reward: {detailed['best_reward']}")
            print(f"Average Reward: {detailed['avg_reward']}")
            print(f"Best Distance: {detailed['best_distance']} km")
            print(f"Average Distance: {detailed['avg_distance']} km")
            print(f"Average Completion Rate: {detailed['avg_completion_rate']}%")
            print(f"Perfect Completion Episodes: {detailed['perfect_completion_episodes']}")
            print(f"Reward Stability: {detailed['reward_stability']}")
            
            # Save detailed summary
            detailed_df = pd.DataFrame([detailed])
            detailed_file = 'data/training_detailed_summary.csv'
            detailed_df.to_csv(detailed_file, index=False)
            print(f"\n💾 Detail summary disimpan: {detailed_file}")
    else:
        print("❌ Tidak ada data training yang ditemukan!")
        print("💡 Jalankan training terlebih dahulu: python train_real_data.py --train")

if __name__ == '__main__':
    main() 