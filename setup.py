"""Script to set up virtual environment, install dependencies, and run the app."""

import os
import subprocess
import sys
import platform


def main():
    """Set up the environment and run the application."""
    venv_dir = ".venv"
    is_windows = platform.system() == "Windows"

    # Paths for virtual environment
    if is_windows:
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_path = os.path.join(venv_dir, "bin", "python")
        pip_path = os.path.join(venv_dir, "bin", "pip")

    # Create virtual environment if it doesn't exist
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print("Virtual environment created.")

    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed.")

    # Run the application
    print("Starting the application...")
    subprocess.run([python_path, "main.py"], check=True)


if __name__ == "__main__":
    main()