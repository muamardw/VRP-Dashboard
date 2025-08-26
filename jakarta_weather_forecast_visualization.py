#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Forecast Visualization
Visualisasi data cuaca Jakarta dalam sehari dengan interval 3 jam
Berdasarkan data dari OpenWeatherMap API
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import requests
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Circle
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
sns.set_palette("husl")

class JakartaWeatherForecastVisualizer:
    def __init__(self, api_key="ec9a1e4e17acbc7681644f5b8f316236"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_jakarta_forecast(self):
        """Ambil data forecast Jakarta dari OpenWeatherMap API"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': 'Jakarta,ID',
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'id'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except Exception as e:
            print(f"Error mengambil data forecast Jakarta: {e}")
            return None
    
    def parse_forecast_data(self, forecast_data):
        """Parse data forecast menjadi format yang mudah divisualisasikan"""
        if not forecast_data or 'list' not in forecast_data:
            return None
        
        parsed_data = []
        
        for item in forecast_data['list']:
            # Parse timestamp
            dt = datetime.fromtimestamp(item['dt'])
            
            # Extract weather data
            weather_info = {
                'datetime': dt,
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind']['deg'],
                'clouds': item['clouds']['all'],
                'visibility': item.get('visibility', 10000),
                'weather_main': item['weather'][0]['main'],
                'weather_description': item['weather'][0]['description'],
                'pop': item.get('pop', 0),  # Probability of precipitation
                'rain_3h': item.get('rain', {}).get('3h', 0) if 'rain' in item else 0
            }
            
            parsed_data.append(weather_info)
        
        return parsed_data
    
    def create_daily_weather_dashboard(self, forecast_data):
        """Buat dashboard cuaca harian Jakarta"""
        if not forecast_data:
            print("❌ Tidak ada data forecast untuk divisualisasikan")
            return
        
        # Filter data untuk 24 jam pertama (8 data points dengan interval 3 jam)
        daily_data = forecast_data[:8]
        
        # Extract time labels
        time_labels = [data['datetime'].strftime('%H:%M') for data in daily_data]
        dates = [data['datetime'].strftime('%d/%m') for data in daily_data]
        
        # Create comprehensive dashboard
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('🌤️ Jakarta Weather Forecast - 24 Jam (Interval 3 Jam)', 
                    fontsize=24, fontweight='bold', y=0.98)
        
        # Create grid layout
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
        
        # 1. Temperature Chart (Main)
        ax1 = fig.add_subplot(gs[0, :2])
        temperatures = [data['temperature'] for data in daily_data]
        feels_like = [data['feels_like'] for data in daily_data]
        
        ax1.plot(time_labels, temperatures, 'o-', linewidth=3, markersize=8, 
                label='Temperature (°C)', color='#E74C3C')
        ax1.plot(time_labels, feels_like, 's-', linewidth=3, markersize=8, 
                label='Feels Like (°C)', color='#F39C12')
        
        ax1.set_title('🌡️ Temperature & Feels Like', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for i, (temp, feels) in enumerate(zip(temperatures, feels_like)):
            ax1.annotate(f'{temp:.1f}°C', (i, temp), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontweight='bold')
            ax1.annotate(f'{feels:.1f}°C', (i, feels), textcoords="offset points", 
                        xytext=(0,-15), ha='center', fontweight='bold', color='#F39C12')
        
        # 2. Weather Conditions Summary
        ax2 = fig.add_subplot(gs[0, 2])
        conditions = [data['weather_description'] for data in daily_data]
        condition_counts = {}
        for condition in conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        if condition_counts:
            colors = ['#3498DB', '#E74C3C', '#F39C12', '#2ECC71', '#9B59B6']
            wedges, texts, autotexts = ax2.pie(condition_counts.values(), 
                                              labels=condition_counts.keys(),
                                              autopct='%1.1f%%', 
                                              startangle=90,
                                              colors=colors[:len(condition_counts)])
            ax2.set_title('☁️ Weather Conditions', fontsize=14, fontweight='bold')
        
        # 3. Humidity & Pressure
        ax3 = fig.add_subplot(gs[1, 0])
        humidities = [data['humidity'] for data in daily_data]
        pressures = [data['pressure'] for data in daily_data]
        
        # Normalize pressure for better visualization
        pressure_norm = [(p - min(pressures)) / (max(pressures) - min(pressures)) * 100 
                        for p in pressures]
        
        ax3_twin = ax3.twinx()
        
        bars1 = ax3.bar(time_labels, humidities, alpha=0.7, color='#3498DB', label='Humidity')
        line1 = ax3_twin.plot(time_labels, pressure_norm, 'o-', color='#E67E22', 
                             linewidth=2, markersize=6, label='Pressure (normalized)')
        
        ax3.set_title('💧 Humidity & Pressure', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Humidity (%)', color='#3498DB')
        ax3_twin.set_ylabel('Pressure (normalized)', color='#E67E22')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, hum in zip(bars1, humidities):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{hum:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        # 4. Wind Speed & Direction
        ax4 = fig.add_subplot(gs[1, 1])
        wind_speeds = [data['wind_speed'] for data in daily_data]
        wind_dirs = [data['wind_deg'] for data in daily_data]
        
        bars2 = ax4.bar(time_labels, wind_speeds, alpha=0.7, color='#2ECC71')
        ax4.set_title('💨 Wind Speed', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Wind Speed (m/s)')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, speed in zip(bars2, wind_speeds):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{speed:.1f} m/s', ha='center', va='bottom', fontweight='bold')
        
        # 5. Cloud Cover & Visibility
        ax5 = fig.add_subplot(gs[1, 2])
        clouds = [data['clouds'] for data in daily_data]
        visibilities = [data['visibility']/1000 for data in daily_data]  # Convert to km
        
        ax5_twin = ax5.twinx()
        
        bars3 = ax5.bar(time_labels, clouds, alpha=0.7, color='#95A5A6', label='Cloud Cover')
        line2 = ax5_twin.plot(time_labels, visibilities, 'o-', color='#8E44AD', 
                             linewidth=2, markersize=6, label='Visibility')
        
        ax5.set_title('☁️ Cloud Cover & Visibility', fontsize=14, fontweight='bold')
        ax5.set_ylabel('Cloud Cover (%)', color='#95A5A6')
        ax5_twin.set_ylabel('Visibility (km)', color='#8E44AD')
        ax5.grid(True, alpha=0.3)
        ax5.tick_params(axis='x', rotation=45)
        
        # 6. Precipitation Probability & Rain
        ax6 = fig.add_subplot(gs[2, 0])
        pop = [data['pop'] * 100 for data in daily_data]  # Convert to percentage
        rain_3h = [data['rain_3h'] for data in daily_data]
        
        bars4 = ax6.bar(time_labels, pop, alpha=0.7, color='#3498DB', label='Precipitation Probability')
        ax6.set_title('🌧️ Precipitation Probability', fontsize=14, fontweight='bold')
        ax6.set_ylabel('Probability (%)')
        ax6.set_ylim(0, 100)
        ax6.grid(True, alpha=0.3)
        ax6.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, prob in zip(bars4, pop):
            height = bar.get_height()
            if height > 0:
                ax6.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{prob:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        # 7. Rain Amount (3h)
        ax7 = fig.add_subplot(gs[2, 1])
        bars5 = ax7.bar(time_labels, rain_3h, alpha=0.7, color='#2980B9')
        ax7.set_title('🌧️ Rain Amount (3h)', fontsize=14, fontweight='bold')
        ax7.set_ylabel('Rain (mm)')
        ax7.grid(True, alpha=0.3)
        ax7.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, rain in zip(bars5, rain_3h):
            height = bar.get_height()
            if height > 0:
                ax7.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{rain:.1f} mm', ha='center', va='bottom', fontweight='bold')
        
        # 8. Temperature Range (Min-Max)
        ax8 = fig.add_subplot(gs[2, 2])
        temp_mins = [data['temp_min'] for data in daily_data]
        temp_maxs = [data['temp_max'] for data in daily_data]
        
        x_pos = np.arange(len(time_labels))
        width = 0.35
        
        bars6a = ax8.bar(x_pos - width/2, temp_mins, width, alpha=0.7, 
                        color='#3498DB', label='Min Temp')
        bars6b = ax8.bar(x_pos + width/2, temp_maxs, width, alpha=0.7, 
                        color='#E74C3C', label='Max Temp')
        
        ax8.set_title('🌡️ Temperature Range', fontsize=14, fontweight='bold')
        ax8.set_ylabel('Temperature (°C)')
        ax8.set_xticks(x_pos)
        ax8.set_xticklabels(time_labels, rotation=45)
        ax8.legend()
        ax8.grid(True, alpha=0.3)
        
        # 9. Weather Impact Analysis
        ax9 = fig.add_subplot(gs[3, :])
        
        # Calculate weather impact factors
        weather_impact = {
            'clear': 1.0,
            'clouds': 1.1,
            'rain': 1.3,
            'heavy_rain': 1.5,
            'storm': 1.8,
            'fog': 1.2,
            'windy': 1.1
        }
        
        impact_factors = []
        for data in daily_data:
            condition = data['weather_main'].lower()
            factor = weather_impact.get(condition, 1.0)
            impact_factors.append(factor)
        
        # Create impact visualization
        bars7 = ax9.bar(time_labels, impact_factors, alpha=0.7, 
                       color=['#2ECC71' if f <= 1.1 else '#F39C12' if f <= 1.3 else '#E74C3C' 
                              for f in impact_factors])
        
        ax9.set_title('⚡ Weather Impact Factor pada Traffic', fontsize=16, fontweight='bold')
        ax9.set_ylabel('Impact Factor')
        ax9.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Normal (1.0)')
        ax9.grid(True, alpha=0.3)
        ax9.legend()
        ax9.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, factor in zip(bars7, impact_factors):
            height = bar.get_height()
            ax9.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{factor:.2f}x', ha='center', va='bottom', fontweight='bold')
        
        # Add date information
        fig.text(0.5, 0.02, f'📅 Date: {dates[0]} - {dates[-1]} | Data Source: OpenWeatherMap API', 
                ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        plt.savefig('jakarta_weather_forecast_24h.png', dpi=300, bbox_inches='tight')
        print("✅ Jakarta weather forecast visualization saved as 'jakarta_weather_forecast_24h.png'")
        plt.show()
        
        return daily_data
    
    def create_weather_variables_summary(self, forecast_data):
        """Ringkasan semua variabel cuaca yang mempengaruhi"""
        if not forecast_data:
            return
        
        # Create summary table
        summary_data = []
        for data in forecast_data:
            summary_data.append({
                'Time': data['datetime'].strftime('%H:%M'),
                'Temperature (°C)': f"{data['temperature']:.1f}",
                'Feels Like (°C)': f"{data['feels_like']:.1f}",
                'Humidity (%)': f"{data['humidity']:.0f}",
                'Pressure (hPa)': f"{data['pressure']:.0f}",
                'Wind Speed (m/s)': f"{data['wind_speed']:.1f}",
                'Wind Direction (°)': f"{data['wind_deg']:.0f}",
                'Cloud Cover (%)': f"{data['clouds']:.0f}",
                'Visibility (km)': f"{data['visibility']/1000:.1f}",
                'Precipitation (%)': f"{data['pop']*100:.0f}",
                'Rain (3h mm)': f"{data['rain_3h']:.1f}",
                'Weather': data['weather_description'],
                'Impact Factor': f"{self.get_weather_impact_factor(data['weather_main']):.2f}x"
            })
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(summary_data)
        df.to_csv('jakarta_weather_forecast_summary.csv', index=False)
        print("✅ Weather summary saved as 'jakarta_weather_forecast_summary.csv'")
        
        # Display summary
        print("\n📊 JAKARTA WEATHER FORECAST SUMMARY (24 Jam)")
        print("="*80)
        print(df.to_string(index=False))
        
        return df
    
    def get_weather_impact_factor(self, weather_main):
        """Hitung weather impact factor"""
        weather_impact = {
            'clear': 1.0,
            'clouds': 1.1,
            'rain': 1.3,
            'heavy_rain': 1.5,
            'storm': 1.8,
            'fog': 1.2,
            'windy': 1.1
        }
        return weather_impact.get(weather_main.lower(), 1.0)

def main():
    """Main function untuk menjalankan visualisasi forecast Jakarta"""
    print("🌤️ Jakarta Weather Forecast Visualization")
    print("="*60)
    
    # Initialize visualizer
    visualizer = JakartaWeatherForecastVisualizer()
    
    # Get forecast data
    print("\n📡 Fetching Jakarta weather forecast data...")
    forecast_data = visualizer.get_jakarta_forecast()
    
    if not forecast_data:
        print("❌ Failed to fetch forecast data")
        return
    
    # Parse data
    print("🔍 Parsing forecast data...")
    parsed_data = visualizer.parse_forecast_data(forecast_data)
    
    if not parsed_data:
        print("❌ Failed to parse forecast data")
        return
    
    # Create visualizations
    print("\n📊 Creating weather dashboard...")
    daily_data = visualizer.create_daily_weather_dashboard(parsed_data)
    
    # Create summary
    print("\n📋 Creating weather summary...")
    summary_df = visualizer.create_weather_variables_summary(daily_data)
    
    print("\n🎉 Jakarta weather forecast visualization completed!")
    print("📁 Generated files:")
    print("  - jakarta_weather_forecast_24h.png")
    print("  - jakarta_weather_forecast_summary.csv")

if __name__ == "__main__":
    main() 