@echo off
REM Create directory structure for Django Portfolio Project
echo Creating Django Portfolio project structure...

mkdir portfolio
mkdir core
mkdir core\migrations
mkdir templates
mkdir templates\core
mkdir templates\core\includes
mkdir static
mkdir static\css
mkdir static\js
mkdir static\images
mkdir media
mkdir media\projects
mkdir media\resume
mkdir media\blog
mkdir logs
mkdir deployment

echo Project structure created successfully!
echo.
echo Next steps:
echo 1. pip install -r requirements.txt
echo 2. Copy .env.example to .env
echo 3. Update .env with your configuration
echo 4. python manage.py migrate
echo 5. python manage.py createsuperuser
echo 6. python manage.py runserver
