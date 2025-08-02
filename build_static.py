#!/usr/bin/env python3
"""
Build script for photography project static files
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {command}")
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {command}")
        print(f"Exception: {e}")
        return False

def main():
    """Main build function"""
    print("🚀 Building static files for photography project...")
    
    # Get the project root directory
    project_root = Path(__file__).parent
    theme_static_src = project_root / "theme" / "static_src"
    
    # Check if we're in the right directory
    if not theme_static_src.exists():
        print("❌ theme/static_src directory not found!")
        return False
    
    print(f"📁 Working in: {theme_static_src}")
    
    # Step 1: Install npm dependencies
    print("\n📦 Installing npm dependencies...")
    if not run_command("npm install", cwd=theme_static_src):
        print("❌ Failed to install npm dependencies")
        return False
    
    # Step 2: Build Tailwind CSS
    print("\n🎨 Building Tailwind CSS...")
    if not run_command("npm run build", cwd=theme_static_src):
        print("❌ Failed to build Tailwind CSS")
        return False
    
    # Step 3: Collect Django static files
    print("\n📁 Collecting Django static files...")
    if not run_command("python manage.py collectstatic --noinput", cwd=project_root):
        print("❌ Failed to collect static files")
        return False
    
    print("\n✅ Build completed successfully!")
    print("\n📝 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000")
    print("3. For development with auto-reload: npm run dev (in theme/static_src)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 