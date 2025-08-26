#!/usr/bin/env python3
"""
Route API untuk DQN VRP
API endpoint untuk informasi rute dengan nama jalan dan kondisi dinamis
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn

from route_info_system import RouteInfoSystem

app = FastAPI(title="Route Information API", version="1.0.0")

# Initialize route system
route_system = RouteInfoSystem()

class RouteRequest(BaseModel):
    vehicle_id: int
    route: List[List[float]]  # List of [lat, lng] coordinates
    weather: str = "sunny"
    start_time: Optional[str] = None

class RouteResponse(BaseModel):
    vehicle_id: int
    total_distance: float
    total_time: float
    weather_condition: str
    start_time: str
    estimated_completion: str
    route_segments: List[Dict]

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Route Information API for DQN VRP", "version": "1.0.0"}

@app.get("/api/route-info/{vehicle_id}")
async def get_route_info(vehicle_id: int, weather: str = "sunny"):
    """Get route information for a specific vehicle"""
    
    # Default route for testing
    default_route = [
        [-6.2088, 106.8456],  # Customer 0
        [-6.2146, 106.8451],  # Customer 2
        [-6.1865, 106.8343],  # Customer 4
        [-6.1751, 106.8650],  # Customer 1
        [-6.2297, 106.7997],  # Customer 3
        [-6.2088, 106.8456]   # Back to depot
    ]
    
    try:
        # Convert route to tuples
        route_tuples = [(point[0], point[1]) for point in default_route]
        
        # Get route information
        route_info = route_system.get_vehicle_route_info(vehicle_id, route_tuples, weather)
        
        # Ensure road_segments are properly included in response
        formatted_segments = []
        for segment in route_info["route_segments"]:
            formatted_segment = {
                "from": segment["from"],
                "to": segment["to"],
                "distance": round(segment["distance"], 2),
                "travel_time": round(segment["travel_time"], 2),
                "traffic_condition": segment["traffic_condition"],
                "weather_condition": segment["weather_condition"],
                "adjusted_speed": round(segment["adjusted_speed"], 1),
                "estimated_arrival": segment["estimated_arrival"].strftime("%H:%M"),
                "road_segments": segment["road_segments"]  # Ensure this is included
            }
            formatted_segments.append(formatted_segment)
        
        return {
            "vehicle_id": route_info["vehicle_id"],
            "total_distance": round(route_info["total_distance"], 2),
            "total_time": round(route_info["total_time"], 2),
            "weather_condition": route_info["weather_condition"],
            "start_time": route_info["start_time"].strftime("%H:%M"),
            "estimated_completion": route_info["estimated_completion"].strftime("%H:%M"),
            "route_segments": formatted_segments
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting route info: {str(e)}")

@app.post("/api/route-info")
async def create_route_info(request: RouteRequest):
    """Create route information for custom route"""
    
    try:
        # Convert route to tuples
        route_tuples = [(point[0], point[1]) for point in request.route]
        
        # Parse start time
        start_time = datetime.now()
        if request.start_time:
            try:
                start_time = datetime.strptime(request.start_time, "%H:%M")
            except ValueError:
                start_time = datetime.now()
        
        # Get route information
        route_info = route_system.get_vehicle_route_info(
            request.vehicle_id, 
            route_tuples, 
            request.weather, 
            start_time
        )
        
        # Format segments with road information
        formatted_segments = []
        for segment in route_info["route_segments"]:
            formatted_segment = {
                "from": segment["from"],
                "to": segment["to"],
                "distance": round(segment["distance"], 2),
                "travel_time": round(segment["travel_time"], 2),
                "traffic_condition": segment["traffic_condition"],
                "weather_condition": segment["weather_condition"],
                "adjusted_speed": round(segment["adjusted_speed"], 1),
                "estimated_arrival": segment["estimated_arrival"].strftime("%H:%M"),
                "road_segments": segment["road_segments"]  # Ensure this is included
            }
            formatted_segments.append(formatted_segment)
        
        return {
            "vehicle_id": route_info["vehicle_id"],
            "total_distance": round(route_info["total_distance"], 2),
            "total_time": round(route_info["total_time"], 2),
            "weather_condition": route_info["weather_condition"],
            "start_time": route_info["start_time"].strftime("%H:%M"),
            "estimated_completion": route_info["estimated_completion"].strftime("%H:%M"),
            "route_segments": formatted_segments
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating route info: {str(e)}")

@app.get("/api/weather-conditions")
async def get_weather_conditions():
    """Get available weather conditions"""
    return {
        "weather_conditions": route_system.weather_conditions,
        "traffic_conditions": route_system.traffic_conditions
    }

@app.get("/api/road-segments/{segment_id}")
async def get_road_segment_info(segment_id: int, weather: str = "sunny"):
    """Get detailed information for a specific road segment"""
    
    try:
        # Get sample road segments
        road_names = list(route_system.jakarta_roads.keys())
        if segment_id < len(road_names):
            road_name = road_names[segment_id]
            road_info = route_system.jakarta_roads[road_name]
            
            return {
                "segment_id": segment_id,
                "road_name": road_name,
                "traffic_level": road_info["traffic_level"],
                "weather_impact": road_info["weather_impact"],
                "area": road_info["area"],
                "current_weather": weather,
                "status": route_system._get_segment_status(
                    {"traffic_level": road_info["traffic_level"]},
                    {"condition": road_info["traffic_level"]},
                    {"condition": weather}
                )
            }
        else:
            raise HTTPException(status_code=404, detail="Road segment not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting road segment info: {str(e)}")

@app.get("/api/route-status/{vehicle_id}")
async def get_route_status(vehicle_id: int):
    """Get current route status for a vehicle"""
    
    try:
        # Get route info
        route_info = await get_route_info(vehicle_id, "sunny")
        
        # Calculate status
        total_segments = len(route_info["route_segments"])
        completed_segments = sum(1 for segment in route_info["route_segments"] 
                               if "completed" in segment and segment["completed"])
        
        progress = (completed_segments / total_segments) * 100 if total_segments > 0 else 0
        
        return {
            "vehicle_id": vehicle_id,
            "progress": round(progress, 1),
            "completed_segments": completed_segments,
            "total_segments": total_segments,
            "status": "In Progress" if progress < 100 else "Completed",
            "estimated_completion": route_info["estimated_completion"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting route status: {str(e)}")

@app.get("/api/traffic-update")
async def get_traffic_update():
    """Get real-time traffic update"""
    
    current_time = datetime.now()
    hour = current_time.hour
    
    # Determine traffic based on time
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        traffic_level = "high"
        description = "Rush Hour"
    elif 10 <= hour <= 16:
        traffic_level = "medium"
        description = "Normal Traffic"
    else:
        traffic_level = "low"
        description = "Off-Peak"
    
    return {
        "current_time": current_time.strftime("%H:%M"),
        "traffic_level": traffic_level,
        "description": description,
        "speed": route_system.traffic_conditions[traffic_level]["speed"],
        "factor": route_system.traffic_conditions[traffic_level]["speed"] / 40
    }

@app.get("/api/test-route")
async def test_route():
    """Test endpoint to check if road segments are working"""
    
    try:
        # Test with a simple route
        test_route = [
            (-6.2088, 106.8456),  # Customer 0
            (-6.2146, 106.8451),  # Customer 2
            (-6.2088, 106.8456)   # Back to depot
        ]
        
        route_info = route_system.get_vehicle_route_info(1, test_route, "sunny")
        
        # Return detailed information for debugging
        return {
            "message": "Test route successful",
            "route_info": route_info,
            "road_segments_example": route_info["route_segments"][0]["road_segments"] if route_info["route_segments"] else []
        }
    
    except Exception as e:
        return {
            "message": "Test route failed",
            "error": str(e)
        }

if __name__ == "__main__":
    print("🚗 Starting Route Information API...")
    print("📡 API will be available at http://localhost:8001")
    print("📚 Documentation at http://localhost:8001/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8001) 