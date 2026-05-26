#!/usr/bin/env python
"""
Setup script for Django Portfolio Project
Creates full project structure and initial files
"""

import os
import sys
from pathlib import Path

def create_structure():
    """Create the Django project structure"""
    
    base_dir = Path(__file__).parent
    
    # Directory structure to create
    directories = [
        'portfolio',
        'core',
        'core/migrations',
        'templates',
        'templates/core',
        'templates/core/includes',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'media',
        'media/projects',
        'media/resume',
        'media/blog',
        'logs',
        'deployment',
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory}")
    
    print("\n✓ Project structure created successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and update configuration")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py createsuperuser")
    print("5. Run: python manage.py runserver")

if __name__ == '__main__':
    create_structure()
