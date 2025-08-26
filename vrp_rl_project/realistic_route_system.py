#!/usr/bin/env python3
"""
Realistic Route System - PT. Sanghiang Perkasa VRP
Sistem routing yang realistis mengikuti jalan yang ada di maps
dengan pertimbangan traffic dan cuaca untuk memilih rute terbaik
"""

import requests
import json
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
import math

@dataclass
class RoadSegment:
    """Representasi segmen jalan"""
    road_name: str
    start_coords: Tuple[float, float]
    end_coords: Tuple[float, float]
    length_km: float
    traffic_level: str
    weather_impact: str
    area: str
    estimated_time_minutes: int

@dataclass
class RouteOption:
    """Opsi rute dengan pertimbangan traffic dan cuaca"""
    route_id: str
    destination: str
    total_distance_km: float
    total_time_minutes: int
    traffic_score: float
    weather_score: float
    overall_score: float
    road_segments: List[RoadSegment]
    polyline: List[Dict[str, float]]

class RealisticRouteSystem:
    """Sistem routing realistis untuk PT. Sanghiang Perkasa"""
    
    def __init__(self):
        self.jakarta_roads = self._load_jakarta_roads()
        self.weather_conditions = self._load_weather_conditions()
        self.traffic_conditions = self._load_traffic_conditions()
        self.destinations = self._load_destinations()
        
    def _load_jakarta_roads(self) -> Dict[str, List[Dict]]:
        """Load database jalan Jakarta yang realistis"""
        return {
            "jakarta_pusat": [
                {
                    "name": "Jalan Sudirman",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.1900, 106.8234),
                    "length": 3.2,
                    "traffic_pattern": "high",
                    "area": "Jakarta Pusat"
                },
                {
                    "name": "Jalan Thamrin",
                    "start": (-6.1900, 106.8234),
                    "end": (-6.1751, 106.8650),
                    "length": 2.8,
                    "traffic_pattern": "very_high",
                    "area": "Jakarta Pusat"
                },
                {
                    "name": "Jalan Gatot Subroto",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.2146, 106.8451),
                    "length": 4.1,
                    "traffic_pattern": "high",
                    "area": "Jakarta Selatan"
                },
                {
                    "name": "Jalan TB Simatupang",
                    "start": (-6.2146, 106.8451),
                    "end": (-6.2297, 106.7997),
                    "length": 5.2,
                    "traffic_pattern": "medium",
                    "area": "Jakarta Selatan"
                },
                {
                    "name": "Jalan Casablanca",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.2200, 106.7900),
                    "length": 3.8,
                    "traffic_pattern": "high",
                    "area": "Jakarta Selatan"
                },
                {
                    "name": "Jalan Wolter Monginsidi",
                    "start": (-6.2200, 106.7900),
                    "end": (-6.2300, 106.7800),
                    "length": 2.5,
                    "traffic_pattern": "medium",
                    "area": "Jakarta Selatan"
                }
            ],
            "jakarta_timur": [
                {
                    "name": "Jalan Raya Bekasi",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.2200, 106.9000),
                    "length": 4.5,
                    "traffic_pattern": "high",
                    "area": "Jakarta Timur"
                },
                {
                    "name": "Jalan Raya Bogor",
                    "start": (-6.2200, 106.9000),
                    "end": (-6.2383, 106.9756),
                    "length": 6.2,
                    "traffic_pattern": "medium",
                    "area": "Bekasi"
                },
                {
                    "name": "Jalan Raya Cililitan",
                    "start": (-6.2200, 106.9000),
                    "end": (-6.2297, 106.7997),
                    "length": 5.1,
                    "traffic_pattern": "low",
                    "area": "Jakarta Timur"
                },
                {
                    "name": "Jalan Raya Pondok Gede",
                    "start": (-6.2383, 106.9756),
                    "end": (-6.2500, 107.0000),
                    "length": 4.0,
                    "traffic_pattern": "medium",
                    "area": "Bekasi"
                },
                {
                    "name": "Jalan Raya Cibubur",
                    "start": (-6.2500, 107.0000),
                    "end": (-6.2700, 107.0200),
                    "length": 3.5,
                    "traffic_pattern": "low",
                    "area": "Bekasi"
                }
            ],
            "bogor_route": [
                {
                    "name": "Jalan Raya Jakarta-Bogor",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.3000, 106.8500),
                    "length": 15.0,
                    "traffic_pattern": "high",
                    "area": "Jakarta-Bogor"
                },
                {
                    "name": "Jalan Raya Bogor",
                    "start": (-6.3000, 106.8500),
                    "end": (-6.4500, 106.8300),
                    "length": 25.0,
                    "traffic_pattern": "medium",
                    "area": "Bogor"
                },
                {
                    "name": "Jalan Wangun",
                    "start": (-6.4500, 106.8300),
                    "end": (-6.5950, 106.8167),
                    "length": 20.0,
                    "traffic_pattern": "low",
                    "area": "Bogor"
                },
                {
                    "name": "Jalan Siliwangi",
                    "start": (-6.5950, 106.8167),
                    "end": (-6.6000, 106.8000),
                    "length": 2.5,
                    "traffic_pattern": "low",
                    "area": "Bogor"
                },
                {
                    "name": "Gang Siliwangi",
                    "start": (-6.6000, 106.8000),
                    "end": (-6.5950, 106.8167),
                    "length": 1.8,
                    "traffic_pattern": "low",
                    "area": "Bogor"
                }
            ],
            "tangerang_route": [
                {
                    "name": "Jalan Raya Tangerang",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.2000, 106.8000),
                    "length": 30.0,
                    "traffic_pattern": "high",
                    "area": "Tangerang"
                },
                {
                    "name": "Jalan Serenade Lake",
                    "start": (-6.2000, 106.8000),
                    "end": (-6.1800, 106.7500),
                    "length": 8.0,
                    "traffic_pattern": "medium",
                    "area": "Tangerang"
                },
                {
                    "name": "Jalan Raya Serpong",
                    "start": (-6.1800, 106.7500),
                    "end": (-6.1500, 106.7000),
                    "length": 12.0,
                    "traffic_pattern": "medium",
                    "area": "Tangerang"
                },
                {
                    "name": "Jalan Raya BSD",
                    "start": (-6.1500, 106.7000),
                    "end": (-6.1200, 106.6500),
                    "length": 10.0,
                    "traffic_pattern": "low",
                    "area": "Tangerang"
                },
                {
                    "name": "Gang BSD Utama",
                    "start": (-6.1200, 106.6500),
                    "end": (-6.1100, 106.6400),
                    "length": 2.0,
                    "traffic_pattern": "low",
                    "area": "Tangerang"
                }
            ],
            "bekasi_route": [
                {
                    "name": "Jalan Raya Bekasi",
                    "start": (-6.2088, 106.8456),
                    "end": (-6.2200, 106.9000),
                    "length": 4.5,
                    "traffic_pattern": "high",
                    "area": "Bekasi"
                },
                {
                    "name": "Jalan Raya Pondok Gede",
                    "start": (-6.2200, 106.9000),
                    "end": (-6.2500, 107.0000),
                    "length": 8.0,
                    "traffic_pattern": "medium",
                    "area": "Bekasi"
                },
                {
                    "name": "Jalan Raya Cibubur",
                    "start": (-6.2500, 107.0000),
                    "end": (-6.2700, 107.0200),
                    "length": 3.5,
                    "traffic_pattern": "low",
                    "area": "Bekasi"
                },
                {
                    "name": "Jalan Raya Cikarang",
                    "start": (-6.2700, 107.0200),
                    "end": (-6.3000, 107.0500),
                    "length": 6.0,
                    "traffic_pattern": "medium",
                    "area": "Bekasi"
                },
                {
                    "name": "Gang Cikarang Baru",
                    "start": (-6.3000, 107.0500),
                    "end": (-6.3100, 107.0600),
                    "length": 2.5,
                    "traffic_pattern": "low",
                    "area": "Bekasi"
                }
            ]
        }
    
    def _load_weather_conditions(self) -> Dict[str, Dict]:
        """Load kondisi cuaca yang mempengaruhi rute"""
        return {
            "sunny": {
                "traffic_impact": 1.0,
                "speed_factor": 1.0,
                "description": "Cerah"
            },
            "cloudy": {
                "traffic_impact": 1.1,
                "speed_factor": 0.95,
                "description": "Berawan"
            },
            "rain": {
                "traffic_impact": 1.3,
                "speed_factor": 0.8,
                "description": "Hujan"
            },
            "heavy_rain": {
                "traffic_impact": 1.5,
                "speed_factor": 0.6,
                "description": "Hujan Lebat"
            },
            "storm": {
                "traffic_impact": 1.8,
                "speed_factor": 0.4,
                "description": "Badai"
            }
        }
    
    def _load_traffic_conditions(self) -> Dict[str, Dict]:
        """Load kondisi lalu lintas"""
        return {
            "low": {
                "speed_factor": 1.0,
                "delay_minutes": 0,
                "color": "#44ff44"
            },
            "medium": {
                "speed_factor": 0.8,
                "delay_minutes": 5,
                "color": "#ffaa00"
            },
            "high": {
                "speed_factor": 0.6,
                "delay_minutes": 15,
                "color": "#ff4444"
            },
            "very_high": {
                "speed_factor": 0.4,
                "delay_minutes": 30,
                "color": "#880000"
            }
        }
    
    def _load_destinations(self) -> Dict[str, Dict]:
        """Load destinasi PT. Sanghiang Perkasa"""
        return {
            "bogor": {
                "name": "Bogor",
                "coordinates": (-6.5950, 106.8167),
                "route_key": "bogor_route"
            },
            "tangerang": {
                "name": "Tangerang", 
                "coordinates": (-6.1783, 106.6319),
                "route_key": "tangerang_route"
            },
            "jakarta": {
                "name": "Jakarta",
                "coordinates": (-6.1702, 106.9417),
                "route_key": "jakarta_pusat"  # Fixed: was "jakarta_local"
            },
            "bekasi": {
                "name": "Bekasi",
                "coordinates": (-6.2383, 106.9756),
                "route_key": "bekasi_route"
            }
        }
    
    def get_current_weather(self, lat: float, lng: float) -> str:
        """Get current weather condition (simulated)"""
        # Simulate weather based on time and location
        hour = datetime.now().hour
        
        if 6 <= hour <= 18:  # Daytime
            weather_options = ["sunny", "cloudy", "rain"]
            weights = [0.6, 0.3, 0.1]
        else:  # Nighttime
            weather_options = ["cloudy", "rain", "heavy_rain"]
            weights = [0.5, 0.3, 0.2]
        
        return random.choices(weather_options, weights=weights)[0]
    
    def get_current_traffic(self, road_name: str, area: str, time_of_day: int = None) -> str:
        """Get current traffic condition based on road and time"""
        if time_of_day is None:
            time_of_day = datetime.now().hour
        
        # Traffic patterns based on time and road type
        if "Sudirman" in road_name or "Thamrin" in road_name:
            if 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
                return "very_high"
            elif 10 <= time_of_day <= 16:
                return "high"
            else:
                return "medium"
        
        elif "Bekasi" in road_name or "Tangerang" in road_name:
            if 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
                return "high"
            else:
                return "medium"
        
        elif "Bogor" in road_name:
            if 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
                return "high"
            else:
                return "low"
        
        else:
            if 7 <= time_of_day <= 9 or 17 <= time_of_day <= 19:
                return "medium"
            else:
                return "low"
    
    def calculate_route_score(self, route_segments: List[RoadSegment], weather: str) -> float:
        """Calculate overall route score based on traffic and weather"""
        total_score = 0
        total_segments = len(route_segments)
        
        for segment in route_segments:
            # Traffic score
            traffic_score = {
                "low": 1.0,
                "medium": 0.8,
                "high": 0.6,
                "very_high": 0.4
            }.get(segment.traffic_level, 1.0)
            
            # Weather impact
            weather_impact = self.weather_conditions[weather]["traffic_impact"]
            
            # Segment score
            segment_score = traffic_score * weather_impact
            total_score += segment_score
        
        return total_score / total_segments
    
    def generate_realistic_route(self, destination: str, weather: str = None) -> RouteOption:
        """Generate realistic route following actual roads"""
        if destination not in self.destinations:
            raise ValueError(f"Destination {destination} not found")
        
        dest_info = self.destinations[destination]
        route_key = dest_info["route_key"]
        
        if weather is None:
            weather = self.get_current_weather(*dest_info["coordinates"])
        
        # Get road segments for this route
        road_data = self.jakarta_roads[route_key]
        route_segments = []
        polyline_points = []
        
        total_distance = 0
        total_time = 0
        
        for i, road in enumerate(road_data):
            # Get current traffic for this road
            current_traffic = self.get_current_traffic(road["name"], road["area"])
            
            # Calculate time with traffic and weather impact
            base_time = road["length"] * 2  # 2 minutes per km base
            traffic_factor = self.traffic_conditions[current_traffic]["speed_factor"]
            weather_factor = self.weather_conditions[weather]["speed_factor"]
            
            estimated_time = int(base_time / (traffic_factor * weather_factor))
            
            # Create road segment
            segment = RoadSegment(
                road_name=road["name"],
                start_coords=road["start"],
                end_coords=road["end"],
                length_km=road["length"],
                traffic_level=current_traffic,
                weather_impact=weather,
                area=road["area"],
                estimated_time_minutes=estimated_time
            )
            
            route_segments.append(segment)
            total_distance += road["length"]
            total_time += estimated_time
            
            # Add polyline points with intermediate points for realistic curves
            polyline_points.extend(self._generate_road_polyline(road["start"], road["end"], road["name"]))
        
        # Calculate route score
        route_score = self.calculate_route_score(route_segments, weather)
        
        return RouteOption(
            route_id=f"route_{destination}",
            destination=dest_info["name"],
            total_distance_km=total_distance,
            total_time_minutes=total_time,
            traffic_score=1.0 - (sum(1 for s in route_segments if s.traffic_level in ["high", "very_high"]) / len(route_segments)),
            weather_score=1.0 / self.weather_conditions[weather]["traffic_impact"],
            overall_score=route_score,
            road_segments=route_segments,
            polyline=polyline_points
        )
    
    def get_optimal_route(self, destination: str, weather: str = None) -> RouteOption:
        """Get optimal route considering traffic and weather"""
        return self.generate_realistic_route(destination, weather)
    
    def get_all_routes(self, weather: str = None) -> List[RouteOption]:
        """Get all routes for all destinations"""
        routes = []
        for dest_key in self.destinations.keys():
            try:
                route = self.get_optimal_route(dest_key, weather)
                routes.append(route)
            except Exception as e:
                print(f"Error generating route for {dest_key}: {e}")
                continue
        
        return routes
    
    def _generate_road_polyline(self, start_coords: Tuple[float, float], end_coords: Tuple[float, float], road_name: str) -> List[Dict[str, float]]:
        """Generate realistic polyline points that follow actual road curves"""
        points = []
        
        # Calculate distance between points
        lat_diff = end_coords[0] - start_coords[0]
        lng_diff = end_coords[1] - start_coords[1]
        distance = math.sqrt(lat_diff**2 + lng_diff**2)
        
        # Number of intermediate points based on road length - MORE POINTS!
        num_points = max(10, int(distance * 200))  # Much more points for realistic curves
        
        # Generate intermediate points with realistic curves
        for i in range(num_points + 1):
            t = i / num_points
            
            # Add some realistic curve variation based on road name
            curve_factor = self._get_road_curve_factor(road_name)
            
            # Calculate intermediate point with curve
            lat = start_coords[0] + (lat_diff * t)
            lng = start_coords[1] + (lng_diff * t)
            
            # Add curve variation - MORE VISIBLE CURVES!
            if 0 < t < 1:
                # Add perpendicular offset for curve with multiple sine waves
                perp_lat = -lng_diff * curve_factor * (math.sin(math.pi * t) + 0.5 * math.sin(2 * math.pi * t))
                perp_lng = lat_diff * curve_factor * (math.sin(math.pi * t) + 0.5 * math.sin(2 * math.pi * t))
                
                # Add some random variation for more realistic roads
                random_factor = 0.0001 * math.sin(i * 0.5)
                perp_lat += random_factor
                perp_lng += random_factor
                
                lat += perp_lat
                lng += perp_lng
            
            points.append({"lat": lat, "lng": lng})
        
        return points
    
    def _get_road_curve_factor(self, road_name: str) -> float:
        """Get curve factor based on road type - MUCH LARGER FACTORS!"""
        if "Tol" in road_name or "Highway" in road_name:
            return 0.02  # Straight highways but still visible curves
        elif "Raya" in road_name:
            return 0.05  # Major roads with visible curves
        elif "Jalan" in road_name:
            return 0.08  # Regular roads with more visible curves
        elif "Gang" in road_name or "Gg" in road_name:
            return 0.12  # Small roads with very visible curves
        else:
            return 0.06  # Default curve factor - much larger!
    
    def format_route_for_api(self, route: RouteOption) -> Dict:
        """Format route for API response"""
        return {
            "id": route.route_id,
            "destination": route.destination,
            "vehicle_id": f"Truck-{route.route_id.split('_')[1]}",
            "vehicle_type": "Truck Sedang" if route.total_distance_km > 20 else "Truck Kecil",
            "capacity_kg": 2000 if route.total_distance_km > 20 else 1000,
            "current_load_kg": 1700 if route.total_distance_km > 20 else 700,
            "remaining_capacity_kg": 300 if route.total_distance_km > 20 else 300,
            "distance_km": route.total_distance_km,
            "start_location": {"lat": -6.1702, "lng": 106.9417},
            "end_location": {"lat": route.road_segments[-1].end_coords[0], "lng": route.road_segments[-1].end_coords[1]},
            "status": "active",
            "estimated_arrival": f"{route.total_time_minutes} minutes",
            "road_segments": [
                {
                    "road_name": segment.road_name,
                    "length_km": segment.length_km,
                    "traffic_level": segment.traffic_level,
                    "weather_impact": segment.weather_impact,
                    "estimated_time_minutes": segment.estimated_time_minutes,
                    "area": segment.area
                }
                for segment in route.road_segments
            ],
            "route_polyline": route.polyline,
            "traffic_score": route.traffic_score,
            "weather_score": route.weather_score,
            "overall_score": route.overall_score
        }

