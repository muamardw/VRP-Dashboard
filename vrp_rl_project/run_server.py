import uvicorn
from backend_api import app

if __name__ == "__main__":
    print("🚀 Starting PT. Sanghiang Perkasa VRP API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/api/pt-sanghiang-data")
    print("\n" + "="*50)
    
    uvicorn.run(
        "backend_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 