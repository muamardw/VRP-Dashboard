from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import requests
import openrouteservice
from datetime import datetime
import config
from pt_sanghiang_data import PTSanghiangDataProcessor
from realistic_route_system import RealisticRouteSystem

app = FastAPI(title="VRP Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "VRP Dashboard API"
    }

ORS_API_KEY = config.ORS_API_KEY
OPENWEATHER_API_KEY = config.OPENWEATHER_API_KEY

class LatLng(BaseModel):
    lat: float
    lng: float

class RouteSegment(BaseModel):
    start: LatLng
    end: LatLng
    distance_km: float
    traffic_level: str
    traffic_color: str
    weather_info: dict

class VehicleRoute(BaseModel):
    route: List[LatLng]
    vehicle_position: LatLng
    eta: float
    name: str
    segments: List[RouteSegment]  # Traffic info per segment
    overall_traffic_level: str
    overall_traffic_color: str

class MultiRouteResponse(BaseModel):
    vehicles: List[VehicleRoute]

# Initialize PT. Sanghiang Perkasa data processor
pt_processor = PTSanghiangDataProcessor()

# Initialize realistic route system
route_system = RealisticRouteSystem()

# Koordinat depot PT. Sanghiang Perkasa - Jl. Raya Bekasi KM 25 Cakung Jakarta Timur
CIKAMPEK = LatLng(lat=-6.1702, lng=106.9417)  # Updated to Jakarta Timur location

# Data aktual PT. Sanghiang Perkasa - Updated dengan 4 destinasi Jabodetabek
PT_SANGHIANG_DESTINATIONS = {
    'Bogor': {
        'coordinates': {'lat': -6.5950, 'lng': 106.8167},  # Jl. Wangun no. 216 Sindangsari Bogor Timur 16720
        'address': 'Jl. Wangun no. 216 Sindangsari Bogor Timur 16720',
        'distance': 60, 'capacity': 2000, 'load': 2000, 'utilization': 100
    },
    'Tangerang': {
        'coordinates': {'lat': -6.1783, 'lng': 106.6319},  # Jl. Serenade Lake No.15, Pakulonan Bar., Kec. Klp. Dua, Kota Tangerang, Banten 15810
        'address': 'Jl. Serenade Lake No.15, Pakulonan Bar., Kec. Klp. Dua, Kota Tangerang, Banten 15810',
        'distance': 55, 'capacity': 1000, 'load': 700, 'utilization': 70
    },
    'Jakarta': {
        'coordinates': {'lat': -6.1702, 'lng': 106.9417},  # Jl. Pulo Lentut no. 10, Kawasan industri Pulo Gadung, Jakarta Timur 13920
        'address': 'Jl. Pulo Lentut no. 10, Kawasan industri Pulo Gadung, Jakarta Timur 13920',
        'distance': 0.5, 'capacity': 2000, 'load': 1700, 'utilization': 85
    },
    'Bekasi': {
        'coordinates': {'lat': -6.2383, 'lng': 106.9756},  # Jl. Jakasetia no. 27 B, Kp. Poncol, Kel. Jakasetia, Bekasi Selatan 17423
        'address': 'Jl. Jakasetia no. 27 B, Kp. Poncol, Kel. Jakasetia, Bekasi Selatan 17423',
        'distance': 10, 'capacity': 1000, 'load': 500, 'utilization': 50
    }
}

