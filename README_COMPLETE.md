# Production Django Portfolio CMS

A modern, professional, production-ready personal portfolio platform built with Django, featuring a dynamic CMS-driven architecture, modern design, and complete recruiter optimization.

## 🎯 Key Features

- **Dynamic CMS**: Manage all portfolio content from Django admin panel
- **Modern Design**: Dark mode with light toggle, smooth animations, premium styling
- **Fully Responsive**: Mobile-first design, works on all devices
- **SEO Optimized**: Meta tags, structured data, sitemap, robots.txt
- **High Performance**: Lazy loading, image optimization, caching ready
- **Blog System**: Full blogging with comments (moderation-enabled)
- **Project Showcase**: Featured projects with tech stacks, live demos, GitHub links
- **GitHub Integration**: Auto-fetch repositories (API integration ready)
- **Contact Form**: Email-enabled contact form with validation
- **Analytics Ready**: Project view tracking, engagement metrics
- **Production Ready**: Gunicorn, Nginx configs, environment variables

## 📋 Tech Stack

- **Backend**: Django 4.2+, Django REST Framework, PostgreSQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no dependencies)
- **Deployment**: Render.com, Gunicorn, Nginx
- **Media**: Cloudinary optional, local storage ready
- **Security**: CSRF, XSS protection, secure headers

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd portfolio

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create project structure
python init_project.py

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` with your settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Email (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# GitHub API (optional)
GITHUB_TOKEN=your-github-token
GITHUB_USERNAME=your-username

# Site
SITE_URL=http://localhost:8000
SITE_NAME=Your Name
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb portfolio_db

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. Run Development Server

```bash
python manage.py runserver

# Visit http://localhost:8000
# Admin: http://localhost:8000/admin
```

## 📁 Project Structure

```
portfolio/
├── portfolio/              # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI app
│   └── asgi.py            # ASGI app
├── core/                  # Main app with models & logic
│   ├── models.py          # Database models
│   ├── admin.py           # Django admin config
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   ├── forms.py           # Forms
│   ├── serializers.py     # REST serializers
│   └── sitemaps.py        # XML sitemaps
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── core/
│   │   ├── index.html     # Home page
│   │   ├── projects.html  # Projects list
│   │   ├── blog.html      # Blog list
│   │   ├── resume.html    # Resume page
│   │   ├── contact.html   # Contact form
│   │   └── includes/      # Template includes
│   └── admin/             # Custom admin templates
├── static/                # Static files
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   ├── js/
│   │   └── main.js        # JavaScript
│   └── images/
├── media/                 # User uploads
│   ├── projects/
│   ├── blog/
│   └── resume/
├── logs/                  # Log files
├── deployment/            # Render, Nginx configs
├── manage.py
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── README.md
```

## 🛠️ Admin Panel Usage

### Adding Skills
1. Go to Admin > Skills
2. Click "Add Skill"
3. Fill in: Name, Category, Proficiency, Icon (Font Awesome class)
4. Save and reorder using the list display

### Adding Projects
1. Go to Admin > Projects
2. Click "Add Project"
3. Fill in all fields:
   - Title, Description, Detailed Description
   - Upload thumbnail image
   - Add technologies (multi-select)
   - Add links (GitHub, Live, Demo)
   - Mark as featured if needed
4. Save

### Creating Blog Posts
1. Go to Admin > Blogs
2. Click "Add Blog"
3. Fill in:
   - Title, Slug (auto-filled)
   - Content (supports Markdown)
   - Featured image
   - Category
   - Meta description for SEO
4. Publish when ready
5. Moderate comments in Admin > Blog Comments

### Managing Resume
1. Go to Admin > Resumes
2. Upload new PDF
3. Mark as "Current" (old one auto-deactivated)
4. Version auto-increments

## 📊 Database Models

### Core Models

- **SiteConfiguration**: Global site settings
- **Skill**: Skills with categories and proficiency
- **SkillCategory**: Skill grouping
- **Project**: Portfolio projects with full details
- **ProjectCategory**: Project type grouping
- **ProjectTechnology**: Tech stack tags
- **Experience**: Work history, internships, certifications
- **Blog**: Blog posts with rich content
- **BlogCategory**: Blog categorization
- **BlogComment**: Comments with moderation
- **Resume**: Resume file management
- **ContactMessage**: Contact form submissions
- **SocialLink**: Social media links
- **ProjectView**: Analytics tracking

## 🌐 SEO Optimization

### Implemented

- ✅ Meta titles and descriptions on all pages
- ✅ Structured data (Schema.org) for projects and blog
- ✅ Open Graph tags for social sharing
- ✅ Twitter Card tags
- ✅ Canonical URLs
- ✅ XML Sitemap (auto-generated)
- ✅ robots.txt
- ✅ Semantic HTML5
- ✅ Optimized heading hierarchy
- ✅ Image alt tags
- ✅ Lazy loading images
- ✅ Mobile responsive (100% mobile-first)

### To Verify SEO

```bash
# Check sitemap
python manage.py sitemap

