import os
import yaml
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dotenv import load_dotenv

def load_config() -> Dict:
    """Load configuration from config.yaml file."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_env_vars() -> Dict[str, str]:
    """Load environment variables from .env file."""
    load_dotenv()
    return {
        'GOOGLE_MAPS_API_KEY': os.getenv('GOOGLE_MAPS_API_KEY'),
        'OPENWEATHER_API_KEY': os.getenv('OPENWEATHER_API_KEY')
    }

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the Haversine distance between two points on Earth.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def generate_simulated_data(n_customers: int = 50, 
                          n_vehicles: int = 5,
                          max_capacity: float = 1000) -> pd.DataFrame:
    """
    Generate simulated delivery data.
    
    Args:
        n_customers: Number of delivery points
        n_vehicles: Number of available vehicles
        max_capacity: Maximum capacity of each vehicle in kg
    
    Returns:
        DataFrame containing simulated delivery data
    """
    np.random.seed(42)
    
    # Generate random coordinates around a center point
    center_lat, center_lon = 0, 0
    lat_range, lon_range = 0.1, 0.1
    
    data = {
        'customer_id': range(n_customers),
        'latitude': np.random.uniform(center_lat - lat_range, center_lat + lat_range, n_customers),
        'longitude': np.random.uniform(center_lon - lon_range, center_lon + lon_range, n_customers),
        'demand': np.random.uniform(10, 100, n_customers),
        'time_window_start': np.random.uniform(0, 12, n_customers),
        'time_window_end': np.random.uniform(13, 24, n_customers),
        'service_time': np.random.uniform(5, 30, n_customers)
    }
    
    df = pd.DataFrame(data)
    df['time_window_end'] = df['time_window_start'] + df['time_window_end']
    
    return df

def calculate_weather_impact(weather_condition: str, config: Dict) -> float:
    """
    Calculate the impact of weather conditions on travel time.
    
    Args:
        weather_condition: Current weather condition
        config: Configuration dictionary
    
    Returns:
        Weather impact factor
    """
    return config['weather_impact'].get(weather_condition.lower(), 1.0)

def calculate_traffic_impact(traffic_level: str, config: Dict) -> float:
    """
    Calculate the impact of traffic conditions on travel time.
    
    Args:
        traffic_level: Current traffic level
        config: Configuration dictionary
    
    Returns:
        Traffic impact factor
    """
    return config['traffic_impact'].get(traffic_level.lower(), 1.0)

def save_results(results: Dict, filename: str):
    """
    Save results to a CSV file.
    
    Args:
        results: Dictionary containing results
        filename: Output filename
    """
    df = pd.DataFrame(results)
    df.to_csv(f'data/{filename}', index=False)

def plot_route(route: List[Tuple[float, float]], 
              customers: pd.DataFrame,
              title: str = "Optimal Route"):
    """
    Plot the delivery route.
    
    Args:
        route: List of (latitude, longitude) tuples
        customers: DataFrame containing customer locations
        title: Plot title
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 10))
    
    # Plot customer locations
    plt.scatter(customers['longitude'], customers['latitude'], 
               c='blue', label='Customers')
    
    # Plot route
    route_lons, route_lats = zip(*route)
    plt.plot(route_lons, route_lats, 'r-', label='Route')
    
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'data/{title.lower().replace(" ", "_")}.png')
    plt.close() 