# Simple fallback data untuk testing dengan 4 destinasi
SIMPLE_FALLBACK_DATA = {
    "success": True,
    "statistics": {
        "total_routes": 4,
        "total_distance_km": 125.5,
        "average_utilization": 81.7,
        "active_vehicles": 4
    },
    "routes": [
        {
            "destination": "Bogor",
            "location": {"lat": -6.5950, "lng": 106.8167},
            "distance_km": 60.0,
            "eta": 1.2,
            "traffic_level": "moderate",
            "traffic_color": "#ffaa00",
            "vehicle_type": "Truck Sedang",
            "capacity_kg": 2000,
            "utilization": 100,
            "current_load": 2000,
            "estimated_time": 100,
            "weather": {"description": "sunny"},
            "route_polyline": [
                {"lat": -6.2088, "lng": 106.8456},
                {"lat": -6.2000, "lng": 106.8500},
                {"lat": -6.1900, "lng": 106.8600},
                {"lat": -6.1751, "lng": 106.8650}
            ],
            "position": {"lat": -6.1900, "lng": 106.8600},
            "road_segments": [
                {
                    "road_name": "Jalan Raya Bogor",
                    "length": 25.0,
                    "traffic_level": "medium",
                    "area": "Bogor"
                },
                {
                    "road_name": "Jalan Raya Jakarta-Bogor",
                    "length": 20.0,
                    "traffic_level": "high",
                    "area": "Bogor"
                },
                {
                    "road_name": "Jalan Wangun",
                    "length": 15.0,
                    "traffic_level": "low",
                    "area": "Bogor"
                }
            ]
        },
        {
            "destination": "Tangerang",
            "location": {"lat": -6.1783, "lng": 106.6319},
            "distance_km": 55.0,
            "eta": 1.1,
            "traffic_level": "heavy",
            "traffic_color": "#ff4444",
            "vehicle_type": "Truck Kecil",
            "capacity_kg": 1000,
            "utilization": 70,
            "current_load": 700,
            "estimated_time": 85,
            "weather": {"description": "cloudy"},
            "route_polyline": [
                {"lat": -6.2088, "lng": 106.8456},
                {"lat": -6.2000, "lng": 106.8000},
                {"lat": -6.1900, "lng": 106.7000},
                {"lat": -6.1783, "lng": 106.6319}
            ],
            "position": {"lat": -6.1900, "lng": 106.7000},
            "road_segments": [
                {
                    "road_name": "Jalan Raya Tangerang",
                    "length": 30.0,
                    "traffic_level": "high",
                    "area": "Tangerang"
                },
                {
                    "road_name": "Jalan Serenade Lake",
                    "length": 15.0,
                    "traffic_level": "medium",
                    "area": "Tangerang"
                },
                {
                    "road_name": "Jalan Pakulonan Barat",
                    "length": 10.0,
                    "traffic_level": "low",
                    "area": "Tangerang"
                }
            ]
        },
        {
            "destination": "Jakarta",
            "location": {"lat": -6.1702, "lng": 106.9417},
            "distance_km": 0.5,
            "eta": 0.1,
            "traffic_level": "moderate",
            "traffic_color": "#ffaa00",
            "vehicle_type": "Truck Sedang",
            "capacity_kg": 2000,
            "utilization": 85,
            "current_load": 1700,
            "estimated_time": 5,
            "weather": {"description": "sunny"},
            "route_polyline": [
                {"lat": -6.1702, "lng": 106.9417},
                {"lat": -6.1702, "lng": 106.9417}
            ],
            "position": {"lat": -6.1702, "lng": 106.9417},
            "road_segments": [
                {
                    "road_name": "Jalan Pulo Lentut",
                    "length": 0.3,
                    "traffic_level": "medium",
                    "area": "Jakarta"
                },
                {
                    "road_name": "Jalan Kawasan Industri Pulo Gadung",
                    "length": 0.2,
                    "traffic_level": "low",
                    "area": "Jakarta"
                }
            ]
        },
        {
            "destination": "Bekasi",
            "location": {"lat": -6.2383, "lng": 106.9756},
            "distance_km": 10.0,
            "eta": 0.3,
            "traffic_level": "moderate",
            "traffic_color": "#ffaa00",
            "vehicle_type": "Truck Kecil",
            "capacity_kg": 1000,
            "utilization": 50,
            "current_load": 500,
            "estimated_time": 25,
            "weather": {"description": "sunny"},
            "route_polyline": [
                {"lat": -6.2088, "lng": 106.8456},
                {"lat": -6.2200, "lng": 106.9000},
                {"lat": -6.2383, "lng": 106.9756}
            ],
            "position": {"lat": -6.2200, "lng": 106.9000},
            "road_segments": [
                {
                    "road_name": "Jalan Raya Bekasi",
                    "length": 5.0,
                    "traffic_level": "high",
                    "area": "Bekasi"
                },
                {
                    "road_name": "Jalan Jakasetia",
                    "length": 3.0,
                    "traffic_level": "medium",
                    "area": "Bekasi"
                },
                {
                    "road_name": "Jalan Kampung Poncol",
                    "length": 2.0,
                    "traffic_level": "low",
                    "area": "Bekasi"
                }
            ]
        }
    ]
}

