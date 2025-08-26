#!/usr/bin/env python3
"""
Install Dependencies untuk S1 Skripsi
Mengecek dan menginstall package yang diperlukan
"""

import subprocess
import sys
import importlib

def check_package(package_name):
    """Check if package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function to check and install dependencies"""
    
    print("🔧 INSTALLING DEPENDENCIES - S1 SKRIPSI")
    print("=" * 50)
    
    # List of required packages
    required_packages = [
        'torch',
        'numpy', 
        'pandas',
        'matplotlib',
        'requests',
        'fastapi',
        'uvicorn'
    ]
    
    print("📦 Checking required packages...")
    print()
    
    missing_packages = []
    
    for package in required_packages:
        if check_package(package):
            print(f"✅ {package} - Already installed")
        else:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    print()
    
    if not missing_packages:
        print("🎉 All dependencies are already installed!")
        print("✅ You can now run: python run_s1_experiment.py")
        return
    
    print(f"📥 Installing {len(missing_packages)} missing packages...")
    print()
    
    failed_packages = []
    
    for package in missing_packages:
        print(f"📦 Installing {package}...")
        if install_package(package):
            print(f"✅ {package} - Installed successfully")
        else:
            print(f"❌ {package} - Failed to install")
            failed_packages.append(package)
    
    print()
    
    if failed_packages:
        print("⚠️ Some packages failed to install:")
        for package in failed_packages:
            print(f"   - {package}")
        print()
        print("💡 Try installing manually:")
        print(f"   pip install {' '.join(failed_packages)}")
    else:
        print("🎉 All dependencies installed successfully!")
        print("✅ You can now run: python run_s1_experiment.py")
    
    print()
    print("📋 Next Steps:")
    print("   1. Run: python run_s1_experiment.py")
    print("   2. Wait for training to complete")
    print("   3. Check generated files for your skripsi")

if __name__ == "__main__":
    main() 