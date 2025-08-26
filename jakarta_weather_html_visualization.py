#!/usr/bin/env python3
"""
🌤️ Jakarta Weather Data Visualization - HTML Export
Visualisasi data cuaca Jakarta dengan export HTML menggunakan Chart.js
"""

from datetime import datetime
import json

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

class JakartaWeatherHTMLVisualizer:
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
    
    def create_html_dashboard(self, weather_data):
        """Buat dashboard HTML dengan Chart.js"""
        
        # Prepare data for charts
        labels = [data['time_str'] for data in weather_data]
        temperatures = [data['temperature'] for data in weather_data]
        feels_like = [data['feels_like'] for data in weather_data]
        humidity = [data['humidity'] for data in weather_data]
        wind_speed = [data['wind_speed'] for data in weather_data]
        wind_gust = [data['wind_gust'] for data in weather_data]
        clouds = [data['clouds'] for data in weather_data]
        pressure = [data['pressure'] for data in weather_data]
        rain_3h = [data['rain_3h'] for data in weather_data]
        impact_factors = [self.get_weather_impact_factor(data['weather_main']) for data in weather_data]
        weather_descriptions = [data['weather_description'] for data in weather_data]
        
        # Calculate statistics
        avg_temp = sum(temperatures) / len(temperatures)
        avg_humidity = sum(humidity) / len(humidity)
        avg_wind = sum(wind_speed) / len(wind_speed)
        avg_impact = sum(impact_factors) / len(impact_factors)
        
        # Create color arrays based on values
        temp_colors = ['#FF6B6B' if temp > 30 else '#4ECDC4' if temp > 25 else '#45B7D1' for temp in temperatures]
        humidity_colors = ['#FF6347' if h > 80 else '#FFD700' if h > 60 else '#4ECDC4' for h in humidity]
        wind_colors = ['#FF6347' if w > 2.5 else '#FFD700' if w > 1.5 else '#45B7D1' for w in wind_speed]
        impact_colors = ['#90EE90' if i <= 1.1 else '#FFD700' if i <= 1.3 else '#FF6347' for i in impact_factors]
        
        html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ Jakarta Weather Forecast Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
        }}
        .data-table {{
            margin: 30px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .data-table h3 {{
            background: #667eea;
            color: white;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        .impact-low {{ color: #28a745; font-weight: bold; }}
        .impact-medium {{ color: #ffc107; font-weight: bold; }}
        .impact-high {{ color: #dc3545; font-weight: bold; }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌤️ Jakarta Weather Forecast Dashboard</h1>
            <p>24 Jam - Interval 3 Jam | Data Source: OpenWeatherMap API</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{avg_temp:.1f}°C</div>
                <div class="stat-label">Temperatur Rata-rata</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_humidity:.0f}%</div>
                <div class="stat-label">Kelembaban Rata-rata</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_wind:.1f} m/s</div>
                <div class="stat-label">Angin Rata-rata</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_impact:.2f}x</div>
                <div class="stat-label">Impact Factor Rata-rata</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">🌡️ Temperatur Jakarta</div>
                <canvas id="temperatureChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">💧 Kelembaban Jakarta</div>
                <canvas id="humidityChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">💨 Kecepatan Angin Jakarta</div>
                <canvas id="windChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">☁️ Tutupan Awan Jakarta</div>
                <canvas id="cloudsChart"></canvas>
            </div>
            
            <div class="chart-container full-width">
                <div class="chart-title">⚡ Weather Impact Factor</div>
                <canvas id="impactChart"></canvas>
            </div>
            
            <div class="chart-container full-width">
                <div class="chart-title">🌧️ Curah Hujan (3 Jam)</div>
                <canvas id="rainChart"></canvas>
            </div>
        </div>
        
        <div class="data-table">
            <h3>📊 Data Cuaca Detail</h3>
            <table>
                <thead>
                    <tr>
                        <th>Waktu</th>
                        <th>Suhu (°C)</th>
                        <th>Terasa (°C)</th>
                        <th>Kelembaban (%)</th>
                        <th>Angin (m/s)</th>
                        <th>Awan (%)</th>
                        <th>Hujan (mm)</th>
                        <th>Kondisi</th>
                        <th>Impact</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add table rows
        for i, data in enumerate(weather_data):
            impact_factor = impact_factors[i]
            impact_class = "impact-low" if impact_factor <= 1.1 else "impact-medium" if impact_factor <= 1.3 else "impact-high"
            
            html_content += f"""
                    <tr>
                        <td>{data['time_str']}</td>
                        <td>{data['temperature']:.1f}</td>
                        <td>{data['feels_like']:.1f}</td>
                        <td>{data['humidity']:.0f}</td>
                        <td>{data['wind_speed']:.1f}</td>
                        <td>{data['clouds']:.0f}</td>
                        <td>{data['rain_3h']:.1f}</td>
                        <td>{data['weather_description']}</td>
                        <td class="{impact_class}">{impact_factor:.2f}x</td>
                    </tr>
"""
        
        html_content += f"""
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Chart.js configuration
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#333';
        
        // Temperature Chart
        new Chart(document.getElementById('temperatureChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [
                    {{
                        label: 'Temperatur Aktual',
                        data: {json.dumps(temperatures)},
                        borderColor: '#FF6B6B',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }},
                    {{
                        label: 'Temperatur Terasa',
                        data: {json.dumps(feels_like)},
                        borderColor: '#FF8E53',
                        backgroundColor: 'rgba(255, 142, 83, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        title: {{
                            display: true,
                            text: 'Temperatur (°C)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Humidity Chart
        new Chart(document.getElementById('humidityChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Kelembaban',
                    data: {json.dumps(humidity)},
                    backgroundColor: {json.dumps(humidity_colors)},
                    borderColor: '#4ECDC4',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Kelembaban (%)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Wind Chart
        new Chart(document.getElementById('windChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [
                    {{
                        label: 'Kecepatan Angin',
                        data: {json.dumps(wind_speed)},
                        backgroundColor: {json.dumps(wind_colors)},
                        borderColor: '#45B7D1',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Angin Gust',
                        data: {json.dumps(wind_gust)},
                        backgroundColor: 'rgba(255, 107, 157, 0.7)',
                        borderColor: '#FF6B9D',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Kecepatan (m/s)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Clouds Chart
        new Chart(document.getElementById('cloudsChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Tutupan Awan',
                    data: {json.dumps(clouds)},
                    borderColor: '#FFEAA7',
                    backgroundColor: 'rgba(255, 234, 167, 0.3)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Tutupan Awan (%)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Impact Factor Chart
        new Chart(document.getElementById('impactChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Weather Impact Factor',
                    data: {json.dumps(impact_factors)},
                    backgroundColor: {json.dumps(impact_colors)},
                    borderColor: '#FF8C42',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            afterLabel: function(context) {{
                                return 'Kondisi: ' + {json.dumps(weather_descriptions)}[context.dataIndex];
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Impact Factor'
                        }}
                    }}
                }}
            }}
        }});
        
        // Rain Chart
        new Chart(document.getElementById('rainChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Curah Hujan (3h)',
                    data: {json.dumps(rain_3h)},
                    backgroundColor: '#DDA0DD',
                    borderColor: '#9370DB',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Curah Hujan (mm)'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        
        # Save HTML file
        with open('jakarta_weather_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Dashboard HTML tersimpan sebagai 'jakarta_weather_dashboard.html'")
        print("📝 Buka file tersebut di browser untuk melihat visualisasi interaktif")
        print("💡 Anda dapat menggunakan browser untuk mengkonversi ke PNG dengan Ctrl+P")

def main():
    print("🌤️ Jakarta Weather Data Visualization - HTML Export")
    print("=" * 60)
    
    # Buat visualizer
    visualizer = JakartaWeatherHTMLVisualizer()
    
    # Parse data
    print("🔍 Parsing weather data...")
    weather_data = visualizer.parse_weather_data(WEATHER_DATA)
    
    # Buat dashboard HTML
    print("📊 Membuat dashboard HTML...")
    visualizer.create_html_dashboard(weather_data)
    
    print("\n🎉 Visualisasi selesai!")
    print("📁 File yang dihasilkan:")
    print("  - jakarta_weather_dashboard.html (Dashboard interaktif)")
    print("\n💡 Cara menggunakan:")
    print("  1. Buka file 'jakarta_weather_dashboard.html' di browser")
    print("  2. Untuk export PNG: Ctrl+P → Save as PDF/PNG")
    print("  3. Atau screenshot langsung dari browser")

if __name__ == "__main__":
    main() 