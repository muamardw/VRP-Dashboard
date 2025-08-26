# Configuration file for VRP RL Project

# API Keys
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImNiYTQ2YzQyZjRkMTQzN2ZiZjhlYmQ4NWMyZjM5OWI3IiwiaCI6Im11cm11cjY0In0="
OPENWEATHER_API_KEY = "ec9a1e4e17acbc7681644f5b8f316236"

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000

# Traffic Factors
TRAFFIC_FACTORS = {
    "rain": 1.3,        # Hujan +30% waktu
    "wind": 1.2,        # Angin kencang +20% waktu
    "storm": 1.5,       # Badai +50% waktu
    "rush_hour": 1.4,   # Jam sibuk +40% waktu
    "distance": 1.2     # Jarak jauh +20% waktu
}

# Rush Hour Times (24-hour format)
RUSH_HOURS = [
    (7, 9),   # Pagi: 07:00-09:00
    (16, 19)  # Sore: 16:00-19:00
] 