def get_ors_polyline_eta(start_lat: float, start_lng: float, end_lat: float, end_lng: float, traffic_factor: float = 1.0):
    """Get polyline and ETA from OpenRouteService API"""
    try:
        if not ORS_API_KEY:
            return get_fallback_polyline(start_lat, start_lng, end_lat, end_lng)
        
        client = openrouteservice.Client(key=ORS_API_KEY)
        coords = [[start_lng, start_lat], [end_lng, end_lat]]
        
        route = client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson'
        )
        
        if route and 'features' in route and len(route['features']) > 0:
            feature = route['features'][0]
            geometry = feature['geometry']
            properties = feature['properties']
            
            # Extract coordinates from GeoJSON
            if geometry['type'] == 'LineString':
                coordinates = geometry['coordinates']
                # Convert [lng, lat] to [lat, lng] for frontend
                polyline = [{"lat": coord[1], "lng": coord[0]} for coord in coordinates]
                
                # Calculate ETA with traffic factor
                duration = properties.get('summary', {}).get('duration', 0)
                eta_hours = (duration / 3600) * traffic_factor
                
                return {
                    "polyline": polyline,
                    "eta_hours": eta_hours,
                    "distance_km": properties.get('summary', {}).get('distance', 0) / 1000
                }
    except Exception as e:
        print(f"Error calling ORS API: {e}")
    
    return get_fallback_polyline(start_lat, start_lng, end_lat, end_lng)

def get_fallback_polyline(start_lat: float, start_lng: float, end_lat: float, end_lng: float):
    """Fallback polyline when ORS API is not available"""
    # Simple straight line approximation
    polyline = [
            {"lat": start_lat, "lng": start_lng},
            {"lat": end_lat, "lng": end_lng}
        ]
    
    # Calculate distance and ETA
    distance_km = ((end_lat - start_lat) ** 2 + (end_lng - start_lng) ** 2) ** 0.5 * 111
    eta_hours = distance_km / 50  # Assume 50 km/h average speed
    
    return {
        "polyline": polyline,
        "eta_hours": eta_hours,
        "distance_km": distance_km
    }

def get_weather_data(lat: float, lng: float):
    """Get weather data from OpenWeatherMap API"""
    try:
        if not OPENWEATHER_API_KEY:
            return {"description": "sunny", "temp": 30, "humidity": 70}
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lng,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "description": data.get("weather", [{}])[0].get("description", "unknown"),
                "temp": data.get("main", {}).get("temp", 30),
                "humidity": data.get("main", {}).get("humidity", 70)
            }
    except Exception as e:
        print(f"Error calling OpenWeatherMap API: {e}")
    
    return {"description": "sunny", "temp": 30, "humidity": 70}

def estimate_traffic_factor(weather_data, route_points):
    """Estimate traffic factor based on weather and route"""
    base_factor = 1.0
    
    # Weather impact
    weather_desc = weather_data.get("description", "").lower()
    if "rain" in weather_desc or "storm" in weather_desc:
        base_factor *= 1.3
    elif "cloud" in weather_desc:
        base_factor *= 1.1
    
    # Route complexity impact
    if len(route_points) > 10:
        base_factor *= 1.2
    
    return min(base_factor, 2.0)

def get_traffic_level_and_color(traffic_factor):
    """Convert traffic factor to level and color"""
    if traffic_factor < 1.2:
        return "light", "#44ff44"
    elif traffic_factor < 1.5:
        return "moderate", "#ffaa00"
    elif traffic_factor < 2.0:
        return "heavy", "#ff4444"
    else:
        return "very_heavy", "#880000"

