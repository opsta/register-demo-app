#!/usr/bin/env python3
"""
Dependency management script for register-demo-app
"""
import subprocess
import sys
import os

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e}")
        return None

def install_dev_deps():
    """Install development dependencies"""
    print("Installing development dependencies...")
    result = run_command("pip install -r requirements-dev.txt")
    if result and result.returncode == 0:
        print("Development dependencies installed successfully!")
    else:
        print("Failed to install development dependencies")

def update_lockfile():
    """Update the requirements.txt lockfile"""
    print("Updating lockfile...")
    result = run_command("pip-compile requirements.in --upgrade")
    if result and result.returncode == 0:
        print("Lockfile updated successfully!")
    else:
        print("Failed to update lockfile")

def sync_deps():
    """Sync dependencies with the lockfile"""
    print("Syncing dependencies...")
    result = run_command("pip-sync requirements.txt")
    if result and result.returncode == 0:
        print("Dependencies synced successfully!")
    else:
        print("Failed to sync dependencies")

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_deps.py [install-dev|update-lock|sync]")
        print("  install-dev: Install development dependencies")
        print("  update-lock: Update the requirements.txt lockfile")
        print("  sync: Sync dependencies with the lockfile")
        return

    command = sys.argv[1]
    
    if command == "install-dev":
        install_dev_deps()
    elif command == "update-lock":
        update_lockfile()
    elif command == "sync":
        sync_deps()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
