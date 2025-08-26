#!/bin/bash

# Script untuk mengambil data cuaca dari OpenWeatherMap API menggunakan cURL
# Ganti YOUR_API_KEY dengan API key Anda

API_KEY="ec9a1e4e17acbc7681644f5b8f316236"

echo "🌤️ Mengambil data cuaca dari OpenWeatherMap API"
echo "=================================================="

# 1. Current Weather - Jakarta
echo "📡 Mengambil data cuaca saat ini untuk Jakarta..."
curl -X GET "https://api.openweathermap.org/data/2.5/weather?q=Jakarta,ID&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o jakarta_current_weather.json

echo "✅ Data Jakarta disimpan ke jakarta_current_weather.json"
echo ""

# 2. Current Weather - Bogor
echo "📡 Mengambil data cuaca saat ini untuk Bogor..."
curl -X GET "https://api.openweathermap.org/data/2.5/weather?q=Bogor,ID&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o bogor_current_weather.json

echo "✅ Data Bogor disimpan ke bogor_current_weather.json"
echo ""

# 3. Current Weather - Tangerang
echo "📡 Mengambil data cuaca saat ini untuk Tangerang..."
curl -X GET "https://api.openweathermap.org/data/2.5/weather?q=Tangerang,ID&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o tangerang_current_weather.json

echo "✅ Data Tangerang disimpan ke tangerang_current_weather.json"
echo ""

# 4. Current Weather - Bekasi
echo "📡 Mengambil data cuaca saat ini untuk Bekasi..."
curl -X GET "https://api.openweathermap.org/data/2.5/weather?q=Bekasi,ID&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o bekasi_current_weather.json

echo "✅ Data Bekasi disimpan ke bekasi_current_weather.json"
echo ""

# 5. Forecast - Jakarta (5 hari)
echo "🔮 Mengambil data forecast 5 hari untuk Jakarta..."
curl -X GET "https://api.openweathermap.org/data/2.5/forecast?q=Jakarta,ID&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o jakarta_forecast.json

echo "✅ Forecast Jakarta disimpan ke jakarta_forecast.json"
echo ""

# 6. Weather by Coordinates - Jakarta
echo "📍 Mengambil data cuaca berdasarkan koordinat Jakarta..."
curl -X GET "https://api.openweathermap.org/data/2.5/weather?lat=-6.2088&lon=106.8456&appid=$API_KEY&units=metric&lang=id" \
  -H "Accept: application/json" \
  -o jakarta_coordinates_weather.json

echo "✅ Data Jakarta (koordinat) disimpan ke jakarta_coordinates_weather.json"
echo ""

echo "🎉 Semua data cuaca berhasil diambil!"
echo "📁 File yang dibuat:"
echo "   - jakarta_current_weather.json"
echo "   - bogor_current_weather.json"
echo "   - tangerang_current_weather.json"
echo "   - bekasi_current_weather.json"
echo "   - jakarta_forecast.json"
echo "   - jakarta_coordinates_weather.json" 