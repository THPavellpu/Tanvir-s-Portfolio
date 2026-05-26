"""
Core Django Models for Portfolio CMS
Comprehensive data models for all portfolio features
"""

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
import markdown

class SiteConfiguration(models.Model):
    """Global site configuration"""
    site_name = models.CharField(max_length=200, default='Portfolio')
    tagline = models.CharField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Social Media
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Theme
    primary_color = models.CharField(max_length=7, default='#3b82f6')
    secondary_color = models.CharField(max_length=7, default='#8b5cf6')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name

class SocialLink(models.Model):
    """Social media and contact links"""
    PLATFORM_CHOICES = (
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('website', 'Website'),
        ('codepen', 'CodePen'),
        ('dribbble', 'Dribbble'),
        ('behance', 'Behance'),
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome or custom icon class")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"


class SkillCategory(models.Model):
    """Skill categories for organization"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "Skill Categories"
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skills with proficiency"""
    PROFICIENCY_CHOICES = (
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES, default=3)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class or image URL")
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-is_featured']
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"


class ProjectCategory(models.Model):
    """Project categorization"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Project Categories"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ProjectTechnology(models.Model):
    """Technology tags for projects"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    color = models.CharField(max_length=7, default='#3b82f6')
    
    class Meta:
        verbose_name_plural = "Project Technologies"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects with full details"""
    PROJECT_TYPE_CHOICES = (
        ('web', 'Web Application'),
        ('mobile', 'Mobile App'),
        ('desktop', 'Desktop App'),
        ('ml', 'Machine Learning'),
        ('iot', 'IoT Project'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('archived', 'Archived'),
        ('planned', 'Planned'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    
    # Media
    thumbnail = models.ImageField(upload_to='projects/')
    images = models.ImageField(upload_to='projects/', blank=True, null=True, help_text="Gallery images separated by comma")
    
    # Project Details
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    technologies = models.ManyToManyField(ProjectTechnology, related_name='projects')
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='web')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Links
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Engagement
    views = models.IntegerField(default=0)
    
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-display_order', '-created_at']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/projects/{self.slug}/"


class Experience(models.Model):
    """Professional experience, internships, and certifications"""
    EXPERIENCE_TYPE_CHOICES = (
        ('job', 'Job'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('project', 'Project'),
        ('certification', 'Certification'),
        ('achievement', 'Achievement'),
    )
    
    title = models.CharField(max_length=200)
    company_or_issuer = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES, default='job')
    
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated list")
    achievements = models.TextField(blank=True)
    
    # Links
    certificate_url = models.URLField(blank=True)
    company_url = models.URLField(blank=True)
    
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-display_order', '-start_date']
        verbose_name_plural = "Experience"
    
    def __str__(self):
        return f"{self.title} at {self.company_or_issuer}"
    
    @property
    def duration_text(self):
        from datetime import datetime
        end = self.end_date or datetime.now().date()
        delta = end - self.start_date
        months = delta.days // 30
        years = months // 12
        months = months % 12
        
        if years > 0:
            return f"{years}y {months}m"
        return f"{months}m"


class BlogCategory(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Blog(models.Model):
    """Blog posts with rich content"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to='blog/')
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/blog/{self.slug}/"
    
    @property
    def content_html(self):
        return markdown.markdown(self.content)
    
    @property
    def reading_time(self):
        word_count = len(self.content.split())
        return max(1, word_count // 200)


class BlogComment(models.Model):
    """Comments on blog posts with moderation"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.blog.title}"


class Resume(models.Model):
    """Resume file management"""
    title = models.CharField(max_length=200, default='Resume')
    file = models.FileField(upload_to='resume/')
    version = models.IntegerField(default=1)
    is_current = models.BooleanField(default=False)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_current', '-version']
    
    def save(self, *args, **kwargs):
        if self.is_current:
            Resume.objects.exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Resume v{self.version}"


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class ProjectView(models.Model):
    """Track project views for analytics"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='view_logs')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.project.title} - viewed at {self.viewed_at}"
