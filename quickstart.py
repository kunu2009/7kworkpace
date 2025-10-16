"""
Quick start guide for Workspace Organizer
"""

import subprocess
import sys
import os


def install_dependencies():
    """Install required packages"""
    print("📥 Installing dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    print("✅ Dependencies installed!")


def run_app():
    """Run the application"""
    print("🚀 Starting Workspace Organizer...")
    subprocess.call([sys.executable, "main.py"])


def build_exe():
    """Build executable"""
    print("🔨 Building executable...")
    subprocess.call([sys.executable, "build_exe.py"])


def show_menu():
    """Show menu"""
    print("""
╔═════════════════════════════════════════╗
║   Workspace Organizer - Quick Start     ║
╚═════════════════════════════════════════╝

Options:
  1. Install dependencies
  2. Run application
  3. Build executable
  4. Exit

    """)


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            run_app()
        elif choice == "3":
            build_exe()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print()
