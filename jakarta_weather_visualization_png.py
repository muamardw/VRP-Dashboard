#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Data Visualization - PNG Export
Visualisasi data cuaca Jakarta dari OpenWeatherMap API dengan export PNG
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi yang lebih menarik
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Data dari OpenWeatherMap API response
WEATHER_DATA = {
    "cod": "200",
    "message": 0,
    "cnt": 40,
    "list": [
        {
            "dt": 1755162000,
            "main": {
                "temp": 32.34,
                "feels_like": 35.79,
                "temp_min": 32.34,
                "temp_max": 32.94,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1006,
                "humidity": 53,
                "temp_kf": -0.6
            },
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "hujan sedang",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 51},
            "wind": {"speed": 2.96, "deg": 37, "gust": 3.17},
            "visibility": 9077,
            "pop": 1,
            "rain": {"3h": 4.29},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-14 09:00:00"
        },
        {
            "dt": 1755172800,
            "main": {
                "temp": 31.57,
                "feels_like": 38.18,
                "temp_min": 31.34,
                "temp_max": 31.57,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 67,
                "temp_kf": 0.23
            },
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "hujan sedang",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 65},
            "wind": {"speed": 2.33, "deg": 87, "gust": 3.74},
            "visibility": 6307,
            "pop": 1,
            "rain": {"3h": 4.75},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 12:00:00"
        },
        {
            "dt": 1755183600,
            "main": {
                "temp": 30.44,
                "feels_like": 37.44,
                "temp_min": 30.44,
                "temp_max": 30.44,
                "pressure": 1011,
                "sea_level": 1011,
                "grnd_level": 1008,
                "humidity": 80,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 93},
            "wind": {"speed": 0.84, "deg": 158, "gust": 1.75},
            "visibility": 10000,
            "pop": 1,
            "rain": {"3h": 2.13},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 15:00:00"
        },
        {
            "dt": 1755194400,
            "main": {
                "temp": 27.61,
                "feels_like": 31.41,
                "temp_min": 27.61,
                "temp_max": 27.61,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 82,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 98},
            "wind": {"speed": 1.34, "deg": 231, "gust": 2.29},
            "visibility": 10000,
            "pop": 1,
            "rain": {"3h": 0.54},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 18:00:00"
        },
        {
            "dt": 1755205200,
            "main": {
                "temp": 28.03,
                "feels_like": 32.82,
                "temp_min": 28.03,
                "temp_max": 28.03,
                "pressure": 1009,
                "sea_level": 1009,
                "grnd_level": 1006,
                "humidity": 84,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10n"
                }
            ],
            "clouds": {"all": 100},
            "wind": {"speed": 2.2, "deg": 223, "gust": 3.53},
            "visibility": 10000,
            "pop": 0.86,
            "rain": {"3h": 0.77},
            "sys": {"pod": "n"},
            "dt_txt": "2025-08-14 21:00:00"
        },
        {
            "dt": 1755216000,
            "main": {
                "temp": 28.47,
                "feels_like": 33.87,
                "temp_min": 28.47,
                "temp_max": 28.47,
                "pressure": 1010,
                "sea_level": 1010,
                "grnd_level": 1007,
                "humidity": 83,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 97},
            "wind": {"speed": 1.88, "deg": 195, "gust": 2.86},
            "visibility": 10000,
            "pop": 0.64,
            "rain": {"3h": 0.18},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 00:00:00"
        },
        {
            "dt": 1755226800,
            "main": {
                "temp": 28.79,
                "feels_like": 31.44,
                "temp_min": 28.79,
                "temp_max": 28.79,
                "pressure": 1011,
                "sea_level": 1011,
                "grnd_level": 1007,
                "humidity": 65,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "awan pecah",
                    "icon": "04d"
                }
            ],
            "clouds": {"all": 60},
            "wind": {"speed": 0.78, "deg": 199, "gust": 0.97},
            "visibility": 10000,
            "pop": 0,
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 03:00:00"
        },
        {
            "dt": 1755237600,
            "main": {
                "temp": 30.27,
                "feels_like": 33.35,
                "temp_min": 30.27,
                "temp_max": 30.27,
                "pressure": 1008,
                "sea_level": 1008,
                "grnd_level": 1005,
                "humidity": 60,
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "hujan rintik-rintik",
                    "icon": "10d"
                }
            ],
            "clouds": {"all": 69},
            "wind": {"speed": 2.8, "deg": 355, "gust": 1.82},
            "visibility": 10000,
            "pop": 0.26,
            "rain": {"3h": 0.21},
            "sys": {"pod": "d"},
            "dt_txt": "2025-08-15 06:00:00"
        }
    ],
    "city": {
        "id": 1642911,
        "name": "Jakarta",
        "coord": {"lat": -6.2146, "lon": 106.8451},
        "country": "ID",
        "population": 8540121,
        "timezone": 25200,
        "sunrise": 1755126025,
        "sunset": 1755168870
    }
}

