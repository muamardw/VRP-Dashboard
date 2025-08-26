#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Data Visualization - Simple PNG Export
Visualisasi data cuaca Jakarta dengan export PNG menggunakan PIL
"""

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math

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

class JakartaWeatherVisualizerSimple:
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
            'background': (255, 255, 255),
            'text': (0, 0, 0),
            'title': (25, 25, 112),
            'temperature': (255, 107, 107),
            'humidity': (78, 205, 196),
            'wind': (69, 183, 209),
            'pressure': (150, 206, 180),
            'clouds': (255, 234, 167),
            'rain': (221, 160, 221),
            'impact_low': (144, 238, 144),
            'impact_medium': (255, 215, 0),
            'impact_high': (255, 99, 71)
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
    
    def create_weather_dashboard(self, weather_data):
        """Buat dashboard cuaca utama"""
        # Buat gambar dengan ukuran besar
        width, height = 1600, 1200
        img = Image.new('RGB', (width, height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Coba gunakan font default
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            header_font = ImageFont.truetype("arial.ttf", 24)
            normal_font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            # Fallback ke font default
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Header
        draw.text((50, 30), "🌤️ JAKARTA WEATHER FORECAST DASHBOARD", 
                  fill=self.colors['title'], font=title_font)
        draw.text((50, 80), "24 Jam - Interval 3 Jam | Data Source: OpenWeatherMap API", 
                  fill=self.colors['text'], font=normal_font)
        
        # Buat tabel data utama
        self.create_main_data_table(draw, weather_data, 50, 120, normal_font, small_font)
        
        # Buat grafik temperatur
        self.create_temperature_chart(draw, weather_data, 50, 400, normal_font, small_font)
        
        # Buat grafik kelembaban
        self.create_humidity_chart(draw, weather_data, 50, 600, normal_font, small_font)
        
        # Buat grafik angin
        self.create_wind_chart(draw, weather_data, 50, 800, normal_font, small_font)
        
        # Buat grafik impact factor
        self.create_impact_chart(draw, weather_data, 50, 1000, normal_font, small_font)
        
        # Simpan gambar
        img.save('jakarta_weather_dashboard_simple.png', 'PNG')
        print("✅ Dashboard tersimpan sebagai 'jakarta_weather_dashboard_simple.png'")
    
    def create_main_data_table(self, draw, weather_data, x, y, normal_font, small_font):
        """Buat tabel data utama"""
        # Header tabel
        headers = ["Waktu", "Suhu", "Kelembaban", "Angin", "Awan", "Hujan", "Kondisi", "Impact"]
        col_widths = [80, 60, 80, 60, 60, 60, 120, 60]
        
        # Draw header
        current_x = x
        for i, header in enumerate(headers):
            draw.rectangle([current_x, y, current_x + col_widths[i], y + 30], 
                          outline=self.colors['text'], fill=self.colors['title'])
            draw.text((current_x + 5, y + 5), header, fill=self.colors['background'], font=small_font)
            current_x += col_widths[i]
        
        # Draw data rows
        row_height = 25
        for i, data in enumerate(weather_data):
            row_y = y + 30 + (i * row_height)
            
            # Alternate row colors
            row_color = (240, 240, 240) if i % 2 == 0 else (255, 255, 255)
            draw.rectangle([x, row_y, x + sum(col_widths), row_y + row_height], 
                          outline=self.colors['text'], fill=row_color)
            
            # Fill data
            current_x = x
            impact_factor = self.get_weather_impact_factor(data['weather_main'])
            
            # Waktu
            draw.text((current_x + 5, row_y + 5), data['time_str'], fill=self.colors['text'], font=small_font)
            current_x += col_widths[0]
            
            # Suhu
            draw.text((current_x + 5, row_y + 5), f"{data['temperature']:.1f}°C", 
                     fill=self.colors['temperature'], font=small_font)
            current_x += col_widths[1]
            
            # Kelembaban
            draw.text((current_x + 5, row_y + 5), f"{data['humidity']:.0f}%", 
                     fill=self.colors['humidity'], font=small_font)
            current_x += col_widths[2]
            
            # Angin
            draw.text((current_x + 5, row_y + 5), f"{data['wind_speed']:.1f}m/s", 
                     fill=self.colors['wind'], font=small_font)
            current_x += col_widths[3]
            
            # Awan
            draw.text((current_x + 5, row_y + 5), f"{data['clouds']:.0f}%", 
                     fill=self.colors['clouds'], font=small_font)
            current_x += col_widths[4]
            
            # Hujan
            draw.text((current_x + 5, row_y + 5), f"{data['rain_3h']:.1f}mm", 
                     fill=self.colors['rain'], font=small_font)
            current_x += col_widths[5]
            
            # Kondisi
            draw.text((current_x + 5, row_y + 5), data['weather_description'][:15], 
                     fill=self.colors['text'], font=small_font)
            current_x += col_widths[6]
            
            # Impact
            impact_color = self.colors['impact_low'] if impact_factor <= 1.1 else \
                          self.colors['impact_medium'] if impact_factor <= 1.3 else \
                          self.colors['impact_high']
            draw.text((current_x + 5, row_y + 5), f"{impact_factor:.2f}x", 
                     fill=impact_color, font=small_font)
    
    def create_temperature_chart(self, draw, weather_data, x, y, normal_font, small_font):
        """Buat grafik temperatur sederhana"""
        chart_width, chart_height = 1400, 150
        chart_x, chart_y = x, y
        
        # Title
        draw.text((chart_x, chart_y - 30), "🌡️ TEMPERATUR JAKARTA", 
                  fill=self.colors['title'], font=normal_font)
        
        # Chart background
        draw.rectangle([chart_x, chart_y, chart_x + chart_width, chart_y + chart_height], 
                      outline=self.colors['text'], fill=(250, 250, 250))
        
        # Find min/max for scaling
        temps = [data['temperature'] for data in weather_data]
        feels = [data['feels_like'] for data in weather_data]
        min_temp = min(min(temps), min(feels))
        max_temp = max(max(temps), max(feels))
        temp_range = max_temp - min_temp
        
        # Draw temperature lines
        for i in range(len(weather_data) - 1):
            # Actual temperature
            x1 = chart_x + 50 + (i * (chart_width - 100) // (len(weather_data) - 1))
            y1 = chart_y + chart_height - 20 - ((temps[i] - min_temp) / temp_range * (chart_height - 40))
            x2 = chart_x + 50 + ((i + 1) * (chart_width - 100) // (len(weather_data) - 1))
            y2 = chart_y + chart_height - 20 - ((temps[i + 1] - min_temp) / temp_range * (chart_height - 40))
            
            draw.line([(x1, y1), (x2, y2)], fill=self.colors['temperature'], width=3)
            draw.ellipse([x1-3, y1-3, x1+3, y1+3], fill=self.colors['temperature'])
            
            # Feels like temperature
            y1_feel = chart_y + chart_height - 20 - ((feels[i] - min_temp) / temp_range * (chart_height - 40))
            y2_feel = chart_y + chart_height - 20 - ((feels[i + 1] - min_temp) / temp_range * (chart_height - 40))
            
            draw.line([(x1, y1_feel), (x2, y2_feel)], fill=(255, 142, 83), width=2)
            draw.ellipse([x1-2, y1_feel-2, x1+2, y1_feel+2], fill=(255, 142, 83))
        
        # Draw last point
        last_x = chart_x + 50 + ((len(weather_data) - 1) * (chart_width - 100) // (len(weather_data) - 1))
        last_y = chart_y + chart_height - 20 - ((temps[-1] - min_temp) / temp_range * (chart_height - 40))
        last_y_feel = chart_y + chart_height - 20 - ((feels[-1] - min_temp) / temp_range * (chart_height - 40))
        
        draw.ellipse([last_x-3, last_y-3, last_x+3, last_y+3], fill=self.colors['temperature'])
        draw.ellipse([last_x-2, last_y_feel-2, last_x+2, last_y_feel+2], fill=(255, 142, 83))
        
        # Add time labels
        for i, data in enumerate(weather_data):
            label_x = chart_x + 50 + (i * (chart_width - 100) // (len(weather_data) - 1))
            label_y = chart_y + chart_height - 10
            draw.text((label_x - 10, label_y), data['time_str'], fill=self.colors['text'], font=small_font)
    
    def create_humidity_chart(self, draw, weather_data, x, y, normal_font, small_font):
        """Buat grafik kelembaban sederhana"""
        chart_width, chart_height = 1400, 150
        chart_x, chart_y = x, y
        
        # Title
        draw.text((chart_x, chart_y - 30), "💧 KELEMBABAN JAKARTA", 
                  fill=self.colors['title'], font=normal_font)
        
        # Chart background
        draw.rectangle([chart_x, chart_y, chart_x + chart_width, chart_y + chart_height], 
                      outline=self.colors['text'], fill=(250, 250, 250))
        
        # Draw humidity bars
        bar_width = (chart_width - 100) // len(weather_data)
        max_humidity = max(data['humidity'] for data in weather_data)
        
        for i, data in enumerate(weather_data):
            bar_x = chart_x + 50 + (i * bar_width)
            bar_height = (data['humidity'] / max_humidity) * (chart_height - 40)
            bar_y = chart_y + chart_height - 20 - bar_height
            
            # Bar color based on humidity level
            if data['humidity'] > 80:
                bar_color = (255, 99, 71)  # Red for high humidity
            elif data['humidity'] > 60:
                bar_color = (255, 215, 0)  # Gold for medium humidity
            else:
                bar_color = self.colors['humidity']  # Blue for low humidity
            
            draw.rectangle([bar_x, bar_y, bar_x + bar_width - 10, chart_y + chart_height - 20], 
                          fill=bar_color, outline=self.colors['text'])
            
            # Add value label
            draw.text((bar_x + 5, bar_y - 15), f"{data['humidity']:.0f}%", 
                     fill=self.colors['text'], font=small_font)
            
            # Add time label
            draw.text((bar_x + 5, chart_y + chart_height - 10), data['time_str'], 
                     fill=self.colors['text'], font=small_font)
    
    def create_wind_chart(self, draw, weather_data, x, y, normal_font, small_font):
        """Buat grafik angin sederhana"""
        chart_width, chart_height = 1400, 150
        chart_x, chart_y = x, y
        
        # Title
        draw.text((chart_x, chart_y - 30), "💨 KECEPATAN ANGIN JAKARTA", 
                  fill=self.colors['title'], font=normal_font)
        
        # Chart background
        draw.rectangle([chart_x, chart_y, chart_x + chart_width, chart_y + chart_height], 
                      outline=self.colors['text'], fill=(250, 250, 250))
        
        # Draw wind speed bars
        bar_width = (chart_width - 100) // len(weather_data)
        max_wind = max(data['wind_speed'] for data in weather_data)
        
        for i, data in enumerate(weather_data):
            bar_x = chart_x + 50 + (i * bar_width)
            bar_height = (data['wind_speed'] / max_wind) * (chart_height - 40)
            bar_y = chart_y + chart_height - 20 - bar_height
            
            # Bar color based on wind speed
            if data['wind_speed'] > 2.5:
                bar_color = (255, 99, 71)  # Red for high wind
            elif data['wind_speed'] > 1.5:
                bar_color = (255, 215, 0)  # Gold for medium wind
            else:
                bar_color = self.colors['wind']  # Blue for low wind
            
            draw.rectangle([bar_x, bar_y, bar_x + bar_width - 10, chart_y + chart_height - 20], 
                          fill=bar_color, outline=self.colors['text'])
            
            # Add value label
            draw.text((bar_x + 5, bar_y - 15), f"{data['wind_speed']:.1f}m/s", 
                     fill=self.colors['text'], font=small_font)
            
            # Add time label
            draw.text((bar_x + 5, chart_y + chart_height - 10), data['time_str'], 
                     fill=self.colors['text'], font=small_font)
    
    def create_impact_chart(self, draw, weather_data, x, y, normal_font, small_font):
        """Buat grafik impact factor sederhana"""
        chart_width, chart_height = 1400, 150
        chart_x, chart_y = x, y
        
        # Title
        draw.text((chart_x, chart_y - 30), "⚡ WEATHER IMPACT FACTOR", 
                  fill=self.colors['title'], font=normal_font)
        
        # Chart background
        draw.rectangle([chart_x, chart_y, chart_x + chart_width, chart_y + chart_height], 
                      outline=self.colors['text'], fill=(250, 250, 250))
        
        # Draw impact factor bars
        bar_width = (chart_width - 100) // len(weather_data)
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        max_impact = max(impact_factors)
        
        for i, impact in enumerate(impact_factors):
            bar_x = chart_x + 50 + (i * bar_width)
            bar_height = (impact / max_impact) * (chart_height - 40)
            bar_y = chart_y + chart_height - 20 - bar_height
            
            # Bar color based on impact level
            if impact <= 1.1:
                bar_color = self.colors['impact_low']  # Green for low impact
            elif impact <= 1.3:
                bar_color = self.colors['impact_medium']  # Gold for medium impact
            else:
                bar_color = self.colors['impact_high']  # Red for high impact
            
            draw.rectangle([bar_x, bar_y, bar_x + bar_width - 10, chart_y + chart_height - 20], 
                          fill=bar_color, outline=self.colors['text'])
            
            # Add value label
            draw.text((bar_x + 5, bar_y - 15), f"{impact:.2f}x", 
                     fill=self.colors['text'], font=small_font)
            
            # Add weather description
            desc = weather_data[i]['weather_description'][:10]
            draw.text((bar_x + 5, bar_y - 30), desc, 
                     fill=self.colors['text'], font=small_font)
            
            # Add time label
            draw.text((bar_x + 5, chart_y + chart_height - 10), weather_data[i]['time_str'], 
                     fill=self.colors['text'], font=small_font)
    
    def create_summary_image(self, weather_data):
        """Buat gambar ringkasan statistik"""
        width, height = 800, 600
        img = Image.new('RGB', (width, height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            normal_font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Title
        draw.text((50, 30), "📊 RINGKASAN CUACA JAKARTA", 
                  fill=self.colors['title'], font=title_font)
        
        # Calculate statistics
        temps = [data['temperature'] for data in weather_data]
        humidity = [data['humidity'] for data in weather_data]
        wind_speed = [data['wind_speed'] for data in weather_data]
        pressure = [data['pressure'] for data in weather_data]
        clouds = [data['clouds'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        
        # Summary text
        summary_lines = [
            f"🌡️ TEMPERATUR:",
            f"  Rata-rata: {sum(temps)/len(temps):.1f}°C",
            f"  Min: {min(temps):.1f}°C, Max: {max(temps):.1f}°C",
            "",
            f"💧 KELEMBABAN:",
            f"  Rata-rata: {sum(humidity)/len(humidity):.0f}%",
            f"  Min: {min(humidity):.0f}%, Max: {max(humidity):.0f}%",
            "",
            f"💨 ANGIN:",
            f"  Rata-rata: {sum(wind_speed)/len(wind_speed):.1f} m/s",
            f"  Max: {max(wind_speed):.1f} m/s",
            "",
            f"⚡ IMPACT FACTOR:",
            f"  Rata-rata: {sum(impact_factors)/len(impact_factors):.2f}x",
            f"  Dampak Rendah: {sum(1 for i in impact_factors if i <= 1.1)} periode",
            f"  Dampak Sedang: {sum(1 for i in impact_factors if 1.1 < i <= 1.3)} periode",
            f"  Dampak Tinggi: {sum(1 for i in impact_factors if i > 1.3)} periode",
            "",
            f"🚛 REKOMENDASI VRP:",
            f"  Rute Normal: {sum(1 for i in impact_factors if i <= 1.1)} periode",
            f"  Rute Alternatif: {sum(1 for i in impact_factors if i > 1.1)} periode",
            f"  Penambahan Waktu: {(sum(impact_factors)/len(impact_factors) - 1) * 30:.1f} menit"
        ]
        
        # Draw summary text
        y_pos = 80
        for line in summary_lines:
            if line.startswith("🌡️") or line.startswith("💧") or line.startswith("💨") or line.startswith("⚡") or line.startswith("🚛"):
                draw.text((50, y_pos), line, fill=self.colors['title'], font=normal_font)
            elif line == "":
                pass
            else:
                draw.text((50, y_pos), line, fill=self.colors['text'], font=normal_font)
            y_pos += 25
        
        # Save image
        img.save('jakarta_weather_summary.png', 'PNG')
        print("✅ Ringkasan tersimpan sebagai 'jakarta_weather_summary.png'")

def main():
    print("🌤️ Jakarta Weather Data Visualization - Simple PNG Export")
    print("=" * 60)
    
    # Buat visualizer
    visualizer = JakartaWeatherVisualizerSimple()
    
    # Parse data
    print("🔍 Parsing weather data...")
    weather_data = visualizer.parse_weather_data(WEATHER_DATA)
    
    # Buat dashboard utama
    print("📊 Membuat dashboard utama...")
    visualizer.create_weather_dashboard(weather_data)
    
    # Buat ringkasan
    print("📈 Membuat ringkasan statistik...")
    visualizer.create_summary_image(weather_data)
    
    print("\n🎉 Visualisasi selesai!")
    print("📁 File yang dihasilkan:")
    print("  - jakarta_weather_dashboard_simple.png (Dashboard utama)")
    print("  - jakarta_weather_summary.png (Ringkasan statistik)")

if __name__ == "__main__":
    main() 