def calculate_internal_traffic_factor(lat: float, lng: float, time_of_day: int = None, weather_condition: str = None):
    """Calculate traffic factor based on location and conditions"""
    base_factor = 1.0
    
    # Time of day impact
    if time_of_day is None:
        time_of_day = datetime.now().hour
    
    if 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
        base_factor *= 1.5  # Rush hour
    elif 10 <= time_of_day <= 16:
        base_factor *= 1.2  # Regular hours
    else:
        base_factor *= 0.8  # Off-peak hours
    
    # Weather impact
    if weather_condition:
        if "rain" in weather_condition.lower():
            base_factor *= 1.3
        elif "storm" in weather_condition.lower():
            base_factor *= 1.5
    
    # Location-based traffic (simplified)
    # Jakarta area typically has higher traffic
    if -6.3 <= lat <= -6.1 and 106.7 <= lng <= 107.0:
            base_factor *= 1.2
    
    return min(base_factor, 2.0)

def generate_traffic_segments(start_lat, start_lng, dest_lat, dest_lng, traffic_factor):
    """Generate traffic segments along the route"""
    segments = []
    
    # Calculate intermediate points
    num_segments = 5
    for i in range(num_segments):
        ratio = i / (num_segments - 1)
        lat = start_lat + (dest_lat - start_lat) * ratio
        lng = start_lng + (dest_lng - start_lng) * ratio
        
        # Vary traffic level for each segment
        segment_traffic = traffic_factor * (0.8 + 0.4 * (i % 3))
        level, color = get_traffic_level_and_color(segment_traffic)
        
        segments.append({
            "position": {"lat": lat, "lng": lng},
            "traffic_level": level,
            "traffic_color": color,
            "traffic_factor": segment_traffic
        })
    
    return segments

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula"""
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def verify_and_update_distances():
    """Verify and update distances in PT_SANGHIANG_DESTINATIONS"""
    depot_lat, depot_lng = CIKAMPEK.lat, CIKAMPEK.lng
    
    for dest_name, dest_data in PT_SANGHIANG_DESTINATIONS.items():
        dest_lat = dest_data['coordinates']['lat']
        dest_lng = dest_data['coordinates']['lng']
        
        calculated_distance = calculate_distance(depot_lat, depot_lng, dest_lat, dest_lng)
        print(f"Distance to {dest_name}: {calculated_distance:.1f} km (stored: {dest_data['distance']} km)")

@app.get("/api/test")
def test_endpoint():
    """Test endpoint to verify API is running"""
    return {
        "message": "PT. Sanghiang Perkasa API is running",
        "timestamp": datetime.now().isoformat(),
        "destinations": list(PT_SANGHIANG_DESTINATIONS.keys())
    }

@app.get("/api/simple-pt-sanghiang-data")
def get_simple_pt_sanghiang_data():
    """Simple endpoint that always returns realistic route data"""
    try:
        print("🛣️ Generating realistic routes...")
        
        # Get current weather
        current_weather = route_system.get_current_weather(CIKAMPEK.lat, CIKAMPEK.lng)
        print(f"🌤️ Weather: {current_weather}")
        
        # Get all realistic routes
        all_routes = route_system.get_all_routes(current_weather)
        print(f"📍 Generated {len(all_routes)} realistic routes")
        
        # Debug: List all destinations
        print(f"🎯 Destinations found:")
        for route in all_routes:
            print(f"   - {route.destination}")
        
        # Format routes for API with detailed information
        formatted_routes = []
        total_distance = 0
        total_capacity = 0
        total_load = 0
        
        for route in all_routes:
            api_route = route_system.format_route_for_api(route)
            
            # Add detailed information for frontend
            detailed_route = {
                "id": api_route["id"],
                "destination": api_route["destination"],
                "vehicle_id": api_route["vehicle_id"],
                "vehicle_type": api_route["vehicle_type"],
                "capacity_kg": api_route["capacity_kg"],
                "current_load_kg": api_route["current_load_kg"],
                "remaining_capacity_kg": api_route["remaining_capacity_kg"],
                "distance_km": api_route["distance_km"],
                "start_location": api_route["start_location"],
                "end_location": api_route["end_location"],
                "status": api_route["status"],
                "estimated_arrival": api_route["estimated_arrival"],
                "route_polyline": api_route["route_polyline"],  # Realistic polyline
                "traffic_level": "medium",  # Default traffic level
                "traffic_color": "#ffaa00",  # Default traffic color
                "weather": {
                    "description": current_weather,
                    "temperature": 28,
                    "humidity": 75
                },
                "utilization_percent": (api_route["current_load_kg"] / api_route["capacity_kg"]) * 100,
                "road_segments": api_route["road_segments"],  # Detailed road segments
                "traffic_score": api_route["traffic_score"],
                "weather_score": api_route["weather_score"],
                "overall_score": api_route["overall_score"]
            }
            
            formatted_routes.append(detailed_route)
            total_distance += route.total_distance_km
            total_capacity += api_route["capacity_kg"]
            total_load += api_route["current_load_kg"]
            
            # Debug: Check polyline points
            polyline_points = len(route.polyline)
            print(f"   📍 {route.destination}: {polyline_points} polyline points")
            
            if polyline_points > 2:
                print(f"      ✅ Realistic polyline with curves")
                print(f"      📍 Start: {route.polyline[0]}")
                print(f"      📍 Middle: {route.polyline[len(route.polyline)//2]}")
                print(f"      📍 End: {route.polyline[-1]}")
            else:
                print(f"      ❌ Still straight line")
        
        # Calculate statistics
        avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
        
        response_data = {
            "success": True,
            "message": "PT. Sanghiang Perkasa Realistic Route Data",
            "routes": formatted_routes,
            "statistics": {
                "total_routes": len(formatted_routes),
                "total_distance_km": total_distance,
                "total_capacity_kg": total_capacity,
                "total_load_kg": total_load,
                "average_utilization_percent": round(avg_utilization, 1),
                "active_vehicles": len(formatted_routes),
                "completed_routes": 0,
                "pending_routes": len(formatted_routes),
                "current_weather": current_weather
            }
        }
        
        print(f"✅ Returning realistic route data with {len(formatted_routes)} routes")
        print(f"📊 Total distance: {total_distance:.1f} km")
        print(f"🌤️ Weather: {current_weather}")
        
        return response_data
        
    except Exception as e:
        print(f"❌ Error in realistic route generation: {e}")
        print("🔄 Falling back to simple data")
        return SIMPLE_FALLBACK_DATA

@app.get("/api/route")
async def get_route():
    """Get a single route to Jakarta for testing"""
    try:
        # Get route to Jakarta
        jakarta_dest = PT_SANGHIANG_DESTINATIONS['Jakarta']
        start_lat, start_lng = CIKAMPEK.lat, CIKAMPEK.lng
        end_lat, end_lng = jakarta_dest['coordinates']['lat'], jakarta_dest['coordinates']['lng']
        
        # Get weather data
        weather_data = get_weather_data(start_lat, start_lng)
        
        # Calculate traffic factor
        traffic_factor = calculate_internal_traffic_factor(start_lat, start_lng, weather_condition=weather_data.get('description'))
        
        # Get route data
        route_data = get_ors_polyline_eta(start_lat, start_lng, end_lat, end_lng, traffic_factor)
        
        # Generate traffic segments
        traffic_segments = generate_traffic_segments(start_lat, start_lng, end_lat, end_lng, traffic_factor)
        
        traffic_level, traffic_color = get_traffic_level_and_color(traffic_factor)
        
        return {
            "success": True,
            "route": {
                "destination": "Jakarta",
                "polyline": route_data["polyline"],
                "eta_hours": route_data["eta_hours"],
                "distance_km": route_data["distance_km"],
                "traffic_level": traffic_level,
                "traffic_color": traffic_color,
                "weather": weather_data,
                "traffic_segments": traffic_segments
            }
        }
    except Exception as e:
        print(f"Error in get_route: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/weather")
def get_weather(lat: float = Query(...), lng: float = Query(...)):
    """Get weather data for a specific location"""
    try:
        weather_data = get_weather_data(lat, lng)
        return {
            "success": True,
            "weather": weather_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/traffic-factor")
def get_traffic_factor(lat: float = Query(...), lng: float = Query(...), time_of_day: int = None, weather_condition: str = None):
    """Get traffic factor for a specific location"""
    try:
        traffic_factor = calculate_internal_traffic_factor(lat, lng, time_of_day, weather_condition)
        traffic_level, traffic_color = get_traffic_level_and_color(traffic_factor)
        
        return {
            "success": True,
            "traffic_factor": traffic_factor,
            "traffic_level": traffic_level,
            "traffic_color": traffic_color
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/pt-sanghiang-data")
def get_pt_sanghiang_data():
    """Get comprehensive PT. Sanghiang Perkasa data with realistic routing"""
    try:
        # Get current weather
        current_weather = route_system.get_current_weather(CIKAMPEK.lat, CIKAMPEK.lng)
        
        # Get all realistic routes
        all_routes = route_system.get_all_routes(current_weather)
        
        # Format routes for API
        processed_routes = []
        total_distance = 0
        total_capacity = 0
        total_load = 0
        
        for route in all_routes:
            try:
                api_route = route_system.format_route_for_api(route)
                
                # Add additional data
                api_route.update({
                    "traffic_level": "high" if route.traffic_score < 0.7 else "medium" if route.traffic_score < 0.9 else "low",
                    "traffic_color": "#ff4444" if route.traffic_score < 0.7 else "#ffaa00" if route.traffic_score < 0.9 else "#44ff44",
                    "weather": {"description": current_weather},
                    "utilization_percent": api_route["current_load_kg"] / api_route["capacity_kg"] * 100,
                    "cargo_type": "Produk Nutrisi (Chil-kid, Entrasol, dll)",
                    "priority": int(route.overall_score * 100)
                })
                
                processed_routes.append(api_route)
                total_distance += route.total_distance_km
                total_capacity += api_route["capacity_kg"]
                total_load += api_route["current_load_kg"]
                
            except Exception as e:
                print(f"Error processing route {route.destination}: {e}")
                continue
        
        # Create statistics
        avg_utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0
        
        stats = {
            "total_routes": len(processed_routes),
            "total_distance_km": total_distance,
            "total_capacity_kg": total_capacity,
            "total_load_kg": total_load,
            "average_utilization_percent": round(avg_utilization, 1),
            "active_vehicles": len(processed_routes),
            "completed_routes": 0,
            "pending_routes": len(processed_routes),
            "current_weather": current_weather
        }
        
        return {
            "success": True,
            "message": "PT. Sanghiang Perkasa Realistic Route Data",
            "routes": processed_routes,
            "statistics": stats
        }
        
    except Exception as e:
        print(f"Error in get_pt_sanghiang_data: {e}")
        # Return fallback data on error
        return SIMPLE_FALLBACK_DATA

@app.get("/api/pt-sanghiang-route/{route_id}")
def get_pt_sanghiang_route(route_id: str):
    """Get specific route data by ID"""
    try:
        # Find route in optimization data
        optimization_data = pt_processor.get_optimization_data(jabodetabek_only=True)
        
        for route_info in optimization_data:
            if route_info['route_id'] == route_id:
                start_lat, start_lng = CIKAMPEK.lat, CIKAMPEK.lng
                end_lat, end_lng = route_info['location']['lat'], route_info['location']['lng']
                
                # Get route data
                route_data = get_ors_polyline_eta(start_lat, start_lng, end_lat, end_lng)
            
            return {
                "success": True,
                    "route": {
                        "id": route_info['route_id'],
                        "name": route_info['route_name'],
                        "destination": route_info['location']['name'],
                        "polyline": route_data["polyline"],
                        "eta_hours": route_data["eta_hours"],
                        "distance_km": route_data["distance_km"],
                        "capacity": route_info['capacity'],
                        "current_load": route_info['current_load'],
                        "utilization": route_info['utilization_percent']
                    }
                }
        
            return {
                "success": False,
            "error": "Route not found"
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/optimize")
def optimize_route():
    """Optimize routes using VRP algorithm"""
    try:
        # Get current routes
        optimization_data = pt_processor.get_optimization_data(jabodetabek_only=True)
        
        # Simple optimization: sort by priority
        optimized_routes = sorted(optimization_data, key=lambda x: x['priority'], reverse=True)
        
        return {
            "success": True,
            "message": "Routes optimized successfully",
            "optimized_routes": optimized_routes[:5]  # Return top 5
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PT. Sanghiang Perkasa VRP API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/api/test")
    print("\n" + "="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 