class JakartaWeatherVisualizerPNG:
    def __init__(self):
        self.weather_impact = {
            'clear': 1.0,
            'clouds': 1.1,
            'rain': 1.3,
            'heavy_rain': 1.5,
            'storm': 1.8,
            'fog': 1.2,
            'windy': 1.1
        }
        self.colors = {
            'temperature': '#FF6B6B',
            'humidity': '#4ECDC4',
            'wind': '#45B7D1',
            'pressure': '#96CEB4',
            'clouds': '#FFEAA7',
            'rain': '#DDA0DD',
            'impact': '#FF8C42'
        }
    
    def parse_weather_data(self, data):
        """Parse data cuaca dari API response"""
        parsed_data = []
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            
            weather_info = {
                'datetime': dt,
                'time_str': dt.strftime('%H:%M'),
                'date_str': dt.strftime('%d/%m/%Y'),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind']['deg'],
                'wind_gust': item['wind'].get('gust', 0),
                'clouds': item['clouds']['all'],
                'visibility': item.get('visibility', 10000),
                'weather_main': item['weather'][0]['main'],
                'weather_description': item['weather'][0]['description'],
                'pop': item.get('pop', 0),
                'rain_3h': item.get('rain', {}).get('3h', 0) if 'rain' in item else 0
            }
            
            parsed_data.append(weather_info)
        
        return parsed_data
    
    def get_weather_impact_factor(self, weather_main):
        """Hitung weather impact factor"""
        return self.weather_impact.get(weather_main.lower(), 1.0)
    
    def create_comprehensive_dashboard(self, weather_data):
        """Buat dashboard komprehensif dengan semua grafik"""
        fig = plt.figure(figsize=(20, 24))
        fig.suptitle('🌤️ JAKARTA WEATHER FORECAST DASHBOARD\n24 Jam - Interval 3 Jam', 
                     fontsize=24, fontweight='bold', y=0.98)
        
        # Grid layout
        gs = fig.add_gridspec(6, 3, hspace=0.3, wspace=0.3)
        
        # 1. Temperature Chart
        ax1 = fig.add_subplot(gs[0, :2])
        self.create_temperature_chart(ax1, weather_data)
        
        # 2. Humidity Chart
        ax2 = fig.add_subplot(gs[0, 2])
        self.create_humidity_chart(ax2, weather_data)
        
        # 3. Wind Chart
        ax3 = fig.add_subplot(gs[1, :2])
        self.create_wind_chart(ax3, weather_data)
        
        # 4. Pressure Chart
        ax4 = fig.add_subplot(gs[1, 2])
        self.create_pressure_chart(ax4, weather_data)
        
        # 5. Clouds and Visibility
        ax5 = fig.add_subplot(gs[2, :2])
        self.create_clouds_visibility_chart(ax5, weather_data)
        
        # 6. Precipitation Chart
        ax6 = fig.add_subplot(gs[2, 2])
        self.create_precipitation_chart(ax6, weather_data)
        
        # 7. Weather Impact Factor
        ax7 = fig.add_subplot(gs[3, :])
        self.create_impact_factor_chart(ax7, weather_data)
        
        # 8. VRP Impact Analysis
        ax8 = fig.add_subplot(gs[4, :])
        self.create_vrp_impact_chart(ax8, weather_data)
        
        # 9. Summary Statistics
        ax9 = fig.add_subplot(gs[5, :])
        self.create_summary_statistics(ax9, weather_data)
        
        plt.tight_layout()
        plt.savefig('jakarta_weather_dashboard.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✅ Dashboard utama tersimpan sebagai 'jakarta_weather_dashboard.png'")
    
    def create_temperature_chart(self, ax, weather_data):
        """Grafik temperatur"""
        times = [data['datetime'] for data in weather_data]
        temps = [data['temperature'] for data in weather_data]
        feels = [data['feels_like'] for data in weather_data]
        
        ax.plot(times, temps, 'o-', color=self.colors['temperature'], linewidth=3, 
               markersize=8, label='Temperatur Aktual')
        ax.plot(times, feels, 's-', color='#FF8E53', linewidth=3, 
               markersize=8, label='Temperatur Terasa')
        
        ax.fill_between(times, temps, feels, alpha=0.3, color='#FFB6C1')
        
        ax.set_title('🌡️ TEMPERATUR JAKARTA', fontsize=16, fontweight='bold')
        ax.set_ylabel('Temperatur (°C)', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Add value labels
        for i, (temp, feel) in enumerate(zip(temps, feels)):
            ax.annotate(f'{temp:.1f}°C', (times[i], temp), 
                       textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
            ax.annotate(f'{feel:.1f}°C', (times[i], feel), 
                       textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8)
    
    def create_humidity_chart(self, ax, weather_data):
        """Grafik kelembaban"""
        times = [data['datetime'] for data in weather_data]
        humidity = [data['humidity'] for data in weather_data]
        
        bars = ax.bar(range(len(times)), humidity, color=self.colors['humidity'], alpha=0.7)
        
        # Add value labels on bars
        for i, (bar, h) in enumerate(zip(bars, humidity)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{h:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title('💧 KELEMBABAN', fontsize=14, fontweight='bold')
        ax.set_ylabel('Kelembaban (%)', fontsize=12)
        ax.set_xlabel('Periode', fontsize=12)
        ax.set_xticks(range(len(times)))
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
    
    def create_wind_chart(self, ax, weather_data):
        """Grafik angin"""
        times = [data['datetime'] for data in weather_data]
        wind_speed = [data['wind_speed'] for data in weather_data]
        wind_gust = [data['wind_gust'] for data in weather_data]
        
        x = range(len(times))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], wind_speed, width, 
                      label='Kecepatan Angin', color=self.colors['wind'], alpha=0.7)
        bars2 = ax.bar([i + width/2 for i in x], wind_gust, width, 
                      label='Angin Gust', color='#FF6B9D', alpha=0.7)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_title('💨 KECEPATAN ANGIN', fontsize=16, fontweight='bold')
        ax.set_ylabel('Kecepatan (m/s)', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
    
    def create_pressure_chart(self, ax, weather_data):
        """Grafik tekanan udara"""
        times = [data['datetime'] for data in weather_data]
        pressure = [data['pressure'] for data in weather_data]
        
        ax.plot(times, pressure, 'o-', color=self.colors['pressure'], linewidth=3, markersize=8)
        
        # Add value labels
        for i, p in enumerate(pressure):
            ax.annotate(f'{p:.0f}hPa', (times[i], p), 
                       textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
        
        ax.set_title('🌪️ TEKANAN UDARA', fontsize=14, fontweight='bold')
        ax.set_ylabel('Tekanan (hPa)', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def create_clouds_visibility_chart(self, ax, weather_data):
        """Grafik tutupan awan dan visibilitas"""
        times = [data['datetime'] for data in weather_data]
        clouds = [data['clouds'] for data in weather_data]
        visibility = [data['visibility']/1000 for data in weather_data]  # Convert to km
        
        # Create dual y-axis
        ax2 = ax.twinx()
        
        # Plot clouds
        bars = ax.bar(range(len(times)), clouds, color=self.colors['clouds'], alpha=0.6, label='Tutupan Awan')
        ax.set_ylabel('Tutupan Awan (%)', color=self.colors['clouds'], fontsize=12)
        ax.set_ylim(0, 100)
        
        # Plot visibility
        line = ax2.plot(range(len(times)), visibility, 'o-', color='#8B4513', 
                       linewidth=3, markersize=8, label='Visibilitas')
        ax2.set_ylabel('Visibilitas (km)', color='#8B4513', fontsize=12)
        ax2.set_ylim(0, 12)
        
        # Add value labels
        for i, (c, v) in enumerate(zip(clouds, visibility)):
            ax.text(i, c + 2, f'{c:.0f}%', ha='center', va='bottom', fontsize=8)
            ax2.text(i, v + 0.2, f'{v:.1f}km', ha='center', va='bottom', fontsize=8)
        
        ax.set_title('☁️ TUTUPAN AWAN & VISIBILITAS', fontsize=16, fontweight='bold')
        ax.set_xlabel('Waktu', fontsize=12)
        ax.set_xticks(range(len(times)))
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.grid(True, alpha=0.3)
        
        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
    
    def create_precipitation_chart(self, ax, weather_data):
        """Grafik presipitasi"""
        times = [data['datetime'] for data in weather_data]
        rain_3h = [data['rain_3h'] for data in weather_data]
        pop = [data['pop'] * 100 for data in weather_data]  # Convert to percentage
        
        x = range(len(times))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], rain_3h, width, 
                      label='Curah Hujan (3h)', color=self.colors['rain'], alpha=0.7)
        bars2 = ax.bar([i + width/2 for i in x], pop, width, 
                      label='Probabilitas Hujan', color='#87CEEB', alpha=0.7)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_title('🌧️ PRESIPITASI', fontsize=14, fontweight='bold')
        ax.set_ylabel('Nilai', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
    
    def create_impact_factor_chart(self, ax, weather_data):
        """Grafik weather impact factor"""
        times = [data['datetime'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        weather_descriptions = [data['weather_description'] for data in weather_data]
        
        bars = ax.bar(range(len(times)), impact_factors, color=self.colors['impact'], alpha=0.7)
        
        # Color bars based on impact level
        for i, (bar, impact) in enumerate(zip(bars, impact_factors)):
            if impact <= 1.1:
                bar.set_color('#90EE90')  # Light green for low impact
            elif impact <= 1.3:
                bar.set_color('#FFD700')  # Gold for medium impact
            else:
                bar.set_color('#FF6347')  # Tomato red for high impact
        
        # Add value labels and weather descriptions
        for i, (bar, impact, desc) in enumerate(zip(bars, impact_factors, weather_descriptions)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{impact:.2f}x\n{desc}', ha='center', va='bottom', fontsize=9)
        
        ax.set_title('⚡ WEATHER IMPACT FACTOR', fontsize=16, fontweight='bold')
        ax.set_ylabel('Impact Factor', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.set_xticks(range(len(times)))
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.grid(True, alpha=0.3)
        
        # Add horizontal lines for impact levels
        ax.axhline(y=1.1, color='green', linestyle='--', alpha=0.7, label='Dampak Rendah')
        ax.axhline(y=1.3, color='orange', linestyle='--', alpha=0.7, label='Dampak Sedang')
        ax.axhline(y=1.5, color='red', linestyle='--', alpha=0.7, label='Dampak Tinggi')
        ax.legend(fontsize=10)
    
    def create_vrp_impact_chart(self, ax, weather_data):
        """Grafik dampak pada VRP"""
        times = [data['datetime'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        
        # Calculate VRP impacts
        base_time = 30  # minutes
        affected_times = [base_time * impact for impact in impact_factors]
        time_increases = [affected_time - base_time for affected_time in affected_times]
        
        # Create stacked bar chart
        bars1 = ax.bar(range(len(times)), [base_time] * len(times), 
                      label='Waktu Normal', color='#90EE90', alpha=0.7)
        bars2 = ax.bar(range(len(times)), time_increases, bottom=[base_time] * len(times),
                      label='Penambahan Waktu', color='#FF6347', alpha=0.7)
        
        # Add value labels
        for i, (bar1, bar2, total) in enumerate(zip(bars1, bars2, affected_times)):
            ax.text(bar1.get_x() + bar1.get_width()/2., total + 1,
                   f'{total:.1f} menit', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_title('🚛 DAMPAK CUACA PADA SISTEM VRP', fontsize=16, fontweight='bold')
        ax.set_ylabel('Waktu Perjalanan (menit)', fontsize=12)
        ax.set_xlabel('Waktu', fontsize=12)
        ax.set_xticks(range(len(times)))
        ax.set_xticklabels([data['time_str'] for data in weather_data], rotation=45)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
    
    def create_summary_statistics(self, ax, weather_data):
        """Ringkasan statistik"""
        ax.axis('off')
        
        # Calculate statistics
        temps = [data['temperature'] for data in weather_data]
        humidity = [data['humidity'] for data in weather_data]
        wind_speed = [data['wind_speed'] for data in weather_data]
        pressure = [data['pressure'] for data in weather_data]
        clouds = [data['clouds'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        
        # Create summary text
        summary_text = f"""
🌤️ RINGKASAN CUACA JAKARTA (24 Jam)

📊 STATISTIK UTAMA:
• Temperatur: {np.mean(temps):.1f}°C (Min: {min(temps):.1f}°C, Max: {max(temps):.1f}°C)
• Kelembaban: {np.mean(humidity):.0f}% (Min: {min(humidity):.0f}%, Max: {max(humidity):.0f}%)
• Kecepatan Angin: {np.mean(wind_speed):.1f} m/s (Max: {max(wind_speed):.1f} m/s)
• Tekanan Udara: {np.mean(pressure):.0f} hPa (Range: {max(pressure) - min(pressure):.0f} hPa)
• Tutupan Awan: {np.mean(clouds):.0f}% (Tertinggi: {max(clouds):.0f}%)

⚡ DAMPAK PADA VRP:
• Weather Impact Factor Rata-rata: {np.mean(impact_factors):.2f}x
• Periode Dampak Rendah (≤1.1x): {sum(1 for i in impact_factors if i <= 1.1)} periode
• Periode Dampak Sedang (1.1-1.3x): {sum(1 for i in impact_factors if 1.1 < i <= 1.3)} periode
• Periode Dampak Tinggi (>1.3x): {sum(1 for i in impact_factors if i > 1.3)} periode

🚛 REKOMENDASI RUTE:
• Rute Normal: {sum(1 for i in impact_factors if i <= 1.1)} periode
• Rute Alternatif: {sum(1 for i in impact_factors if i > 1.1)} periode
• Penambahan Waktu Rata-rata: {(np.mean(impact_factors) - 1) * 30:.1f} menit

🌧️ KONDISI CUACA:
• Hujan: {sum(1 for data in weather_data if 'rain' in data['weather_main'].lower())} periode
• Berawan: {sum(1 for data in weather_data if 'clouds' in data['weather_main'].lower())} periode
• Total Curah Hujan: {sum(data['rain_3h'] for data in weather_data):.1f} mm
        """
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    def create_individual_charts(self, weather_data):
        """Buat grafik individual untuk setiap variabel"""
        # Temperature chart
        fig, ax = plt.subplots(figsize=(12, 8))
        self.create_temperature_chart(ax, weather_data)
        plt.tight_layout()
        plt.savefig('jakarta_temperature.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        # Humidity chart
        fig, ax = plt.subplots(figsize=(10, 6))
        self.create_humidity_chart(ax, weather_data)
        plt.tight_layout()
        plt.savefig('jakarta_humidity.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        # Wind chart
        fig, ax = plt.subplots(figsize=(12, 8))
        self.create_wind_chart(ax, weather_data)
        plt.tight_layout()
        plt.savefig('jakarta_wind.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        # Impact factor chart
        fig, ax = plt.subplots(figsize=(12, 8))
        self.create_impact_factor_chart(ax, weather_data)
        plt.tight_layout()
        plt.savefig('jakarta_impact_factor.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✅ Grafik individual tersimpan:")
        print("  - jakarta_temperature.png")
        print("  - jakarta_humidity.png")
        print("  - jakarta_wind.png")
        print("  - jakarta_impact_factor.png")

def main():
    print("🌤️ Jakarta Weather Data Visualization - PNG Export")
    print("=" * 60)
    
    # Buat visualizer
    visualizer = JakartaWeatherVisualizerPNG()
    
    # Parse data
    print("🔍 Parsing weather data...")
    weather_data = visualizer.parse_weather_data(WEATHER_DATA)
    
    # Buat dashboard komprehensif
    print("📊 Membuat dashboard komprehensif...")
    visualizer.create_comprehensive_dashboard(weather_data)
    
    # Buat grafik individual
    print("📈 Membuat grafik individual...")
    visualizer.create_individual_charts(weather_data)
    
    print("\n🎉 Visualisasi selesai!")
    print("📁 File yang dihasilkan:")
    print("  - jakarta_weather_dashboard.png (Dashboard utama)")
    print("  - jakarta_temperature.png (Grafik temperatur)")
    print("  - jakarta_humidity.png (Grafik kelembaban)")
    print("  - jakarta_wind.png (Grafik angin)")
    print("  - jakarta_impact_factor.png (Grafik impact factor)")

if __name__ == "__main__":
    main() 