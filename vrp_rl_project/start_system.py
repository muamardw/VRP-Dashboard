#!/usr/bin/env python3
"""
Start System - PT. Sanghiang Perkasa VRP
Script untuk menjalankan backend dan frontend dengan mudah
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn are installed")
    except ImportError:
        print("❌ FastAPI or Uvicorn not found")
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
    
    try:
        import requests
        print("✅ Requests is installed")
    except ImportError:
        print("❌ Requests not found")
        print("Installing requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

def start_backend():
    """Start the backend API server"""
    print("🚀 Starting PT. Sanghiang Perkasa Backend API...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/api/test")
    print("📊 Simple Data: http://localhost:8000/api/simple-pt-sanghiang-data")
    print("\n" + "="*60)
    
    try:
        # Start the backend server
        backend_process = subprocess.Popen([
            sys.executable, "run_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("⏳ Waiting for backend server to start...")
        time.sleep(5)
        
        # Test if server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/api/test", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully!")
                return backend_process
            else:
                print("❌ Backend server not responding properly")
                return None
        except:
            print("❌ Backend server not responding")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend server: {e}")
        return None

def start_frontend():
    """Start the frontend React app"""
    print("\n🌐 Starting PT. Sanghiang Perkasa Frontend...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("📊 Dashboard with maps and route information")
    print("🛣️ Road names and traffic information")
    print("\n" + "="*60)
    
    try:
        # Change to frontend directory
        frontend_dir = Path("../frontend")
        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return None
        
        # Check if node_modules exists
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            subprocess.check_call(["npm", "install"], cwd=frontend_dir)
        
        # Start the frontend
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to start
        print("⏳ Waiting for frontend to start...")
        time.sleep(10)
        
        # Open browser
        print("🌐 Opening dashboard in browser...")
        webbrowser.open("http://localhost:3000")
        
        return frontend_process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def show_manual_instructions():
    """Show manual instructions if automatic setup fails"""
    print("\n📋 Manual Setup Instructions")
    print("="*40)
    print("Jika sistem otomatis gagal, ikuti langkah berikut:")
    print()
    print("1. Start Backend (Terminal 1):")
    print("   cd vrp_rl_project")
    print("   python run_server.py")
    print()
    print("2. Start Frontend (Terminal 2):")
    print("   cd frontend")
    print("   npm start")
    print()
    print("3. Open Dashboard:")
    print("   Buka http://localhost:3000 di browser")
    print()
    print("4. Test API:")
    print("   curl http://localhost:8000/api/simple-pt-sanghiang-data")
    print()

def main():
    """Main function to start the complete system"""
    print("🚀 PT. Sanghiang Perkasa VRP System")
    print("="*50)
    print("🎯 Backend: FastAPI dengan data PT. Sanghiang Perkasa")
    print("🌐 Frontend: React Dashboard dengan maps dan nama jalan")
    print("🛣️ Fitur: Informasi rute, traffic, weather, dan nama jalan")
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Start backend
    backend_process = start_backend()
    
    if backend_process:
        # Start frontend
        frontend_process = start_frontend()
        
        if frontend_process:
            print("\n🎉 System started successfully!")
            print("📊 Dashboard: http://localhost:3000")
            print("📡 API: http://localhost:8000")
            print("📚 Docs: http://localhost:8000/docs")
            print("\n💡 Press Ctrl+C to stop the system")
            
            try:
                # Keep the system running
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping system...")
                
                # Stop processes
                if backend_process:
                    backend_process.terminate()
                    print("✅ Backend stopped")
                
                if frontend_process:
                    frontend_process.terminate()
                    print("✅ Frontend stopped")
                
                print("👋 System stopped. Goodbye!")
        else:
            print("\n⚠️ Frontend failed to start")
            print("Backend is running at http://localhost:8000")
            show_manual_instructions()
    else:
        print("\n❌ Backend failed to start")
        show_manual_instructions()

if __name__ == "__main__":
    main() 