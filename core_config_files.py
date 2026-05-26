"""
Complete Django Portfolio Project - Additional Configuration Files
Copy sections to appropriate files after running init_project.py
"""

# ============================================================================
# FILE: core/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.IndexView.as_view(), name='index'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/api/filter/', views.ProjectFilterAPIView.as_view(), name='project_filter_api'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/comment/', views.BlogCommentCreateView.as_view(), name='blog_comment'),
    path('blog/api/search/', views.BlogSearchAPIView.as_view(), name='blog_search_api'),
    
    # Resume
    path('resume/', views.ResumeView.as_view(), name='resume'),
    
    # Contact
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    
    # APIs
    path('api/skills/', views.SkillListAPIView.as_view(), name='api_skills'),
    path('api/projects/', views.ProjectListAPIView.as_view(), name='api_projects'),
    path('api/blog/', views.BlogListAPIView.as_view(), name='api_blog'),
]

# ============================================================================
# FILE: core/views.py (Partial - Main Views)
# ============================================================================
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Project, Skill, Blog, Experience, Resume, ContactMessage,
    SkillCategory, BlogCategory, SiteConfiguration, SocialLink
)
from .forms import ContactForm, BlogCommentForm
from .serializers import (
    ProjectSerializer, SkillSerializer, BlogSerializer
)


class IndexView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:6]
        context['featured_skills'] = Skill.objects.filter(is_featured=True)[:12]
        context['featured_blog'] = Blog.objects.filter(is_published=True, is_featured=True).first()
        context['recent_blog'] = Blog.objects.filter(is_published=True)[:3]
        context['social_links'] = SocialLink.objects.filter(is_active=True)
        context['experiences'] = Experience.objects.all()[:5]
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'core/projects.html'
    context_object_name = 'projects'
    paginate_by = settings.ITEMS_PER_PAGE
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by type
        project_type = self.request.GET.get('type')
        if project_type:
            queryset = queryset.filter(project_type=project_type)
        
        # Search
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    slug_field = 'slug'
    context_object_name = 'project'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class BlogListView(ListView):
    model = Blog
    template_name = 'core/blog.html'
    context_object_name = 'posts'
    paginate_by = settings.BLOG_ITEMS_PER_PAGE
    
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['featured_post'] = Blog.objects.filter(is_published=True, is_featured=True).first()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'core/blog_detail.html'
    slug_field = 'slug'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_published:
            obj.views += 1
            obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Blog.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['comment_form'] = BlogCommentForm()
        return context


class BlogCommentCreateView(FormView):
    form_class = BlogCommentForm
    template_name = 'core/blog_detail.html'
    
    def form_valid(self, form):
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        return JsonResponse({'success': True, 'message': 'Comment submitted for moderation'})
    
    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class ResumeView(TemplateView):
    template_name = 'core/resume.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume'] = Resume.objects.filter(is_current=True).first()
        context['experiences'] = Experience.objects.all()
        return context


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = '/contact/success/'
    
    def form_valid(self, form):
        # Save message
        message = form.save()
        
        # Send email
        try:
            send_mail(
                subject=f"New Contact: {form.cleaned_data['subject']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            pass
        
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'core/contact_success.html'


# API Views
class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'category__name']


class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    pagination_class = None


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = None


class ProjectFilterAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        queryset = Project.objects.all()
        category = self.request.query_params.get('category')
        project_type = self.request.query_params.get('type')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if project_type:
            queryset = queryset.filter(project_type=project_type)
        
        return queryset


class BlogSearchAPIView(generics.ListAPIView):
    serializer_class = BlogSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Blog.objects.filter(
            is_published=True,
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:10]

# ============================================================================
# FILE: core/forms.py
# ============================================================================
from django import forms
from .models import ContactMessage, BlogComment


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'author_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment', 'rows': 4}),
        }

# ============================================================================
# FILE: core/serializers.py
# ============================================================================
from rest_framework import serializers
from .models import Project, Skill, Blog


class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category_name', 'proficiency', 'icon', 'description']


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    technologies = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'thumbnail', 'category_name', 'technologies', 'status', 'github_url', 'live_url']


class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'excerpt', 'author_name', 'category_name', 'featured_image', 'published_at', 'views']

# ============================================================================
# FILE: core/sitemaps.py
# ============================================================================
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Blog


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Project.objects.all()
    
    def lastmod(self, item):
        return item.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        return Blog.objects.filter(is_published=True)
    
    def lastmod(self, item):
        return item.published_at


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    
    def items(self):
        return ['index', 'projects', 'blog', 'resume', 'contact']
    
    def location(self, item):
        return reverse(f'core:{item}')

# ============================================================================
# FILE: core/context_processors.py
# ============================================================================
from .models import SiteConfiguration, SocialLink


def site_context(request):
    try:
        config = SiteConfiguration.objects.first()
        social_links = SocialLink.objects.filter(is_active=True)
    except:
        config = None
        social_links = []
    
    return {
        'site_config': config,
        'social_links': social_links,
    }

# ============================================================================
# FILE: core/robots.py
# ============================================================================
from django.urls import path
from django.http import HttpResponse

def robots_txt(request):
    return HttpResponse("""User-agent: *
Allow: /
Disallow: /admin/
Sitemap: http://example.com/sitemap.xml""", content_type="text/plain")

urlpatterns = [
    path('', robots_txt),
]
