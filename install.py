#!/usr/bin/env python3
"""
Automated installation script for PhotoShare photography project
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step, message):
    """Print a formatted step message"""
    print(f"\n{'='*50}")
    print(f"STEP {step}: {message}")
    print(f"{'='*50}")

def run_command(command, cwd=None, check=True):
    """Run a command and return the result"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {command}")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print(f"❌ Error: {command}")
            print(f"Error output: {result.stderr}")
            if check:
                return False
        return True
    except Exception as e:
        print(f"❌ Exception: {command}")
        print(f"Exception: {e}")
        if check:
            return False
        return True

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed!")
    print("Please install Node.js 16+ from https://nodejs.org/")
    return False

def create_virtual_environment():
    """Create and activate virtual environment"""
    venv_name = "env"
    
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists")
        return True
    
    print(f"Creating virtual environment '{venv_name}'...")
    if not run_command(f"python -m venv {venv_name}"):
        return False
    
    print("✅ Virtual environment created successfully")
    print("\n📝 To activate the virtual environment:")
    if platform.system() == "Windows":
        print(f"  {venv_name}\\Scripts\\activate")
    else:
        print(f"  source {venv_name}/bin/activate")
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    return run_command("pip install -r requirements.txt")

def setup_tailwind():
    """Set up Tailwind CSS"""
    theme_dir = Path("theme/static_src")
    if not theme_dir.exists():
        print("❌ theme/static_src directory not found!")
        return False
    
    print("Setting up Tailwind CSS...")
    
    # Install npm dependencies
    if not run_command("npm install", cwd=theme_dir):
        return False
    
    # Build Tailwind CSS
    if not run_command("npm run build", cwd=theme_dir):
        return False
    
    return True

def setup_database():
    """Set up database"""
    print("Setting up database...")
    
    # Make migrations
    if not run_command("python manage.py makemigrations"):
        return False
    
    # Apply migrations
    if not run_command("python manage.py migrate"):
        return False
    
    return True

def collect_static_files():
    """Collect static files"""
    print("Collecting static files...")
    return run_command("python manage.py collectstatic --noinput")

def create_superuser():
    """Create superuser account"""
    print("\n🤔 Would you like to create a superuser account? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes']:
        print("Creating superuser...")
        # Use subprocess.Popen for interactive input
        try:
            process = subprocess.Popen(
                ["python", "manage.py", "createsuperuser"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("✅ Superuser creation initiated")
            print("📝 You can create a superuser manually later with:")
            print("   python manage.py createsuperuser")
        except Exception as e:
            print(f"❌ Error creating superuser: {e}")
    
    return True

def main():
    """Main installation function"""
    print("🚀 PhotoShare Installation Script")
    print("This script will set up the PhotoShare photography project")
    
    # Check prerequisites
    print_step(1, "Checking Prerequisites")
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_installed():
        sys.exit(1)
    
    # Create virtual environment
    print_step(2, "Setting up Virtual Environment")
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install Python dependencies
    print_step(3, "Installing Python Dependencies")
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Set up Tailwind CSS
    print_step(4, "Setting up Tailwind CSS")
    if not setup_tailwind():
        print("❌ Failed to set up Tailwind CSS")
        sys.exit(1)
    
    # Set up database
    print_step(5, "Setting up Database")
    if not setup_database():
        print("❌ Failed to set up database")
        sys.exit(1)
    
    # Collect static files
    print_step(6, "Collecting Static Files")
    if not collect_static_files():
        print("❌ Failed to collect static files")
        sys.exit(1)
    
    # Create superuser
    print_step(7, "Creating Superuser Account")
    create_superuser()
    
    # Final instructions
    print_step(8, "Installation Complete!")
    print("🎉 PhotoShare has been successfully installed!")
    print("\n📝 Next steps:")
    print("1. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   env\\Scripts\\activate")
    else:
        print("   source env/bin/activate")
    
    print("2. Start the development server:")
    print("   python manage.py runserver")
    
    print("3. Open your browser and visit:")
    print("   http://localhost:8000")
    
    print("\n📚 Additional Resources:")
    print("- README.md: Complete project documentation")
    print("- STATIC_FILES_SETUP.md: Static files configuration")
    print("- SEO_OPTIMIZATION.md: SEO implementation guide")
    
    print("\n🆘 Need help?")
    print("- Check the README.md file for detailed instructions")
    print("- Open an issue on GitHub for support")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1) 