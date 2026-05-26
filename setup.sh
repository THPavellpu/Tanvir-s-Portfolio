#!/bin/bash
# Setup script for Django Portfolio Project

echo "Creating Django Portfolio Project Structure..."

# Create project directories
mkdir -p portfolio/portfolio
mkdir -p portfolio/core/migrations
mkdir -p portfolio/templates/core
mkdir -p portfolio/static/{css,js,images}
mkdir -p portfolio/media/{projects,resume,blog}
mkdir -p portfolio/logs
mkdir -p portfolio/deployment

echo "Django Portfolio project structure created successfully!"
echo ""
echo "Next steps:"
echo "1. pip install -r requirements.txt"
echo "2. cp .env.example .env"
echo "3. Update .env with your configuration"
echo "4. python manage.py migrate"
echo "5. python manage.py createsuperuser"
echo "6. python manage.py runserver"