# Test the system
if __name__ == "__main__":
    route_system = RealisticRouteSystem()
    
    print("🧪 Testing Realistic Route System")
    print("=" * 50)
    
    # Test single route
    bogor_route = route_system.get_optimal_route("bogor", "rain")
    print(f"📍 Route to Bogor:")
    print(f"   Distance: {bogor_route.total_distance_km} km")
    print(f"   Time: {bogor_route.total_time_minutes} minutes")
    print(f"   Score: {bogor_route.overall_score:.2f}")
    print(f"   Roads: {[s.road_name for s in bogor_route.road_segments]}")
    
    # Test all routes
    all_routes = route_system.get_all_routes("sunny")
    print(f"\n📊 All Routes (Sunny Weather):")
    for route in all_routes:
        print(f"   {route.destination}: {route.total_distance_km} km, {route.total_time_minutes} min, Score: {route.overall_score:.2f}")
    
    # Test API format
    api_route = route_system.format_route_for_api(bogor_route)
    print(f"\n🔗 API Format:")
    print(f"   Destination: {api_route['destination']}")
    print(f"   Distance: {api_route['distance_km']} km")
    print(f"   Road Segments: {len(api_route['road_segments'])}")
    print(f"   Polyline Points: {len(api_route['route_polyline'])}") 