#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Data Export - CSV/Excel Format
Export data cuaca Jakarta ke format CSV yang terstruktur
"""

import csv
from datetime import datetime

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

class JakartaWeatherDataExporter:
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
            dt = datetime.fromtimestamp(item['dt'])
            
            weather_info = {
                'datetime': dt,
                'time_str': dt.strftime('%H:%M'),
                'date_str': dt.strftime('%d/%m/%Y'),
                'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
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
    
    def create_main_data_csv(self, weather_data):
        """Buat CSV utama dengan semua data"""
        filename = 'jakarta_weather_main_data.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Waktu', 'Tanggal', 'Timestamp', 'Temperatur (°C)', 'Terasa (°C)', 
                'Min (°C)', 'Max (°C)', 'Kelembaban (%)', 'Tekanan (hPa)', 
                'Angin (m/s)', 'Arah Angin (°)', 'Angin Gust (m/s)', 
                'Tutupan Awan (%)', 'Visibilitas (km)', 'Kondisi Cuaca', 
                'Deskripsi', 'Probabilitas Hujan', 'Curah Hujan (mm)', 
                'Weather Impact Factor', 'Dampak Level', 'Rekomendasi VRP'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in weather_data:
                impact_factor = self.get_weather_impact_factor(data['weather_main'])
                
                # Tentukan level dampak
                if impact_factor <= 1.1:
                    impact_level = "Rendah"
                    vrp_recommendation = "Rute Normal"
                elif impact_factor <= 1.3:
                    impact_level = "Sedang"
                    vrp_recommendation = "Rute Alternatif"
                else:
                    impact_level = "Tinggi"
                    vrp_recommendation = "Rute Alternatif + Waspada"
                
                writer.writerow({
                    'Waktu': data['time_str'],
                    'Tanggal': data['date_str'],
                    'Timestamp': data['timestamp'],
                    'Temperatur (°C)': round(data['temperature'], 1),
                    'Terasa (°C)': round(data['feels_like'], 1),
                    'Min (°C)': round(data['temp_min'], 1),
                    'Max (°C)': round(data['temp_max'], 1),
                    'Kelembaban (%)': round(data['humidity'], 0),
                    'Tekanan (hPa)': round(data['pressure'], 0),
                    'Angin (m/s)': round(data['wind_speed'], 1),
                    'Arah Angin (°)': round(data['wind_deg'], 0),
                    'Angin Gust (m/s)': round(data['wind_gust'], 1),
                    'Tutupan Awan (%)': round(data['clouds'], 0),
                    'Visibilitas (km)': round(data['visibility']/1000, 1),
                    'Kondisi Cuaca': data['weather_main'],
                    'Deskripsi': data['weather_description'],
                    'Probabilitas Hujan': round(data['pop'] * 100, 0),
                    'Curah Hujan (mm)': round(data['rain_3h'], 1),
                    'Weather Impact Factor': round(impact_factor, 2),
                    'Dampak Level': impact_level,
                    'Rekomendasi VRP': vrp_recommendation
                })
        
        print(f"✅ Data utama tersimpan sebagai '{filename}'")
    
    def create_temperature_analysis_csv(self, weather_data):
        """Buat CSV khusus analisis temperatur"""
        filename = 'jakarta_temperature_analysis.csv'
        
        temps = [data['temperature'] for data in weather_data]
        feels = [data['feels_like'] for data in weather_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Waktu', 'Temperatur Aktual (°C)', 'Temperatur Terasa (°C)', 
                'Selisih (°C)', 'Kategori Suhu', 'Kategori Terasa'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in weather_data:
                temp = data['temperature']
                feel = data['feels_like']
                diff = feel - temp
                
                # Kategori suhu
                if temp < 20:
                    temp_category = "Dingin"
                elif temp < 25:
                    temp_category = "Sejuk"
                elif temp < 30:
                    temp_category = "Hangat"
                elif temp < 35:
                    temp_category = "Panas"
                else:
                    temp_category = "Sangat Panas"
                
                # Kategori terasa
                if feel < 20:
                    feel_category = "Dingin"
                elif feel < 25:
                    feel_category = "Sejuk"
                elif feel < 30:
                    feel_category = "Hangat"
                elif feel < 35:
                    feel_category = "Panas"
                else:
                    feel_category = "Sangat Panas"
                
                writer.writerow({
                    'Waktu': data['time_str'],
                    'Temperatur Aktual (°C)': round(temp, 1),
                    'Temperatur Terasa (°C)': round(feel, 1),
                    'Selisih (°C)': round(diff, 1),
                    'Kategori Suhu': temp_category,
                    'Kategori Terasa': feel_category
                })
            
            # Tambahkan statistik
            writer.writerow({})
            writer.writerow({
                'Waktu': 'STATISTIK',
                'Temperatur Aktual (°C)': f"Rata-rata: {sum(temps)/len(temps):.1f}°C",
                'Temperatur Terasa (°C)': f"Rata-rata: {sum(feels)/len(feels):.1f}°C",
                'Selisih (°C)': f"Max: {max(feels) - max(temps):.1f}°C",
                'Kategori Suhu': f"Min: {min(temps):.1f}°C, Max: {max(temps):.1f}°C",
                'Kategori Terasa': f"Min: {min(feels):.1f}°C, Max: {max(feels):.1f}°C"
            })
        
        print(f"✅ Analisis temperatur tersimpan sebagai '{filename}'")
    
    def create_humidity_analysis_csv(self, weather_data):
        """Buat CSV khusus analisis kelembaban"""
        filename = 'jakarta_humidity_analysis.csv'
        
        humidities = [data['humidity'] for data in weather_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Waktu', 'Kelembaban (%)', 'Kategori Kelembaban', 
                'Dampak pada Kenyamanan', 'Dampak pada Traffic'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in weather_data:
                humidity = data['humidity']
                
                # Kategori kelembaban
                if humidity < 30:
                    category = "Sangat Kering"
                    comfort = "Tidak Nyaman"
                    traffic_impact = "Rendah"
                elif humidity < 50:
                    category = "Kering"
                    comfort = "Agak Nyaman"
                    traffic_impact = "Rendah"
                elif humidity < 70:
                    category = "Normal"
                    comfort = "Nyaman"
                    traffic_impact = "Normal"
                elif humidity < 80:
                    category = "Lembab"
                    comfort = "Agak Tidak Nyaman"
                    traffic_impact = "Sedang"
                else:
                    category = "Sangat Lembab"
                    comfort = "Tidak Nyaman"
                    traffic_impact = "Tinggi"
                
                writer.writerow({
                    'Waktu': data['time_str'],
                    'Kelembaban (%)': round(humidity, 0),
                    'Kategori Kelembaban': category,
                    'Dampak pada Kenyamanan': comfort,
                    'Dampak pada Traffic': traffic_impact
                })
            
            # Tambahkan statistik
            writer.writerow({})
            writer.writerow({
                'Waktu': 'STATISTIK',
                'Kelembaban (%)': f"Rata-rata: {sum(humidities)/len(humidities):.0f}%",
                'Kategori Kelembaban': f"Min: {min(humidities):.0f}%, Max: {max(humidities):.0f}%",
                'Dampak pada Kenyamanan': f"Range: {max(humidities) - min(humidities):.0f}%",
                'Dampak pada Traffic': f"Tinggi (>80%): {sum(1 for h in humidities if h > 80)} periode"
            })
        
        print(f"✅ Analisis kelembaban tersimpan sebagai '{filename}'")
    
    def create_wind_analysis_csv(self, weather_data):
        """Buat CSV khusus analisis angin"""
        filename = 'jakarta_wind_analysis.csv'
        
        wind_speeds = [data['wind_speed'] for data in weather_data]
        wind_gusts = [data['wind_gust'] for data in weather_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Waktu', 'Kecepatan Angin (m/s)', 'Angin Gust (m/s)', 
                'Arah Angin (°)', 'Kategori Angin', 'Dampak pada Traffic'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in weather_data:
                wind_speed = data['wind_speed']
                wind_gust = data['wind_gust']
                
                # Kategori angin
                if wind_speed < 0.5:
                    category = "Tenang"
                    traffic_impact = "Tidak Ada"
                elif wind_speed < 1.5:
                    category = "Lemah"
                    traffic_impact = "Minimal"
                elif wind_speed < 2.5:
                    category = "Sedang"
                    traffic_impact = "Sedang"
                elif wind_speed < 4.0:
                    category = "Kuat"
                    traffic_impact = "Signifikan"
                else:
                    category = "Sangat Kuat"
                    traffic_impact = "Tinggi"
                
                writer.writerow({
                    'Waktu': data['time_str'],
                    'Kecepatan Angin (m/s)': round(wind_speed, 1),
                    'Angin Gust (m/s)': round(wind_gust, 1),
                    'Arah Angin (°)': round(data['wind_deg'], 0),
                    'Kategori Angin': category,
                    'Dampak pada Traffic': traffic_impact
                })
            
            # Tambahkan statistik
            writer.writerow({})
            writer.writerow({
                'Waktu': 'STATISTIK',
                'Kecepatan Angin (m/s)': f"Rata-rata: {sum(wind_speeds)/len(wind_speeds):.1f} m/s",
                'Angin Gust (m/s)': f"Rata-rata: {sum(wind_gusts)/len(wind_gusts):.1f} m/s",
                'Arah Angin (°)': f"Max: {max(wind_speeds):.1f} m/s",
                'Kategori Angin': f"Min: {min(wind_speeds):.1f} m/s",
                'Dampak pada Traffic': f"Range: {max(wind_speeds) - min(wind_speeds):.1f} m/s"
            })
        
        print(f"✅ Analisis angin tersimpan sebagai '{filename}'")
    
    def create_vrp_impact_analysis_csv(self, weather_data):
        """Buat CSV khusus analisis dampak VRP"""
        filename = 'jakarta_vrp_impact_analysis.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Waktu', 'Kondisi Cuaca', 'Weather Impact Factor', 
                'Waktu Normal (menit)', 'Waktu Terpengaruh (menit)', 
                'Penambahan Waktu (menit)', 'Dampak Level', 'Rekomendasi Rute',
                'Faktor Kunci', 'Catatan'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in weather_data:
                impact_factor = self.get_weather_impact_factor(data['weather_main'])
                base_time = 30  # menit
                affected_time = base_time * impact_factor
                time_increase = affected_time - base_time
                
                # Tentukan dampak level
                if impact_factor <= 1.1:
                    impact_level = "Rendah"
                    recommendation = "Rute Normal"
                    key_factor = "Kondisi Baik"
                    notes = "Tidak ada hambatan signifikan"
                elif impact_factor <= 1.3:
                    impact_level = "Sedang"
                    recommendation = "Rute Alternatif"
                    key_factor = "Hujan Ringan/Sedang"
                    notes = "Perlu waktu tambahan untuk perjalanan"
                else:
                    impact_level = "Tinggi"
                    recommendation = "Rute Alternatif + Waspada"
                    key_factor = "Hujan Lebat/Badai"
                    notes = "Hindari rute rawan genangan"
                
                writer.writerow({
                    'Waktu': data['time_str'],
                    'Kondisi Cuaca': data['weather_description'],
                    'Weather Impact Factor': round(impact_factor, 2),
                    'Waktu Normal (menit)': base_time,
                    'Waktu Terpengaruh (menit)': round(affected_time, 1),
                    'Penambahan Waktu (menit)': round(time_increase, 1),
                    'Dampak Level': impact_level,
                    'Rekomendasi Rute': recommendation,
                    'Faktor Kunci': key_factor,
                    'Catatan': notes
                })
            
            # Tambahkan ringkasan
            impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
            avg_impact = sum(impact_factors) / len(impact_factors)
            
            writer.writerow({})
            writer.writerow({
                'Waktu': 'RINGKASAN VRP',
                'Kondisi Cuaca': f"Rata-rata Impact Factor: {avg_impact:.2f}x",
                'Weather Impact Factor': f"Penambahan Waktu Rata-rata: {(avg_impact - 1) * 30:.1f} menit",
                'Waktu Normal (menit)': f"Rute Normal: {sum(1 for i in impact_factors if i <= 1.1)} periode",
                'Waktu Terpengaruh (menit)': f"Rute Alternatif: {sum(1 for i in impact_factors if i > 1.1)} periode",
                'Penambahan Waktu (menit)': f"Dampak Rendah: {sum(1 for i in impact_factors if i <= 1.1)} periode",
                'Dampak Level': f"Dampak Sedang: {sum(1 for i in impact_factors if 1.1 < i <= 1.3)} periode",
                'Rekomendasi Rute': f"Dampak Tinggi: {sum(1 for i in impact_factors if i > 1.3)} periode",
                'Faktor Kunci': f"Total Curah Hujan: {sum(data['rain_3h'] for data in weather_data):.1f} mm",
                'Catatan': "Analisis berdasarkan data OpenWeatherMap API"
            })
        
        print(f"✅ Analisis dampak VRP tersimpan sebagai '{filename}'")
    
    def create_summary_statistics_csv(self, weather_data):
        """Buat CSV ringkasan statistik"""
        filename = 'jakarta_weather_summary_statistics.csv'
        
        # Hitung statistik
        temps = [data['temperature'] for data in weather_data]
        humidities = [data['humidity'] for data in weather_data]
        wind_speeds = [data['wind_speed'] for data in weather_data]
        pressures = [data['pressure'] for data in weather_data]
        clouds = [data['clouds'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        rain_totals = [data['rain_3h'] for data in weather_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Kategori', 'Metrik', 'Nilai', 'Satuan', 'Keterangan'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Temperatur
            writer.writerow({'Kategori': 'TEMPERATUR', 'Metrik': 'Rata-rata', 'Nilai': round(sum(temps)/len(temps), 1), 'Satuan': '°C', 'Keterangan': 'Temperatur aktual'})
            writer.writerow({'Kategori': 'TEMPERATUR', 'Metrik': 'Tertinggi', 'Nilai': round(max(temps), 1), 'Satuan': '°C', 'Keterangan': f"Pukul {weather_data[temps.index(max(temps))]['time_str']}"})
            writer.writerow({'Kategori': 'TEMPERATUR', 'Metrik': 'Terendah', 'Nilai': round(min(temps), 1), 'Satuan': '°C', 'Keterangan': f"Pukul {weather_data[temps.index(min(temps))]['time_str']}"})
            writer.writerow({'Kategori': 'TEMPERATUR', 'Metrik': 'Range', 'Nilai': round(max(temps) - min(temps), 1), 'Satuan': '°C', 'Keterangan': 'Selisih tertinggi-terendah'})
            
            # Kelembaban
            writer.writerow({'Kategori': 'KELEMBABAN', 'Metrik': 'Rata-rata', 'Nilai': round(sum(humidities)/len(humidities), 0), 'Satuan': '%', 'Keterangan': 'Kelembaban relatif'})
            writer.writerow({'Kategori': 'KELEMBABAN', 'Metrik': 'Tertinggi', 'Nilai': round(max(humidities), 0), 'Satuan': '%', 'Keterangan': f"Pukul {weather_data[humidities.index(max(humidities))]['time_str']}"})
            writer.writerow({'Kategori': 'KELEMBABAN', 'Metrik': 'Terendah', 'Nilai': round(min(humidities), 0), 'Satuan': '%', 'Keterangan': f"Pukul {weather_data[humidities.index(min(humidities))]['time_str']}"})
            writer.writerow({'Kategori': 'KELEMBABAN', 'Metrik': 'Tinggi (>80%)', 'Nilai': sum(1 for h in humidities if h > 80), 'Satuan': 'periode', 'Keterangan': 'Jumlah periode kelembaban tinggi'})
            
            # Angin
            writer.writerow({'Kategori': 'ANGIN', 'Metrik': 'Rata-rata', 'Nilai': round(sum(wind_speeds)/len(wind_speeds), 1), 'Satuan': 'm/s', 'Keterangan': 'Kecepatan angin'})
            writer.writerow({'Kategori': 'ANGIN', 'Metrik': 'Tertinggi', 'Nilai': round(max(wind_speeds), 1), 'Satuan': 'm/s', 'Keterangan': f"Pukul {weather_data[wind_speeds.index(max(wind_speeds))]['time_str']}"})
            writer.writerow({'Kategori': 'ANGIN', 'Metrik': 'Terendah', 'Nilai': round(min(wind_speeds), 1), 'Satuan': 'm/s', 'Keterangan': f"Pukul {weather_data[wind_speeds.index(min(wind_speeds))]['time_str']}"})
            
            # Tekanan
            writer.writerow({'Kategori': 'TEKANAN', 'Metrik': 'Rata-rata', 'Nilai': round(sum(pressures)/len(pressures), 0), 'Satuan': 'hPa', 'Keterangan': 'Tekanan atmosfer'})
            writer.writerow({'Kategori': 'TEKANAN', 'Metrik': 'Tertinggi', 'Nilai': round(max(pressures), 0), 'Satuan': 'hPa', 'Keterangan': f"Pukul {weather_data[pressures.index(max(pressures))]['time_str']}"})
            writer.writerow({'Kategori': 'TEKANAN', 'Metrik': 'Terendah', 'Nilai': round(min(pressures), 0), 'Satuan': 'hPa', 'Keterangan': f"Pukul {weather_data[pressures.index(min(pressures))]['time_str']}"})
            
            # Awan
            writer.writerow({'Kategori': 'AWAN', 'Metrik': 'Rata-rata', 'Nilai': round(sum(clouds)/len(clouds), 0), 'Satuan': '%', 'Keterangan': 'Tutupan awan'})
            writer.writerow({'Kategori': 'AWAN', 'Metrik': 'Tertinggi', 'Nilai': round(max(clouds), 0), 'Satuan': '%', 'Keterangan': f"Pukul {weather_data[clouds.index(max(clouds))]['time_str']}"})
            writer.writerow({'Kategori': 'AWAN', 'Metrik': 'Berawan Tebal', 'Nilai': sum(1 for c in clouds if c >= 75), 'Satuan': 'periode', 'Keterangan': 'Tutupan awan ≥75%'})
            
            # Impact Factor
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Rata-rata', 'Nilai': round(sum(impact_factors)/len(impact_factors), 2), 'Satuan': 'x', 'Keterangan': 'Weather impact factor'})
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Tertinggi', 'Nilai': round(max(impact_factors), 2), 'Satuan': 'x', 'Keterangan': 'Dampak maksimal'})
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Terendah', 'Nilai': round(min(impact_factors), 2), 'Satuan': 'x', 'Keterangan': 'Dampak minimal'})
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Dampak Rendah', 'Nilai': sum(1 for i in impact_factors if i <= 1.1), 'Satuan': 'periode', 'Keterangan': 'Impact factor ≤1.1x'})
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Dampak Sedang', 'Nilai': sum(1 for i in impact_factors if 1.1 < i <= 1.3), 'Satuan': 'periode', 'Keterangan': 'Impact factor 1.1-1.3x'})
            writer.writerow({'Kategori': 'IMPACT FACTOR', 'Metrik': 'Dampak Tinggi', 'Nilai': sum(1 for i in impact_factors if i > 1.3), 'Satuan': 'periode', 'Keterangan': 'Impact factor >1.3x'})
            
            # Hujan
            writer.writerow({'Kategori': 'HUJAN', 'Metrik': 'Total Curah Hujan', 'Nilai': round(sum(rain_totals), 1), 'Satuan': 'mm', 'Keterangan': '24 jam'})
            writer.writerow({'Kategori': 'HUJAN', 'Metrik': 'Rata-rata per 3 jam', 'Nilai': round(sum(rain_totals)/len(rain_totals), 1), 'Satuan': 'mm', 'Keterangan': 'Per periode'})
            writer.writerow({'Kategori': 'HUJAN', 'Metrik': 'Tertinggi', 'Nilai': round(max(rain_totals), 1), 'Satuan': 'mm', 'Keterangan': f"Pukul {weather_data[rain_totals.index(max(rain_totals))]['time_str']}"})
            writer.writerow({'Kategori': 'HUJAN', 'Metrik': 'Periode Hujan', 'Nilai': sum(1 for r in rain_totals if r > 0), 'Satuan': 'periode', 'Keterangan': 'Jumlah periode dengan hujan'})
            
            # VRP
            writer.writerow({'Kategori': 'VRP', 'Metrik': 'Rute Normal', 'Nilai': sum(1 for i in impact_factors if i <= 1.1), 'Satuan': 'periode', 'Keterangan': 'Tidak perlu rute alternatif'})
            writer.writerow({'Kategori': 'VRP', 'Metrik': 'Rute Alternatif', 'Nilai': sum(1 for i in impact_factors if i > 1.1), 'Satuan': 'periode', 'Keterangan': 'Perlu rute alternatif'})
            writer.writerow({'Kategori': 'VRP', 'Metrik': 'Penambahan Waktu', 'Nilai': round((sum(impact_factors)/len(impact_factors) - 1) * 30, 1), 'Satuan': 'menit', 'Keterangan': 'Rata-rata per rute'})
        
        print(f"✅ Statistik ringkasan tersimpan sebagai '{filename}'")

def main():
    print("🌤️ Jakarta Weather Data Export - CSV/Excel Format")
    print("=" * 60)
    
    # Buat exporter
    exporter = JakartaWeatherDataExporter()
    
    # Parse data
    print("🔍 Parsing weather data...")
    weather_data = exporter.parse_weather_data(WEATHER_DATA)
    
    # Buat berbagai file CSV
    print("📊 Membuat file CSV...")
    
    # 1. Data utama
    exporter.create_main_data_csv(weather_data)
    
    # 2. Analisis temperatur
    exporter.create_temperature_analysis_csv(weather_data)
    
    # 3. Analisis kelembaban
    exporter.create_humidity_analysis_csv(weather_data)
    
    # 4. Analisis angin
    exporter.create_wind_analysis_csv(weather_data)
    
    # 5. Analisis dampak VRP
    exporter.create_vrp_impact_analysis_csv(weather_data)
    
    # 6. Statistik ringkasan
    exporter.create_summary_statistics_csv(weather_data)
    
    print("\n🎉 Export selesai!")
    print("📁 File CSV yang dihasilkan:")
    print("  - jakarta_weather_main_data.csv (Data utama lengkap)")
    print("  - jakarta_temperature_analysis.csv (Analisis temperatur)")
    print("  - jakarta_humidity_analysis.csv (Analisis kelembaban)")
    print("  - jakarta_wind_analysis.csv (Analisis angin)")
    print("  - jakarta_vrp_impact_analysis.csv (Analisis dampak VRP)")
    print("  - jakarta_weather_summary_statistics.csv (Statistik ringkasan)")
    print("\n💡 Cara menggunakan:")
    print("  1. Buka file CSV di Excel, Google Sheets, atau aplikasi spreadsheet")
    print("  2. File dapat digunakan untuk analisis lebih lanjut")
    print("  3. Data siap untuk visualisasi atau laporan")

if __name__ == "__main__":
    main() 