# FILE: core/utils.py - Utility Functions

import requests
import os
from django.core.cache import cache
from django.conf import settings

def get_github_repos():
    """Fetch user's GitHub repositories"""
    if not settings.GITHUB_TOKEN or not settings.GITHUB_USERNAME:
        return []
    
    # Check cache first
    cache_key = f'github_repos_{settings.GITHUB_USERNAME}'
    repos = cache.get(cache_key)
    
    if repos:
        return repos
    
    try:
        headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
        url = f'https://api.github.com/users/{settings.GITHUB_USERNAME}/repos'
        params = {
            'sort': 'updated',
            'per_page': 10,
            'type': 'owner'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        
        repos = response.json()
        
        # Cache for 24 hours
        cache.set(cache_key, repos, 86400)
        
        return repos
    except Exception as e:
        print(f'Error fetching GitHub repos: {str(e)}')
        return []


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_contact_notification(contact_message):
    """Send notification email for new contact"""
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    
    try:
        context = {'message': contact_message}
        html_message = render_to_string('core/emails/contact_notification.html', context)
        
        send_mail(
            subject=f'New Contact Form Submission: {contact_message.subject}',
            message=f'{contact_message.name} ({contact_message.email}) sent: {contact_message.message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f'Error sending notification: {str(e)}')


def generate_sitemap_entries():
    """Generate sitemap entries for SEO"""
    from core.models import Project, Blog
    from django.urls import reverse
    
    entries = []
    
    # Add static pages
    entries.append({
        'url': '/',
        'changefreq': 'daily',
        'priority': 1.0
    })
    
    # Add projects
    for project in Project.objects.all():
        entries.append({
            'url': project.get_absolute_url(),
            'changefreq': 'weekly',
            'priority': 0.8,
            'lastmod': project.updated_at
        })
    
    # Add blog posts
    for blog in Blog.objects.filter(is_published=True):
        entries.append({
            'url': blog.get_absolute_url(),
            'changefreq': 'weekly',
            'priority': 0.7,
            'lastmod': blog.published_at
        })
    
    return entries


def validate_email_domain(email):
    """Validate email domain for spam prevention"""
    disposable_domains = [
        'tempmail.com',
        '10minutemail.com',
        'guerrillamail.com',
        'mailinator.com',
    ]
    
    domain = email.split('@')[1]
    return domain not in disposable_domains


def get_reading_time(text, words_per_minute=200):
    """Calculate reading time"""
    word_count = len(text.split())
    reading_time = max(1, word_count // words_per_minute)
    return reading_time


# FILE: core/signals.py - Django Signals

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import ContactMessage, Blog, BlogComment
from core.utils import send_contact_notification


@receiver(post_save, sender=ContactMessage)
def send_contact_email(sender, instance, created, **kwargs):
    """Send email when new contact message is created"""
    if created:
        send_contact_notification(instance)


@receiver(post_save, sender=Blog)
def update_blog_slug(sender, instance, **kwargs):
    """Auto-update slug when blog title changes"""
    from django.utils.text import slugify
    if not instance.slug:
        instance.slug = slugify(instance.title)
        instance.save()


@receiver(post_save, sender=BlogComment)
def notify_on_new_comment(sender, instance, created, **kwargs):
    """Notify admin of new blog comment"""
    if created:
        # Could send email notification
        pass


# Add to core/apps.py:
# from django.apps import AppConfig
#
# class CoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'core'
#
#     def ready(self):
#         import core.signals


# FILE: core/tests.py - Unit Tests

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Project, Blog, Skill, SkillCategory


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            thumbnail='test.jpg'
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Test Project')
        self.assertTrue(self.project.slug)

    def test_project_url(self):
        self.assertIn('/projects/', self.project.get_absolute_url())


class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            author=self.user,
            featured_image='test.jpg'
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertFalse(self.blog.is_published)

    def test_reading_time(self):
        self.blog.content = ' '.join(['word'] * 400)
        self.assertEqual(self.blog.reading_time, 2)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_projects_view(self):
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)

    def test_blog_view(self):
        response = self.client.get(reverse('core:blog'))
        self.assertEqual(response.status_code, 200)


# FILE: manage.py - Django Management Script (full version)

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# FILE: core/middleware.py - Custom Middleware

import time
from django.utils.deprecation import MiddlewareMixin


class TimingMiddleware(MiddlewareMixin):
    """Log request processing time"""
    
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Process-Time'] = str(duration)
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers"""
    
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'no-referrer-when-downgrade'
        return response


# FILE: Portfolio Setup Master Checklist

## Pre-Development
- [ ] Python 3.11+ installed
- [ ] PostgreSQL installed and running
- [ ] Git installed
- [ ] GitHub account created
- [ ] GitHub token generated (for API)
- [ ] Render account created

## Local Development Setup
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] init_project.py executed
- [ ] .env file created and configured
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Development server runs

## Content Setup (Admin Panel)
- [ ] Site configuration completed
- [ ] Skills added (at least 10)
- [ ] Skill categories set
- [ ] 3-5 projects added
- [ ] Project technologies added
- [ ] Experience entries created
- [ ] 2-3 blog posts written
- [ ] Resume uploaded
- [ ] Social links configured

## Frontend Customization
- [ ] Color scheme customized
- [ ] Profile image added
- [ ] Tagline updated
- [ ] Bio written
- [ ] Logo/branding finalized
- [ ] Mobile preview tested

## Testing
- [ ] All pages accessible
- [ ] Forms working (contact)
- [ ] Links working
- [ ] Images loading
- [ ] Responsive design tested
- [ ] Dark/light mode working
- [ ] Admin panel accessible
- [ ] Pagination working
- [ ] Search functionality tested

## SEO Verification
- [ ] Meta tags present
- [ ] Sitemap generated
- [ ] robots.txt accessible
- [ ] Structured data valid
- [ ] Mobile-friendly (Google Mobile-Friendly Test)
- [ ] Page speed acceptable (Lighthouse >90)

## Deployment Preparation
- [ ] Repository pushed to GitHub
- [ ] .env.example created
- [ ] Procfile created
- [ ] requirements.txt updated
- [ ] build.sh created
- [ ] Database backups configured
- [ ] Email configured for production
- [ ] Secret key changed
- [ ] DEBUG set to False

## Production Deployment
- [ ] Render project created
- [ ] Environment variables set
- [ ] Database migrated
- [ ] Superuser created on production
- [ ] Static files collected
- [ ] Domain configured
- [ ] SSL certificate active
- [ ] Database backup tested

## Post-Deployment
- [ ] Email notifications working
- [ ] Admin panel accessible
- [ ] Analytics tracking
- [ ] Performance monitoring set up
- [ ] Error logging configured
- [ ] Uptime monitoring active