# Test robots.txt
curl http://localhost:8000/robots.txt

# Use Google PageSpeed Insights
# https://pagespeed.web.dev
```

## 🚀 Deployment to Render.com

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial portfolio commit"
git push origin main
```

### 2. Create Render Account

Visit [render.com](https://render.com) and sign up with GitHub

### 3. Create Web Service

1. Click "New +" > "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: portfolio
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn portfolio.wsgi:application`
   - **Plan**: Free tier okay for portfolio

### 4. Environment Variables

Set in Render dashboard:

```
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com,www.your-domain.com
DATABASE_URL=postgresql://...
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup

```bash
# SSH into Render service
render-shell

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Custom Domain (Optional)

1. Purchase domain (Namecheap, GoDaddy, etc.)
2. In Render > Settings > Custom Domains
3. Add your domain and update DNS records

## 🔐 Security Checklist

Before production deployment:

- [ ] Change `SECRET_KEY` to a strong random string
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Configure email credentials
- [ ] Set strong admin password
- [ ] Enable HTTPS (Render does automatically)
- [ ] Review `SECURE_*` settings in settings.py
- [ ] Set up database backups
- [ ] Monitor logs
- [ ] Enable admin audit logging

## 📈 Performance Optimization

### Implemented

- ✅ Static files served via WhiteNoise
- ✅ Database query optimization
- ✅ Image lazy loading
- ✅ CSS/JS minification ready
- ✅ Gzip compression
- ✅ Browser caching headers

### Additional

```bash
# Minify CSS (optional)
python -m pip install django-compressor

# Image optimization (optional)
pip install Pillow

# Database indexing already configured
```

### Performance Targets

- Lighthouse Score: 90+
- First Contentful Paint: < 2s
- Largest Contentful Paint: < 3s
- Cumulative Layout Shift: < 0.1

## 🎨 Customization

### Colors

Edit `static/css/styles.css` CSS variables:

```css
:root {
    --primary: #3b82f6;        /* Blue */
    --secondary: #8b5cf6;      /* Purple */
    --accent: #ec4899;         /* Pink */
}
```

### Fonts

Currently using "Poppins" and "JetBrains Mono" from Google Fonts. Change in `base.html`

### Themes

Toggle between dark/light modes (enabled by default). Users can toggle via moon icon.

## 📚 Additional Features

### GitHub Integration

```python
# In settings.py
GITHUB_TOKEN = 'your-token'
GITHUB_USERNAME = 'your-username'

# Get latest repos
from core.utils import get_github_repos
repos = get_github_repos()
```

### Blog Features

- Markdown support
- Code syntax highlighting
- Related posts
- Reading time estimate
- Comment moderation
- Analytics (views, likes)

### Analytics

Track in admin panel:
- Project views
- Contact form submissions
- Blog engagement

## 🐛 Troubleshooting

### Database Issues

```bash
# Reset database (development only!)
python manage.py flush
python manage.py migrate

# Backup database
pg_dump portfolio_db > backup.sql
```

### Static Files Not Loading

```bash
# Rebuild static files
python manage.py collectstatic --noinput
```

### Email Not Sending

- Check EMAIL_* environment variables
- Use App-specific password (Gmail)
- Check spam folder
- Verify SMTP settings

### Migration Issues

```bash
# Create new migration
python manage.py makemigrations core

# Check migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate core 0001
```

## 📚 Documentation Files

Included in repository:
- API documentation (if using DRF)
- Admin guide
- Deployment guide
- Customization guide

## 🤝 Contributing

To add features or improvements:

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For issues and questions:
- Check troubleshooting section
- Review Django documentation
- Check Render documentation
- Create GitHub issue

## 🎉 Next Steps

1. **Customize**: Update colors, fonts, and content in admin
2. **Add Projects**: Upload your portfolio projects
3. **Write Blog**: Share your knowledge
4. **Deploy**: Push to Render.com
5. **Monitor**: Check performance and analytics
6. **Promote**: Share your portfolio

## 📊 Performance Monitoring

Monitor production:

```bash
# Check logs in Render dashboard
# Set up Sentry for error tracking
# Use Google Analytics for traffic
# Monitor uptime with UptimeRobot
```

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Render Documentation](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Font Awesome Icons](https://fontawesome.com/)

---

Built with ❤️ for developers, recruiters, and hiring managers.
Last Updated: 2024
