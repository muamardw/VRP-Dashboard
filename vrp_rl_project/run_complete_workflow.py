#!/usr/bin/env python3
"""
Script untuk menjalankan workflow lengkap DQN VRP dengan data real PT. Sanghiang Perkasa.
Otomatis menjalankan: create dataset → training → evaluation → summary table
"""

import os
import subprocess
import sys
import time

def run_command(command: str, description: str) -> bool:
    """
    Run a command and handle errors.
    
    Args:
        command: Command to run
        description: Description of what the command does
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n🚀 {description}")
    print(f"📝 Command: {command}")
    print("=" * 60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Berhasil!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_file_exists(filepath: str, description: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        filepath: Path to file
        description: Description of the file
        
    Returns:
        True if file exists, False otherwise
    """
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} tidak ditemukan: {filepath}")
        return False

def main():
    """Main function to run complete workflow."""
    
    print("🚚 WORKFLOW LENGKAP DQN VRP - DATA REAL PT. SANGHIANG PERKASA")
    print("=" * 70)
    print("Workflow ini akan menjalankan:")
    print("1. 📊 Buat dataset real dari data perusahaan")
    print("2. 🎯 Training DQN dengan data real")
    print("3. 🔍 Evaluasi model dengan metrik lengkap")
    print("4. 📋 Buat tabel ringkasan training")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists('config.yaml'):
        print("❌ File config.yaml tidak ditemukan!")
        print("💡 Pastikan Anda berada di direktori vrp_rl_project")
        return
    
    # Step 1: Create real dataset
    print("\n" + "="*70)
    print("STEP 1: MEMBUAT DATASET REAL")
    print("="*70)
    
    if not run_command("python create_real_dataset.py", "Membuat dataset real dari data PT. Sanghiang Perkasa"):
        print("❌ Gagal membuat dataset real!")
        return
    
    if not check_file_exists("data/real_shipments.csv", "Dataset real"):
        print("❌ Dataset real tidak berhasil dibuat!")
        return
    
    # Step 2: Training
    print("\n" + "="*70)
    print("STEP 2: TRAINING DQN DENGAN DATA REAL")
    print("="*70)
    
    # Ask user for training episodes
    try:
        episodes = input("Masukkan jumlah episode training (default: 1000): ").strip()
        if not episodes:
            episodes = "1000"
        episodes = int(episodes)
    except ValueError:
        episodes = 1000
    
    training_command = f"python train_real_data.py --train --episodes {episodes}"
    
    if not run_command(training_command, f"Training DQN dengan {episodes} episode"):
        print("❌ Gagal melakukan training!")
        return
    
    if not check_file_exists("model/dqn_real_final.weights.h5", "Model trained"):
        print("❌ Model tidak berhasil disimpan!")
        return
    
    if not check_file_exists("data/training_results_real.csv", "Hasil training"):
        print("❌ Hasil training tidak berhasil disimpan!")
        return
    
    # Step 3: Evaluation
    print("\n" + "="*70)
    print("STEP 3: EVALUASI MODEL")
    print("="*70)
    
    if not run_command("python evaluate_real_data.py", "Evaluasi model dengan metrik lengkap"):
        print("❌ Gagal melakukan evaluasi!")
        return
    
    if not check_file_exists("data/evaluation_real_summary.csv", "Hasil evaluasi"):
        print("❌ Hasil evaluasi tidak berhasil disimpan!")
        return
    
    # Step 4: Training Summary Table
    print("\n" + "="*70)
    print("STEP 4: TABEL RINGKASAN TRAINING")
    print("="*70)
    
    if not run_command("python create_training_summary.py", "Membuat tabel ringkasan training"):
        print("❌ Gagal membuat tabel ringkasan!")
        return
    
    if not check_file_exists("data/training_summary_table.csv", "Tabel ringkasan"):
        print("❌ Tabel ringkasan tidak berhasil dibuat!")
        return
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 WORKFLOW LENGKAP SELESAI!")
    print("="*70)
    
    print("\n📁 File yang dihasilkan:")
    check_file_exists("data/real_shipments.csv", "Dataset real")
    check_file_exists("model/dqn_real_final.weights.h5", "Model trained")
    check_file_exists("data/training_results_real.csv", "Hasil training")
    check_file_exists("data/training_results_real.png", "Grafik training")
    check_file_exists("data/evaluation_real_summary.csv", "Ringkasan evaluasi")
    check_file_exists("data/evaluation_real_episodes.csv", "Data evaluasi per episode")
    check_file_exists("data/training_summary_table.csv", "Tabel ringkasan training")
    check_file_exists("data/training_detailed_summary.csv", "Ringkasan detail training")
    
    print(f"\n📊 Metrik Evaluasi yang Dihitung:")
    print(f"   ✅ Total distance (km), total time (jam)")
    print(f"   ✅ Completion rate (%), jumlah pelanggaran kapasitas/time window")
    print(f"   ✅ Capacity utilization (%), route efficiency (%), distance optimization (% vs baseline)")
    print(f"   ✅ Average return/reward pada evaluasi")
    print(f"   ✅ Episode optimal, epsilon, exploration vs exploitation")
    print(f"   ✅ Convergence status, completion rate")
    
    print(f"\n🎯 Langkah Selanjutnya:")
    print(f"   1. Analisis hasil di file CSV yang dihasilkan")
    print(f"   2. Bandingkan dengan baseline nearest-neighbor")
    print(f"   3. Implementasi di sistem operasional perusahaan")
    print(f"   4. Monitoring performa di lapangan")
    
    print(f"\n💡 Tips:")
    print(f"   • File training_results_real.png menampilkan grafik training")
    print(f"   • File training_summary_table.csv berisi tabel episode optimal")
    print(f"   • File evaluation_real_summary.csv berisi metrik evaluasi lengkap")
    print(f"   • Model siap digunakan untuk optimasi rute PT. Sanghiang Perkasa")

if __name__ == '__main__':
    main() 