import requests
import os
from typing import Dict, Optional, Tuple
from utils import load_config, load_env_vars

class TrafficAPI:
    def __init__(self):
        """Initialize Traffic API client."""
        self.config = load_config()
        self.env_vars = load_env_vars()
        self.api_key = self.env_vars['GOOGLE_MAPS_API_KEY']
        self.base_url = self.config['api']['google_maps']['base_url']
        self.traffic_endpoint = self.config['api']['google_maps']['traffic_endpoint']

    def get_traffic_data(self, 
                        origin: Tuple[float, float], 
                        destination: Tuple[float, float]) -> Optional[Dict]:
        """
        Get traffic data between two points.
        
        Args:
            origin: Tuple of (latitude, longitude) for origin
            destination: Tuple of (latitude, longitude) for destination
            
        Returns:
            Dictionary containing traffic information or None if request fails
        """
        try:
            url = f"{self.base_url}/directions/json"
            params = {
                'origin': f"{origin[0]},{origin[1]}",
                'destination': f"{destination[0]},{destination[1]}",
                'key': self.api_key,
                'departure_time': 'now',
                'traffic_model': 'best_guess'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['status'] == 'OK':
                route = data['routes'][0]['legs'][0]
                return {
                    'distance': route['distance']['value'],  # meters
                    'duration': route['duration']['value'],  # seconds
                    'duration_in_traffic': route.get('duration_in_traffic', {}).get('value', route['duration']['value']),
                    'traffic_level': self._calculate_traffic_level(route)
                }
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching traffic data: {e}")
            return None

    def _calculate_traffic_level(self, route: Dict) -> str:
        """
        Calculate traffic level based on duration and duration in traffic.
        
        Args:
            route: Route information from Google Maps API
            
        Returns:
            Traffic level ('low', 'medium', or 'high')
        """
        duration = route['duration']['value']
        duration_in_traffic = route.get('duration_in_traffic', {}).get('value', duration)
        
        # Calculate traffic impact ratio
        ratio = duration_in_traffic / duration
        
        if ratio < 1.2:
            return 'low'
        elif ratio < 1.5:
            return 'medium'
        else:
            return 'high'

    def get_traffic_impact(self, 
                          origin: Tuple[float, float], 
                          destination: Tuple[float, float]) -> float:
        """
        Calculate traffic impact factor between two points.
        
        Args:
            origin: Tuple of (latitude, longitude) for origin
            destination: Tuple of (latitude, longitude) for destination
            
        Returns:
            Traffic impact factor (1.0 for normal conditions)
        """
        traffic_data = self.get_traffic_data(origin, destination)
        if traffic_data:
            return self.config['traffic_impact'].get(
                traffic_data['traffic_level'],
                1.0
            )
        return 1.0  # Default to normal conditions if API fails 