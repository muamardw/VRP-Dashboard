#!/usr/bin/env python3
"""
Visualisasi Data Preprocessing untuk VRP
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_missing_values_visualization():
    """Visualisasi penanganan missing values"""
    
    # Data contoh
    original_data = [25, np.nan, 35, 45, np.nan, 30]
    cleaned_data = [25, 25, 35, 45, 45, 30]
    indices = list(range(len(original_data)))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Penanganan Missing Values dengan Forward Fill', fontsize=14, fontweight='bold')
    
    # Before cleaning
    ax1.bar(indices, original_data, color='red', alpha=0.7, label='Missing Values')
    ax1.set_title('Data Sebelum Cleaning', fontweight='bold')
    ax1.set_xlabel('Index Data')
    ax1.set_ylabel('Jarak (km)')
    ax1.set_ylim(0, 50)
    ax1.grid(True, alpha=0.3)
    
    # Add NaN labels
    for i, val in enumerate(original_data):
        if np.isnan(val):
            ax1.text(i, 5, 'NaN', ha='center', va='bottom', fontweight='bold', color='red')
    
    # After cleaning
    ax2.bar(indices, cleaned_data, color='green', alpha=0.7, label='Forward Fill')
    ax2.set_title('Data Setelah Forward Fill', fontweight='bold')
    ax2.set_xlabel('Index Data')
    ax2.set_ylabel('Jarak (km)')
    ax2.set_ylim(0, 50)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for i, val in enumerate(cleaned_data):
        ax2.text(i, val + 1, str(val), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('missing_values_handling.png', dpi=300, bbox_inches='tight')
    print("✅ Missing values visualization saved as 'missing_values_handling.png'")

def create_outlier_detection_visualization():
    """Visualisasi outlier detection dengan IQR method"""
    
    # Data contoh
    data = [25, 35, 45, 120, 30, 28, 32, 40, 38, 42]
    sorted_data = sorted(data)
    
    # Calculate IQR
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Identify outliers
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    clean_data = [x for x in data if x >= lower_bound and x <= upper_bound]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Outlier Detection menggunakan IQR Method', fontsize=14, fontweight='bold')
    
    # Box plot
    ax1.boxplot(data, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    ax1.set_title('Box Plot dengan Outlier', fontweight='bold')
    ax1.set_ylabel('Jarak (km)')
    ax1.grid(True, alpha=0.3)
    
    # Add IQR lines
    ax1.axhline(y=q1, color='red', linestyle='--', alpha=0.7, label=f'Q1 = {q1:.1f}')
    ax1.axhline(y=q3, color='red', linestyle='--', alpha=0.7, label=f'Q3 = {q3:.1f}')
    ax1.axhline(y=lower_bound, color='orange', linestyle=':', alpha=0.7, label=f'Lower Bound = {lower_bound:.1f}')
    ax1.axhline(y=upper_bound, color='orange', linestyle=':', alpha=0.7, label=f'Upper Bound = {upper_bound:.1f}')
    ax1.legend()
    
    # Histogram comparison
    ax2.hist(data, bins=10, alpha=0.7, color='red', label='Data dengan Outlier', density=True)
    ax2.hist(clean_data, bins=8, alpha=0.7, color='green', label='Data Bersih', density=True)
    ax2.set_title('Distribusi Data Sebelum dan Sesudah Cleaning', fontweight='bold')
    ax2.set_xlabel('Jarak (km)')
    ax2.set_ylabel('Density')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    ax2.text(0.02, 0.98, f'Outlier: {outliers}', transform=ax2.transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('outlier_detection.png', dpi=300, bbox_inches='tight')
    print("✅ Outlier detection visualization saved as 'outlier_detection.png'")

def create_normalization_visualization():
    """Visualisasi normalisasi data"""
    
    # Data koordinat
    cities = ['Jakarta', 'Bekasi', 'Bogor', 'Tangerang']
    latitudes = [-6.2088, -6.2383, -6.5950, -6.1783]
    longitudes = [106.8456, 106.9756, 106.8167, 106.6319]
    
    # Normalize coordinates
    min_lat, max_lat = -7.0, -6.0
    min_lon, max_lon = 106.0, 108.0
    
    norm_latitudes = [(lat - min_lat) / (max_lat - min_lat) for lat in latitudes]
    norm_longitudes = [(lon - min_lon) / (max_lon - min_lon) for lon in longitudes]
    
    # Temperature data for Z-score
    temperatures = [28, 30, 25, 32, 29, 31, 27, 33]
    temp_mean = np.mean(temperatures)
    temp_std = np.std(temperatures)
    z_scores = [(temp - temp_mean) / temp_std for temp in temperatures]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Normalisasi Data untuk VRP', fontsize=16, fontweight='bold')
    
    # Original coordinates
    ax1.scatter(longitudes, latitudes, c=range(len(cities)), cmap='viridis', s=100)
    for i, city in enumerate(cities):
        ax1.annotate(city, (longitudes[i], latitudes[i]), xytext=(5, 5), 
                    textcoords='offset points', fontweight='bold')
    ax1.set_title('Koordinat GPS Asli', fontweight='bold')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True, alpha=0.3)
    
    # Normalized coordinates
    ax2.scatter(norm_longitudes, norm_latitudes, c=range(len(cities)), cmap='viridis', s=100)
    for i, city in enumerate(cities):
        ax2.annotate(city, (norm_longitudes[i], norm_latitudes[i]), xytext=(5, 5), 
                    textcoords='offset points', fontweight='bold')
    ax2.set_title('Koordinat GPS Normalisasi (Min-Max)', fontweight='bold')
    ax2.set_xlabel('Normalized Longitude')
    ax2.set_ylabel('Normalized Latitude')
    ax2.grid(True, alpha=0.3)
    
    # Original temperature data
    ax3.hist(temperatures, bins=8, alpha=0.7, color='blue', edgecolor='black')
    ax3.axvline(temp_mean, color='red', linestyle='--', label=f'Mean = {temp_mean:.1f}')
    ax3.set_title('Distribusi Temperatur Asli', fontweight='bold')
    ax3.set_xlabel('Temperatur (°C)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Z-score normalized temperature
    ax4.hist(z_scores, bins=8, alpha=0.7, color='green', edgecolor='black')
    ax4.axvline(0, color='red', linestyle='--', label='Mean = 0')
    ax4.set_title('Distribusi Temperatur Z-Score', fontweight='bold')
    ax4.set_xlabel('Z-Score')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data_normalization.png', dpi=300, bbox_inches='tight')
    print("✅ Data normalization visualization saved as 'data_normalization.png'")

def create_preprocessing_summary():
    """Visualisasi ringkasan preprocessing"""
    
    # Data untuk summary
    steps = ['Raw Data', 'Missing Values\nHandling', 'Outlier\nDetection', 'Normalization', 'Final\nClean Data']
    data_quality = [60, 75, 85, 95, 100]  # Percentage
    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Ringkasan Data Preprocessing Pipeline', fontsize=16, fontweight='bold')
    
    # Pipeline steps
    bars = ax1.bar(steps, data_quality, color=colors, alpha=0.7)
    ax1.set_title('Data Quality Improvement', fontweight='bold')
    ax1.set_ylabel('Data Quality (%)')
    ax1.set_ylim(0, 110)
    
    # Add value labels
    for bar, value in zip(bars, data_quality):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}%', ha='center', va='bottom', fontweight='bold')
    
    # Processing time
    processing_times = [0, 2, 5, 3, 1]  # Minutes
    ax2.plot(steps, processing_times, 'o-', linewidth=2, markersize=8, color='blue')
    ax2.set_title('Processing Time per Step', fontweight='bold')
    ax2.set_ylabel('Time (minutes)')
    ax2.grid(True, alpha=0.3)
    
    # Add time labels
    for i, time in enumerate(processing_times):
        ax2.text(i, time + 0.2, f'{time} min', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('preprocessing_summary.png', dpi=300, bbox_inches='tight')
    print("✅ Preprocessing summary saved as 'preprocessing_summary.png'")

if __name__ == "__main__":
    print("🎨 Creating Data Preprocessing Visualizations...")
    
    # Create all visualizations
    create_missing_values_visualization()
    create_outlier_detection_visualization()
    create_normalization_visualization()
    create_preprocessing_summary()
    
    print("\n🎉 All preprocessing visualizations created successfully!")
    print("📊 Files generated:")
    print("  - missing_values_handling.png")
    print("  - outlier_detection.png")
    print("  - data_normalization.png")
    print("  - preprocessing_summary.png") 