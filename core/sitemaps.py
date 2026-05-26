from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Project


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, item):
        return getattr(item, 'updated_at', None)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, item):
        return getattr(item, 'published_at', None)


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['index', 'projects', 'blog', 'resume', 'contact']

    def location(self, item):
        return reverse(f'core:{item}')

