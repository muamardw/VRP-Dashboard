#!/usr/bin/env python3
"""
Route Information System untuk DQN VRP
Sistem informasi rute dengan nama jalan dan kondisi dinamis
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class RouteInfoSystem:
    """Sistem informasi rute dengan nama jalan dan kondisi dinamis"""
    
    def __init__(self):
        """Initialize route information system"""
        self.jakarta_roads = {
            "Jalan Sudirman": {"traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Pusat"},
            "Jalan Thamrin": {"traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Pusat"},
            "Jalan Gatot Subroto": {"traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Rasuna Said": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan HR Rasuna Said": {"traffic_level": "medium", "weather_impact": "medium", "area": "Jakarta Selatan"},
            "Jalan Jenderal Ahmad Yani": {"traffic_level": "high", "weather_impact": "high", "area": "Jakarta Timur"},
            "Jalan Hayam Wuruk": {"traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Barat"},
            "Jalan Gajah Mada": {"traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Pusat"},
            "Jalan MH Thamrin": {"traffic_level": "high", "weather_impact": "low", "area": "Jakarta Pusat"},
            "Jalan Senayan": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Pusat"},
            "Jalan Asia Afrika": {"traffic_level": "medium", "weather_impact": "medium", "area": "Jakarta Pusat"},
            "Jalan Kuningan": {"traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Setiabudi": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Kebayoran Baru": {"traffic_level": "medium", "weather_impact": "medium", "area": "Jakarta Selatan"},
            "Jalan Kemang": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Blok M": {"traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Selatan"},
            "Jalan Fatmawati": {"traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Ciputat Raya": {"traffic_level": "medium", "weather_impact": "medium", "area": "Jakarta Selatan"},
            "Jalan Lebak Bulus": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"},
            "Jalan Pondok Indah": {"traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"}
        }
        
        self.weather_conditions = {
            "sunny": {"impact": "low", "description": "Cerah"},
            "cloudy": {"impact": "medium", "description": "Berawan"},
            "rainy": {"impact": "high", "description": "Hujan"},
            "stormy": {"impact": "very_high", "description": "Badai"}
        }
        
        self.traffic_conditions = {
            "low": {"speed": 40, "description": "Lancar"},
            "medium": {"speed": 25, "description": "Sedang"},
            "high": {"speed": 15, "description": "Padat"},
            "very_high": {"speed": 8, "description": "Macet"}
        }
        
        # Mapping koordinat ke area Jakarta
        self.jakarta_areas = {
            "Jakarta Pusat": [(-6.2088, 106.8456), (-6.1751, 106.8650)],
            "Jakarta Selatan": [(-6.2146, 106.8451), (-6.1865, 106.8343)],
            "Jakarta Timur": [(-6.2297, 106.7997)],
            "Jakarta Barat": [(-6.1751, 106.8650)],
            "Jakarta Utara": [(-6.2088, 106.8456)]
        }
    
    def get_route_info(self, start_point: Tuple[float, float], end_point: Tuple[float, float], 
                       weather: str = "sunny", time: datetime = None) -> Dict:
        """Get route information with road names and dynamic conditions"""
        
        if time is None:
            time = datetime.now()
        
        # Calculate distance (simplified)
        distance = self._calculate_distance(start_point, end_point)
        
        # Get road segments for this route
        road_segments = self._get_road_segments(start_point, end_point)
        
        # Calculate dynamic factors
        traffic_impact = self._calculate_traffic_impact(road_segments, time)
        weather_impact = self._calculate_weather_impact(weather, road_segments)
        
        # Calculate travel time
        base_speed = 30  # km/h
        traffic_factor = traffic_impact['factor']
        weather_factor = weather_impact['factor']
        
        adjusted_speed = base_speed * traffic_factor * weather_factor
        travel_time = distance / adjusted_speed  # hours
        
        return {
            "distance": distance,
            "travel_time": travel_time,
            "road_segments": road_segments,
            "traffic_condition": traffic_impact['condition'],
            "weather_condition": weather,
            "weather_description": self.weather_conditions[weather]['description'],
            "adjusted_speed": adjusted_speed,
            "traffic_factor": traffic_factor,
            "weather_factor": weather_factor,
            "route_details": self._generate_route_details(road_segments, traffic_impact, weather_impact)
        }
    
    def _calculate_distance(self, start: Tuple[float, float], end: Tuple[float, float]) -> float:
        """Calculate distance between two points (simplified)"""
        import math
        
        lat1, lon1 = start
        lat2, lon2 = end
        
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        return distance
    
    def _get_road_segments(self, start: Tuple[float, float], end: Tuple[float, float]) -> List[Dict]:
        """Get road segments for the route with realistic road mapping"""
        
        # Determine area based on coordinates
        start_area = self._get_area_from_coordinates(start)
        end_area = self._get_area_from_coordinates(end)
        
        # Get appropriate roads for the route
        road_segments = []
        
        # Route from start to end
        if start_area == "Jakarta Pusat" and end_area == "Jakarta Selatan":
            # Route: Pusat → Selatan
            road_segments = [
                {"road_name": "Jalan Sudirman", "length": 1.2, "traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Pusat"},
                {"road_name": "Jalan Gatot Subroto", "length": 2.1, "traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Selatan"},
                {"road_name": "Jalan Rasuna Said", "length": 1.8, "traffic_level": "low", "weather_impact": "low", "area": "Jakarta Selatan"}
            ]
        elif start_area == "Jakarta Selatan" and end_area == "Jakarta Timur":
            # Route: Selatan → Timur
            road_segments = [
                {"road_name": "Jalan HR Rasuna Said", "length": 1.5, "traffic_level": "medium", "weather_impact": "medium", "area": "Jakarta Selatan"},
                {"road_name": "Jalan Jenderal Ahmad Yani", "length": 3.2, "traffic_level": "high", "weather_impact": "high", "area": "Jakarta Timur"},
                {"road_name": "Jalan Fatmawati", "length": 1.8, "traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Selatan"}
            ]
        elif start_area == "Jakarta Timur" and end_area == "Jakarta Pusat":
            # Route: Timur → Pusat
            road_segments = [
                {"road_name": "Jalan Jenderal Ahmad Yani", "length": 2.5, "traffic_level": "high", "weather_impact": "high", "area": "Jakarta Timur"},
                {"road_name": "Jalan Sudirman", "length": 1.8, "traffic_level": "medium", "weather_impact": "low", "area": "Jakarta Pusat"},
                {"road_name": "Jalan Thamrin", "length": 1.2, "traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Pusat"}
            ]
        elif start_area == "Jakarta Pusat" and end_area == "Jakarta Barat":
            # Route: Pusat → Barat
            road_segments = [
                {"road_name": "Jalan MH Thamrin", "length": 1.0, "traffic_level": "high", "weather_impact": "low", "area": "Jakarta Pusat"},
                {"road_name": "Jalan Gajah Mada", "length": 1.5, "traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Pusat"},
                {"road_name": "Jalan Hayam Wuruk", "length": 2.0, "traffic_level": "high", "weather_impact": "medium", "area": "Jakarta Barat"}
            ]
        else:
            # Default route with random roads
            road_names = list(self.jakarta_roads.keys())
            num_segments = random.randint(2, 4)
            
            for i in range(num_segments):
                road_name = random.choice(road_names)
                road_info = self.jakarta_roads[road_name]
                segment_length = random.uniform(0.8, 3.0)
                
                road_segments.append({
                    "road_name": road_name,
                    "length": segment_length,
                    "traffic_level": road_info["traffic_level"],
                    "weather_impact": road_info["weather_impact"],
                    "area": road_info["area"]
                })
        
        return road_segments
    
    def _get_area_from_coordinates(self, coordinates: Tuple[float, float]) -> str:
        """Get Jakarta area from coordinates"""
        lat, lon = coordinates
        
        # Simplified area mapping based on coordinates
        if -6.21 <= lat <= -6.18 and 106.80 <= lon <= 106.85:
            return "Jakarta Pusat"
        elif -6.22 <= lat <= -6.18 and 106.83 <= lon <= 106.87:
            return "Jakarta Selatan"
        elif -6.23 <= lat <= -6.20 and 106.79 <= lon <= 106.82:
            return "Jakarta Timur"
        elif -6.17 <= lat <= -6.15 and 106.86 <= lon <= 106.87:
            return "Jakarta Barat"
        else:
            return "Jakarta Pusat"  # Default
    
    def _calculate_traffic_impact(self, road_segments: List[Dict], time: datetime) -> Dict:
        """Calculate traffic impact based on time and road segments"""
        
        # Time-based traffic patterns
        hour = time.hour
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Rush hours
            base_traffic = "high"
        elif 10 <= hour <= 16:  # Normal hours
            base_traffic = "medium"
        else:  # Off-peak hours
            base_traffic = "low"
        
        # Calculate average traffic level
        traffic_levels = [segment["traffic_level"] for segment in road_segments]
        avg_traffic = max(traffic_levels, key=traffic_levels.count)
        
        # Combine time-based and road-based traffic
        if base_traffic == "high" and avg_traffic == "high":
            final_traffic = "very_high"
        elif base_traffic == "high" or avg_traffic == "high":
            final_traffic = "high"
        elif base_traffic == "medium" or avg_traffic == "medium":
            final_traffic = "medium"
        else:
            final_traffic = "low"
        
        return {
            "condition": final_traffic,
            "description": self.traffic_conditions[final_traffic]["description"],
            "speed": self.traffic_conditions[final_traffic]["speed"],
            "factor": self.traffic_conditions[final_traffic]["speed"] / 40  # Normalized factor
        }
    
    def _calculate_weather_impact(self, weather: str, road_segments: List[Dict]) -> Dict:
        """Calculate weather impact on route"""
        
        weather_impact = self.weather_conditions[weather]["impact"]
        
        # Weather impact factors
        impact_factors = {
            "low": 1.0,
            "medium": 0.8,
            "high": 0.6,
            "very_high": 0.4
        }
        
        return {
            "condition": weather,
            "description": self.weather_conditions[weather]["description"],
            "factor": impact_factors[weather_impact]
        }
    
    def _generate_route_details(self, road_segments: List[Dict], traffic: Dict, weather: Dict) -> List[Dict]:
        """Generate detailed route information"""
        
        details = []
        for i, segment in enumerate(road_segments):
            detail = {
                "segment": i + 1,
                "road_name": segment["road_name"],
                "length": segment["length"],
                "traffic_level": segment["traffic_level"],
                "weather_impact": segment["weather_impact"],
                "area": segment["area"],
                "estimated_time": segment["length"] / (traffic["speed"] * weather["factor"]),
                "status": self._get_segment_status(segment, traffic, weather)
            }
            details.append(detail)
        
        return details
    
    def _get_segment_status(self, segment: Dict, traffic: Dict, weather: Dict) -> str:
        """Get status for road segment"""
        
        if traffic["condition"] == "very_high" and weather["condition"] in ["rainy", "stormy"]:
            return "⚠️ Macet & Cuaca Buruk"
        elif traffic["condition"] == "very_high":
            return "🚗 Macet"
        elif weather["condition"] in ["rainy", "stormy"]:
            return "🌧️ Cuaca Buruk"
        elif traffic["condition"] == "high":
            return "🚙 Padat"
        else:
            return "✅ Lancar"
    
    def get_vehicle_route_info(self, vehicle_id: int, route: List[Tuple[float, float]], 
                              weather: str = "sunny", start_time: datetime = None) -> Dict:
        """Get complete route information for a vehicle"""
        
        if start_time is None:
            start_time = datetime.now()
        
        route_info = []
        total_distance = 0
        total_time = 0
        current_time = start_time
        
        for i in range(len(route) - 1):
            start_point = route[i]
            end_point = route[i + 1]
            
            segment_info = self.get_route_info(start_point, end_point, weather, current_time)
            
            route_info.append({
                "from": f"Customer {i}" if i < len(route) - 2 else "Depot",
                "to": f"Customer {i + 1}" if i < len(route) - 2 else "Depot",
                "distance": segment_info["distance"],
                "travel_time": segment_info["travel_time"],
                "road_segments": segment_info["road_segments"],
                "traffic_condition": segment_info["traffic_condition"],
                "weather_condition": segment_info["weather_condition"],
                "adjusted_speed": segment_info["adjusted_speed"],
                "estimated_arrival": current_time + timedelta(hours=segment_info["travel_time"]),
                "route_details": segment_info["route_details"]
            })
            
            total_distance += segment_info["distance"]
            total_time += segment_info["travel_time"]
            current_time += timedelta(hours=segment_info["travel_time"])
        
        return {
            "vehicle_id": vehicle_id,
            "total_distance": total_distance,
            "total_time": total_time,
            "weather_condition": weather,
            "start_time": start_time,
            "estimated_completion": start_time + timedelta(hours=total_time),
            "route_segments": route_info
        }

def main():
    """Test the route information system"""
    
    print("🚗 Route Information System untuk DQN VRP")
    print("=" * 50)
    
    # Initialize system
    route_system = RouteInfoSystem()
    
    # Test route
    test_route = [
        (-6.2088, 106.8456),  # Customer 0
        (-6.2146, 106.8451),  # Customer 2
        (-6.1865, 106.8343),  # Customer 4
        (-6.1751, 106.8650),  # Customer 1
        (-6.2297, 106.7997),  # Customer 3
        (-6.2088, 106.8456)   # Back to depot
    ]
    
    # Get route information
    route_info = route_system.get_vehicle_route_info(1, test_route, "rainy")
    
    print(f"\n📊 Informasi Rute Kendaraan {route_info['vehicle_id']}:")
    print(f"Total Distance: {route_info['total_distance']:.2f} km")
    print(f"Total Time: {route_info['total_time']:.2f} jam")
    print(f"Weather: {route_info['weather_condition']}")
    print(f"Start Time: {route_info['start_time'].strftime('%H:%M')}")
    print(f"Estimated Completion: {route_info['estimated_completion'].strftime('%H:%M')}")
    
    print(f"\n🛣️ Detail Rute dengan Informasi Jalan:")
    for i, segment in enumerate(route_info['route_segments']):
        print(f"\nSegment {i+1}: {segment['from']} → {segment['to']}")
        print(f"  Distance: {segment['distance']:.2f} km")
        print(f"  Travel Time: {segment['travel_time']:.2f} jam")
        print(f"  Traffic: {segment['traffic_condition']}")
        print(f"  Weather: {segment['weather_condition']}")
        print(f"  Speed: {segment['adjusted_speed']:.1f} km/h")
        print(f"  ETA: {segment['estimated_arrival'].strftime('%H:%M')}")
        
        # Show detailed road information
        print(f"  🛣️ Jalan yang akan dilewati:")
        for j, road in enumerate(segment['road_segments']):
            print(f"    {j+1}. {road['road_name']} ({road['area']})")
            print(f"       - Panjang: {road['length']:.1f} km")
            print(f"       - Traffic Level: {road['traffic_level']}")
            print(f"       - Weather Impact: {road['weather_impact']}")
            print(f"       - Status: {route_system._get_segment_status(road, {'condition': road['traffic_level']}, {'condition': segment['weather_condition']})}")

if __name__ == "__main__":
    main() 