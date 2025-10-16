"""
Installation and Setup Script for Workspace Organizer
This script handles all the setup needed to run the application
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have Python {version.major}.{version.minor}")
        return False
    return True


def install_requirements():
    """Install required packages from requirements.txt"""
    print("📥 Installing dependencies...")
    print("   This may take a few minutes...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_installation():
    """Verify that all required packages are installed"""
    required_packages = ['PyQt6']
    
    print("🔍 Checking installation...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            return False
    
    return True


def create_directories():
    """Create necessary directories"""
    dirs_to_create = [
        Path.home() / ".workspace_organizer",
        Path.home() / ".workspace_organizer" / "notes"
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created/verified")


def main():
    """Main installation routine"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║        Workspace Organizer - Installation Script              ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check Python version
    print("Step 1/4: Checking Python version...")
    if not check_python_version():
        print("Please install Python 3.8 or higher from https://www.python.org/")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    print()
    
    # Step 2: Install requirements
    print("Step 2/4: Installing dependencies...")
    if not install_requirements():
        print("Please try installing manually:")
        print("  python -m pip install -r requirements.txt")
        sys.exit(1)
    print()
    
    # Step 3: Verify installation
    print("Step 3/4: Verifying installation...")
    if not check_installation():
        print("Installation verification failed!")
        sys.exit(1)
    print()
    
    # Step 4: Create directories
    print("Step 4/4: Setting up data directories...")
    create_directories()
    print()
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║              Installation Complete! ✅                         ║
╚════════════════════════════════════════════════════════════════╝

Your Workspace Organizer is ready to use!

Next Steps:
  1. Run the application: python main.py
  2. Or double-click: RUN_APP.bat
  
To build an executable:
  1. Run: python build_exe.py
  2. Or double-click: BUILD_EXE.bat

For more information, see: README.md and SETUP_GUIDE.txt
    """)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
