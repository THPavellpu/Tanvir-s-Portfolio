# COMPLETE INSTALLATION & SETUP GUIDE

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Project Installation](#project-installation)
3. [Database Configuration](#database-configuration)
4. [Admin Panel Setup](#admin-panel-setup)
5. [Local Development](#local-development)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Environment Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 13+ (or SQLite for development)
- Git
- pip (Python package manager)
- Virtual environment support

### Step 1: System Setup

**Windows:**
```bash
# Download Python from python.org
# Download PostgreSQL from postgresql.org
# Add Python to PATH during installation
python --version
psql --version
```

**Mac:**
```bash
# Using Homebrew
brew install python@3.11
brew install postgresql
python3 --version
psql --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv postgresql postgresql-contrib
python3 --version
psql --version
```

### Step 2: Clone Repository

```bash
cd ~/projects  # Or your preferred directory
git clone https://github.com/yourusername/portfolio.git
cd portfolio
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
```

---

## Project Installation

### Step 1: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installations
pip list | grep -i django
```

### Step 2: Create Project Structure

```bash
# Run initialization script
python init_project.py

# Verify structure
ls -la  # On Mac/Linux
dir     # On Windows
```

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Windows: notepad .env
# Mac/Linux: nano .env
```

**Example .env Configuration:**

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Or PostgreSQL (recommended)
# DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Email Configuration (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-not-main-password

# Optional: GitHub API
GITHUB_TOKEN=your-github-token
GITHUB_USERNAME=your-github-username

# Site Configuration
SITE_URL=http://localhost:8000
SITE_NAME=Your Name
```

---

## Database Configuration

### Option 1: SQLite (Easy - Development Only)

No additional setup needed. Django uses SQLite by default.

```bash
# Run migrations
python manage.py migrate
```

### Option 2: PostgreSQL (Production Recommended)

**Step 1: Create Database**

```bash
# Windows (using Command Prompt with psql in PATH)
createdb portfolio_db

# Mac/Linux
createdb portfolio_db

# Or using psql:
psql
postgres=# CREATE DATABASE portfolio_db;
postgres=# CREATE USER portfolio_user WITH PASSWORD 'your_password';
postgres=# ALTER ROLE portfolio_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE portfolio_user SET default_transaction_isolation TO 'read committed';
postgres=# GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
postgres=# \q
```

**Step 2: Update .env**

```env
DATABASE_URL=postgresql://portfolio_user:your_password@localhost:5432/portfolio_db
```

**Step 3: Run Migrations**

```bash
python manage.py migrate
```

---

## Admin Panel Setup

### Step 1: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts for username, email, password
```

### Step 2: Initialize Default Data

```bash
python manage.py init_portfolio
# This creates skill categories, project categories, etc.
```

### Step 3: Access Admin

```bash
# Start development server
python manage.py runserver

# Visit http://localhost:8000/admin
# Login with superuser credentials
```

### Step 4: Add Content via Admin

1. **Site Configuration:**
   - Admin > Site Configuration > Add
   - Fill: Site Name, Tagline, Bio, Profile Image, Resume
   - Save

2. **Skills:**
   - Admin > Skills > Add
   - Add 10+ skills with categories
   - Mark some as featured

3. **Projects:**
   - Admin > Projects > Add
   - Upload project images
   - Add GitHub/Live links
   - Add technologies

4. **Blog Posts:**
   - Admin > Blogs > Add
   - Write content (Markdown supported)
   - Add featured image
   - Publish when ready

5. **Social Links:**
   - Admin > Social Links > Add
   - Add all social profiles

---

## Local Development

### Running the Development Server

```bash
# Make sure virtual environment is activated
# (venv) should appear in your prompt

# Run development server
python manage.py runserver

# Server runs at http://localhost:8000
# Admin at http://localhost:8000/admin
```

### Creating Database Migrations

```bash
# After modifying models
python manage.py makemigrations core

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Collecting Static Files

```bash
# Collect all static files
python manage.py collectstatic --noinput

# Files go to /staticfiles/ directory
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test core.tests.ProjectModelTest

# With verbose output
python manage.py test --verbosity=2
```

### Django Shell

```bash
# Open Django shell for testing
python manage.py shell

# Example queries:
from core.models import Project
projects = Project.objects.all()
project = Project.objects.first()
project.views
```

### Creating Fixtures (Data Backup)

```bash
# Export data to JSON
python manage.py dumpdata core > data.json

# Load data from JSON
python manage.py loaddata data.json
```

---

## Deployment

### Preparing for Production

**Step 1: Update Settings**

```python
# In settings.py or .env
DEBUG = False
SECRET_KEY = 'your-very-secret-key-generated'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

**Step 2: Verify Everything**

```bash
# Check for issues
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test
```

### Deploy to Render.com

**Step 1: Push to GitHub**

```bash
git add .
git commit -m "Portfolio deployment ready"
git push origin main
```

**Step 2: Create Render Web Service**

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" > "Web Service"
4. Select your repository
5. Configure:
   - Name: portfolio
   - Environment: Python
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn portfolio.wsgi:application`
   - Plan: Free tier

**Step 3: Set Environment Variables**

In Render dashboard > Environment:

```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=portfolio.onrender.com,yourdomain.com
DATABASE_URL=postgresql://...
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Step 4: Run Migrations on Deployment**

In Render > Settings:
- Pre-deploy Command: `python manage.py migrate`

**Step 5: Setup Custom Domain**

1. Purchase domain (Namecheap, GoDaddy, etc.)
2. Render > Settings > Custom Domains
3. Add your domain
4. Update DNS records (Render provides instructions)

### Deploy to VPS (Optional)

For self-hosted VPS deployment, see included `deployment/` files.

---

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError: No module named 'django'**
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

**Issue: Database connection refused**
```bash
# Check PostgreSQL is running
# On Mac: brew services start postgresql
# On Linux: sudo service postgresql start
# On Windows: Start PostgreSQL service in Services.msc

# Verify DATABASE_URL in .env
```

**Issue: Port 8000 already in use**
```bash
# Run on different port
python manage.py runserver 8001

# Or kill process using port:
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

**Issue: Static files not loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL in settings
```

**Issue: Email not sending**
```bash
# Check EMAIL_* variables in .env
# For Gmail: Use App-Specific Password, not main password
# Enable "Less secure app access" if not using app password
# Check spam folder
```

**Issue: Admin panel not accessible**
```bash
# Create new superuser
python manage.py createsuperuser

# Clear sessions
python manage.py clearsessions
```

**Issue: Migration conflicts**
```bash
# Check migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate core 0001

# Create new migration
python manage.py makemigrations
python manage.py migrate
```

### Debugging Tips

**Enable Debug Mode**
```python
# In .env
DEBUG=True

# More detailed error messages
```

**Check Logs**
```bash
# View logs
tail -f logs/django.log

# On Windows
type logs/django.log
```

**Database Queries**
```python
# In Django shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    # Your code here
    pass

print(f'Queries: {len(queries)}')
for query in queries:
    print(query['sql'])
```

---

## Performance Optimization

### Database Optimization

```bash
# Analyze query performance
python manage.py shell

from django.db import connection
from django.db.models import F
# Run queries and check connection.queries
```

### Static Files Optimization

```bash
# Minify CSS/JS (install django-compressor)
pip install django-compressor

# Generate gzipped versions
python manage.py collectstatic --compress
```

### Caching Configuration

Already configured in `settings.py`. For production, consider:
- Redis (better performance)
- Memcached (alternative)

### Image Optimization

```bash
# Use Pillow for automatic optimization
pip install Pillow

# Add to Project model:
# thumbnail = OptimizedImageField(...)
```

---

## Monitoring & Maintenance

### Regular Tasks

```bash
# Weekly: Backup database
python manage.py dumpdata core > backups/backup_$(date +%Y%m%d).json

# Monthly: Check for updates
pip list --outdated

# Clear expired sessions
python manage.py clearsessions
```

### Performance Monitoring

- Use Google PageSpeed Insights
- Monitor with Sentry (error tracking)
- Track with Google Analytics
- Monitor uptime with UptimeRobot

### Security

- Change SECRET_KEY regularly
- Update dependencies
- Review admin logs
- Enable 2FA on Render
- Regular security scans

---

## Support & Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Render Documentation](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Useful Commands Cheatsheet

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Flush database
python manage.py flush

# Load data
python manage.py loaddata data.json

# Dump data
python manage.py dumpdata > data.json

# Shell access
python manage.py shell

# Run tests
python manage.py test

# Check deployment
python manage.py check --deploy
```

---

## Next Steps

1. ✅ Complete this installation guide
2. ✅ Set up and configure Django
3. ✅ Add your portfolio content via admin
4. ✅ Customize design and branding
5. ✅ Test all features thoroughly
6. ✅ Deploy to Render.com
7. ✅ Configure custom domain
8. ✅ Monitor and maintain

---

## Getting Help

If you encounter issues:
1. Check the Troubleshooting section
2. Review Django documentation
3. Check Render documentation
4. Search Stack Overflow
5. Create GitHub issues

Happy coding! 🚀
