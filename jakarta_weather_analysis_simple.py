#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Forecast Analysis (Simple Version)
Analisis data cuaca Jakarta dalam sehari dengan interval 3 jam
Berdasarkan data dari OpenWeatherMap API
"""

import json
from datetime import datetime
import pandas as pd

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

class JakartaWeatherAnalyzer:
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
    
    def parse_weather_data(self, data):
        """Parse data cuaca dari API response"""
        parsed_data = []
        
        for item in data['list']:
            # Parse timestamp
            dt = datetime.fromtimestamp(item['dt'])
            
            # Extract weather data
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
    
    def create_weather_summary_table(self, weather_data):
        """Buat tabel ringkasan cuaca"""
        print("\n" + "="*120)
        print("🌤️ JAKARTA WEATHER FORECAST - 24 JAM (INTERVAL 3 JAM)")
        print("="*120)
        print("Data Source: OpenWeatherMap API")
        print("="*120)
        
        # Header
        header = f"{'Waktu':<12} {'Suhu':<8} {'Terasa':<8} {'Kelembaban':<12} {'Tekanan':<10} {'Angin':<8} {'Awan':<6} {'Jarak':<8} {'Hujan':<8} {'Kondisi':<20} {'Impact':<8}"
        print(header)
        print("-" * 120)
        
        # Data rows
        for data in weather_data:
            impact_factor = self.get_weather_impact_factor(data['weather_main'])
            
            row = (f"{data['time_str']:<12} "
                  f"{data['temperature']:<8.1f}°C "
                  f"{data['feels_like']:<8.1f}°C "
                  f"{data['humidity']:<12.0f}% "
                  f"{data['pressure']:<10.0f}hPa "
                  f"{data['wind_speed']:<8.1f}m/s "
                  f"{data['clouds']:<6.0f}% "
                  f"{data['visibility']/1000:<8.1f}km "
                  f"{data['rain_3h']:<8.1f}mm "
                  f"{data['weather_description']:<20} "
                  f"{impact_factor:<8.2f}x")
            print(row)
        
        print("-" * 120)
    
    def create_detailed_analysis(self, weather_data):
        """Analisis detail setiap variabel cuaca"""
        print("\n" + "="*80)
        print("📊 ANALISIS DETAIL VARIABEL CUACA JAKARTA")
        print("="*80)
        
        # 1. Temperature Analysis
        print("\n🌡️ ANALISIS TEMPERATUR:")
        print("-" * 40)
        temps = [data['temperature'] for data in weather_data]
        feels = [data['feels_like'] for data in weather_data]
        
        print(f"Temperatur Rata-rata: {sum(temps)/len(temps):.1f}°C")
        print(f"Temperatur Tertinggi: {max(temps):.1f}°C")
        print(f"Temperatur Terendah: {min(temps):.1f}°C")
        print(f"Feels Like Rata-rata: {sum(feels)/len(feels):.1f}°C")
        print(f"Selisih Terbesar (Feels Like - Actual): {max(feels) - max(temps):.1f}°C")
        
        # 2. Humidity Analysis
        print("\n💧 ANALISIS KELEMBABAN:")
        print("-" * 40)
        humidities = [data['humidity'] for data in weather_data]
        print(f"Kelembaban Rata-rata: {sum(humidities)/len(humidities):.0f}%")
        print(f"Kelembaban Tertinggi: {max(humidities):.0f}%")
        print(f"Kelembaban Terendah: {min(humidities):.0f}%")
        
        # 3. Wind Analysis
        print("\n💨 ANALISIS ANGIN:")
        print("-" * 40)
        wind_speeds = [data['wind_speed'] for data in weather_data]
        wind_dirs = [data['wind_deg'] for data in weather_data]
        
        print(f"Kecepatan Angin Rata-rata: {sum(wind_speeds)/len(wind_speeds):.1f} m/s")
        print(f"Kecepatan Angin Tertinggi: {max(wind_speeds):.1f} m/s")
        print(f"Kecepatan Angin Terendah: {min(wind_speeds):.1f} m/s")
        print(f"Arah Angin: {wind_dirs[0]:.0f}° - {wind_dirs[-1]:.0f}°")
        
        # 4. Pressure Analysis
        print("\n🌪️ ANALISIS TEKANAN UDARA:")
        print("-" * 40)
        pressures = [data['pressure'] for data in weather_data]
        print(f"Tekanan Rata-rata: {sum(pressures)/len(pressures):.0f} hPa")
        print(f"Tekanan Tertinggi: {max(pressures):.0f} hPa")
        print(f"Tekanan Terendah: {min(pressures):.0f} hPa")
        
        # 5. Cloud Cover Analysis
        print("\n☁️ ANALISIS TUTUPAN AWAN:")
        print("-" * 40)
        clouds = [data['clouds'] for data in weather_data]
        print(f"Tutupan Awan Rata-rata: {sum(clouds)/len(clouds):.0f}%")
        print(f"Tutupan Awan Tertinggi: {max(clouds):.0f}%")
        print(f"Tutupan Awan Terendah: {min(clouds):.0f}%")
        
        # 6. Visibility Analysis
        print("\n👁️ ANALISIS VISIBILITAS:")
        print("-" * 40)
        visibilities = [data['visibility']/1000 for data in weather_data]
        print(f"Visibilitas Rata-rata: {sum(visibilities)/len(visibilities):.1f} km")
        print(f"Visibilitas Tertinggi: {max(visibilities):.1f} km")
        print(f"Visibilitas Terendah: {min(visibilities):.1f} km")
        
        # 7. Precipitation Analysis
        print("\n🌧️ ANALISIS PRESIPITASI:")
        print("-" * 40)
        pops = [data['pop'] * 100 for data in weather_data]
        rains = [data['rain_3h'] for data in weather_data]
        
        print(f"Probabilitas Hujan Rata-rata: {sum(pops)/len(pops):.0f}%")
        print(f"Probabilitas Hujan Tertinggi: {max(pops):.0f}%")
        print(f"Total Curah Hujan: {sum(rains):.1f} mm")
        print(f"Curah Hujan Tertinggi per 3h: {max(rains):.1f} mm")
        
        # 8. Weather Impact Analysis
        print("\n⚡ ANALISIS DAMPAK CUACA PADA TRAFFIC:")
        print("-" * 40)
        impacts = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        print(f"Impact Factor Rata-rata: {sum(impacts)/len(impacts):.2f}x")
        print(f"Impact Factor Tertinggi: {max(impacts):.2f}x")
        print(f"Impact Factor Terendah: {min(impacts):.2f}x")
        
        # Weather conditions summary
        conditions = {}
        for data in weather_data:
            desc = data['weather_description']
            conditions[desc] = conditions.get(desc, 0) + 1
        
        print(f"\nKondisi Cuaca yang Terjadi:")
        for condition, count in conditions.items():
            percentage = (count / len(weather_data)) * 100
            print(f"  - {condition}: {count} kali ({percentage:.1f}%)")
    
    def create_traffic_impact_analysis(self, weather_data):
        """Analisis dampak cuaca pada traffic VRP"""
        print("\n" + "="*80)
        print("🚛 ANALISIS DAMPAK CUACA PADA SISTEM VRP")
        print("="*80)
        
        print("\n📊 DAMPAK PADA RUTE JAKARTA:")
        print("-" * 50)
        
        for i, data in enumerate(weather_data):
            impact_factor = self.get_weather_impact_factor(data['weather_main'])
            
            # Simulate base travel time (30 minutes for Jakarta routes)
            base_time = 30  # minutes
            impacted_time = base_time * impact_factor
            
            print(f"\n🕐 {data['time_str']} - {data['weather_description']}")
            print(f"   Impact Factor: {impact_factor:.2f}x")
            print(f"   Waktu Tempuh Normal: {base_time} menit")
            print(f"   Waktu Tempuh Terpengaruh: {impacted_time:.1f} menit")
            print(f"   Penambahan Waktu: {impacted_time - base_time:.1f} menit")
            
            # Traffic recommendations
            if impact_factor <= 1.1:
                recommendation = "✅ Rute normal, traffic minimal terpengaruh"
            elif impact_factor <= 1.3:
                recommendation = "⚠️ Rute alternatif disarankan, traffic sedang"
            else:
                recommendation = "🚨 Rute alternatif wajib, traffic berat"
            
            print(f"   Rekomendasi: {recommendation}")
    
    def save_to_csv(self, weather_data):
        """Simpan data ke CSV"""
        try:
            import pandas as pd
            
            # Prepare data for CSV
            csv_data = []
            for data in weather_data:
                csv_data.append({
                    'Waktu': data['time_str'],
                    'Tanggal': data['date_str'],
                    'Temperatur_C': data['temperature'],
                    'Terasa_C': data['feels_like'],
                    'Temp_Min_C': data['temp_min'],
                    'Temp_Max_C': data['temp_max'],
                    'Kelembaban_Persen': data['humidity'],
                    'Tekanan_hPa': data['pressure'],
                    'Kecepatan_Angin_ms': data['wind_speed'],
                    'Arah_Angin_Derajat': data['wind_deg'],
                    'Angin_Gust_ms': data['wind_gust'],
                    'Tutupan_Awan_Persen': data['clouds'],
                    'Visibilitas_km': data['visibility']/1000,
                    'Probabilitas_Hujan_Persen': data['pop'] * 100,
                    'Curah_Hujan_3h_mm': data['rain_3h'],
                    'Kondisi_Cuaca': data['weather_description'],
                    'Weather_Impact_Factor': self.get_weather_impact_factor(data['weather_main'])
                })
            
            df = pd.DataFrame(csv_data)
            df.to_csv('jakarta_weather_forecast_analysis.csv', index=False)
            print(f"\n✅ Data tersimpan ke 'jakarta_weather_forecast_analysis.csv'")
            
        except ImportError:
            print("\n⚠️ Pandas tidak tersedia, data tidak dapat disimpan ke CSV")
    
    def create_ascii_chart(self, weather_data):
        """Buat chart ASCII sederhana"""
        print("\n" + "="*80)
        print("📈 GRAFIK TEMPERATUR JAKARTA (ASCII)")
        print("="*80)
        
        temps = [data['temperature'] for data in weather_data]
        times = [data['time_str'] for data in weather_data]
        
        max_temp = max(temps)
        min_temp = min(temps)
        temp_range = max_temp - min_temp
        
        print(f"Temperatur: {min_temp:.1f}°C - {max_temp:.1f}°C")
        print()
        
        # Create ASCII chart
        for i, (temp, time) in enumerate(zip(temps, times)):
            # Normalize temperature to 0-50 range for display
            normalized = int(((temp - min_temp) / temp_range) * 50) if temp_range > 0 else 25
            
            bar = "█" * normalized
            print(f"{time:>8} | {bar:<50} | {temp:>5.1f}°C")
        
        print("-" * 70)

def main():
    """Main function"""
    print("🌤️ Jakarta Weather Forecast Analysis")
    print("="*60)
    
    # Initialize analyzer
    analyzer = JakartaWeatherAnalyzer()
    
    # Parse weather data
    print("🔍 Parsing weather data...")
    weather_data = analyzer.parse_weather_data(WEATHER_DATA)
    
    if not weather_data:
        print("❌ Failed to parse weather data")
        return
    
    # Create summary table
    analyzer.create_weather_summary_table(weather_data)
    
    # Create detailed analysis
    analyzer.create_detailed_analysis(weather_data)
    
    # Create traffic impact analysis
    analyzer.create_traffic_impact_analysis(weather_data)
    
    # Create ASCII chart
    analyzer.create_ascii_chart(weather_data)
    
    # Save to CSV
    analyzer.save_to_csv(weather_data)
    
    print("\n🎉 Jakarta weather analysis completed!")
    print("📁 Generated files:")
    print("  - jakarta_weather_forecast_analysis.csv")

if __name__ == "__main__":
    main() 