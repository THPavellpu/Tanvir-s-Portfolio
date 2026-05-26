#!/usr/bin/env python
"""
Complete Django Portfolio Project Generator
This script generates all necessary files for the portfolio project
"""

import os
from pathlib import Path

def generate_project():
    base_dir = Path.cwd() / 'portfolio_project'
    
    files_to_create = {
        # Project structure directories
        'portfolio/__init__.py': '',
        'portfolio/asgi.py': '''"""
ASGI config for portfolio project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
application = get_asgi_application()
''',
        'portfolio/wsgi.py': '''"""
WSGI config for portfolio project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
application = get_wsgi_application()
''',
        'portfolio/urls.py': '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProjectSitemap, BlogSitemap, StaticSitemap

sitemaps = {
    'projects': ProjectSitemap,
    'blog': BlogSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
''',
        'core/__init__.py': '',
        'core/migrations/__init__.py': '',
        'templates/__init__.py': '',
        'static/__init__.py': '',
        '.gitignore': '''*.pyc
__pycache__/
*.egg-info/
dist/
build/
.env
.venv
env/
venv/
db.sqlite3
/media/
/staticfiles/
/logs/
.DS_Store
*.log
.idea/
.vscode/
*.swp
''',
        'manage.py': '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is not installed") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
''',
    }
    
    print("Files to create:")
    for file_path in files_to_create:
        print(f"  - {file_path}")

if __name__ == '__main__':
    generate_project()
