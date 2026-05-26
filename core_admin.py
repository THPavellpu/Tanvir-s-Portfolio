"""
Django Admin Configuration for Portfolio CMS
Optimized admin interface with rich editing and media previews
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
import core.models as core_models


@admin.register(core_models.SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline_preview', 'email', 'updated_at')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline', 'bio', 'profile_image')
        }),
        ('Branding', {
            'fields': ('primary_color', 'secondary_color'),
            'classes': ('collapse',)
        }),
        ('Files', {
            'fields': ('resume_file',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
    )
    
    def tagline_preview(self, obj):
        return obj.tagline[:50] if obj.tagline else '—'
    tagline_preview.short_description = 'Tagline'


@admin.register(core_models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform_badge', 'url_preview', 'display_order', 'is_active')
    list_filter = ('platform', 'is_active')
    list_editable = ('display_order', 'is_active')
    ordering = ('display_order',)
    
    def platform_badge(self, obj):
        color_map = {
            'github': '#181717',
            'linkedin': '#0077b5',
            'twitter': '#1da1f2',
            'instagram': '#e4405f',
            'email': '#ea4335',
        }
        color = color_map.get(obj.platform, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_platform_display()
        )
    platform_badge.short_description = 'Platform'
    
    def url_preview(self, obj):
        return obj.url[:40] + '...' if len(obj.url) > 40 else obj.url
    url_preview.short_description = 'URL'


@admin.register(core_models.SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'skill_count', 'display_order')
    list_editable = ('display_order',)
    ordering = ('display_order',)
    
    def skill_count(self, obj):
        count = obj.skills.count()
        return format_html(
            '<span style="background-color: #3b82f6; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    skill_count.short_description = 'Skills'


@admin.register(core_models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_badge', 'is_featured', 'display_order')
    list_filter = ('category', 'proficiency', 'is_featured')
    list_editable = ('display_order', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ('-is_featured', 'display_order')
    fieldsets = (
        ('Skill Information', {
            'fields': ('name', 'category', 'icon', 'description')
        }),
        ('Details', {
            'fields': ('proficiency', 'is_featured', 'display_order')
        }),
    )
    
    def proficiency_badge(self, obj):
        colors = {1: '#ef4444', 2: '#f97316', 3: '#3b82f6', 4: '#22c55e'}
        color = colors.get(obj.proficiency, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_proficiency_display()
        )
    proficiency_badge.short_description = 'Proficiency'


@admin.register(core_models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def project_count(self, obj):
        count = obj.projects.count()
        return format_html(
            '<span style="background-color: #8b5cf6; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    project_count.short_description = 'Projects'


@admin.register(core_models.ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview', 'slug', 'usage_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border-radius: 3px; border: 1px solid #ddd;"></span>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def usage_count(self, obj):
        count = obj.projects.count()
        return format_html(
            '<span style="background-color: #ec4899; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    usage_count.short_description = 'Used In'


@admin.register(core_models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_with_thumbnail', 'status_badge', 'project_type', 'featured_badge', 'views', 'updated_at')
    list_filter = ('status', 'project_type', 'category', ('technologies', RelatedDropdownFilter), 'is_featured')
    search_fields = ('title', 'description', 'technologies__name')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'detailed_description', 'category', 'project_type')
        }),
        ('Media', {
            'fields': ('thumbnail', 'images')
        }),
        ('Technologies & Details', {
            'fields': ('technologies', 'status', 'start_date', 'end_date')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'demo_url')
        }),
        ('Metadata', {
            'fields': ('is_featured', 'display_order', 'meta_description', 'views')
        }),
    )
    
    filter_horizontal = ('technologies',)
    readonly_fields = ('views',)
    ordering = ('-is_featured', '-display_order', '-updated_at')
    
    def title_with_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; border-radius: 3px; margin-right: 10px;"/><strong>{}</strong>',
                obj.thumbnail.url,
                obj.title
            )
        return obj.title
    title_with_thumbnail.short_description = 'Project'
    
    def status_badge(self, obj):
        colors = {
            'completed': '#22c55e',
            'ongoing': '#3b82f6',
            'archived': '#6b7280',
            'planned': '#f59e0b'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background-color: #f97316; color: white; padding: 3px 8px; border-radius: 3px;">⭐ Featured</span>'
            )
        return '—'
    featured_badge.short_description = 'Featured'


@admin.register(core_models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_or_issuer', 'experience_type_badge', 'duration_text', 'display_order')
    list_filter = ('experience_type', ('start_date', RelatedDropdownFilter), 'is_current')
    search_fields = ('title', 'company_or_issuer', 'description')
    list_editable = ('display_order',)
    ordering = ('-display_order', '-start_date')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company_or_issuer', 'experience_type', 'location')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('description', 'technologies', 'achievements')
        }),
        ('Links', {
            'fields': ('company_url', 'certificate_url')
        }),
        ('Display', {
            'fields': ('display_order',)
        }),
    )
    
    def experience_type_badge(self, obj):
        colors = {
            'job': '#3b82f6',
            'internship': '#8b5cf6',
            'freelance': '#ec4899',
            'project': '#f59e0b',
            'certification': '#22c55e',
            'achievement': '#06b6d4'
        }
        color = colors.get(obj.experience_type, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_experience_type_display()
        )
    experience_type_badge.short_description = 'Type'


@admin.register(core_models.BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        count = obj.posts.count()
        return format_html(
            '<span style="background-color: #3b82f6; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    post_count.short_description = 'Posts'


@admin.register(core_models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'author', 'category', 'status_badge', 'views', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category', 'published_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'likes', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Engagement', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_preview(self, obj):
        return obj.title[:60] + '...' if len(obj.title) > 60 else obj.title
    title_preview.short_description = 'Title'
    
    def status_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background-color: #22c55e; color: white; padding: 3px 8px; border-radius: 3px;">📖 Published</span>'
            )
        return format_html(
            '<span style="background-color: #f59e0b; color: white; padding: 3px 8px; border-radius: 3px;">Draft</span>'
        )
    status_badge.short_description = 'Status'


@admin.register(core_models.BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'blog_link', 'approval_status', 'created_at')
    list_filter = ('is_approved', 'is_spam', 'blog', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_comments', 'mark_as_spam']
    
    fieldsets = (
        ('Author', {
            'fields': ('author_name', 'author_email')
        }),
        ('Comment', {
            'fields': ('blog', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_spam')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def blog_link(self, obj):
        return format_html(
            '<a href="/admin/core/blog/{}/change/">{}</a>',
            obj.blog.id,
            obj.blog.title[:40]
        )
    blog_link.short_description = 'Blog Post'
    
    def approval_status(self, obj):
        if obj.is_spam:
            return format_html(
                '<span style="background-color: #ef4444; color: white; padding: 3px 8px; border-radius: 3px;">🚫 Spam</span>'
            )
        elif obj.is_approved:
            return format_html(
                '<span style="background-color: #22c55e; color: white; padding: 3px 8px; border-radius: 3px;">✓ Approved</span>'
            )
        return format_html(
            '<span style="background-color: #f59e0b; color: white; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
        )
    approval_status.short_description = 'Status'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True, is_spam=False)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True, is_approved=False)
        self.message_user(request, f'{queryset.count()} comments marked as spam.')
    mark_as_spam.short_description = 'Mark as spam'


@admin.register(core_models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'version_badge', 'is_current_badge', 'file_preview', 'uploaded_at')
    readonly_fields = ('version', 'uploaded_at', 'updated_at')
    ordering = ('-is_current', '-version')
    
    def version_badge(self, obj):
        return format_html(
            '<span style="background-color: #3b82f6; color: white; padding: 3px 8px; border-radius: 3px;">v{}</span>',
            obj.version
        )
    version_badge.short_description = 'Version'
    
    def is_current_badge(self, obj):
        if obj.is_current:
            return format_html(
                '<span style="background-color: #22c55e; color: white; padding: 3px 8px; border-radius: 3px;">✓ Current</span>'
            )
        return '—'
    is_current_badge.short_description = 'Current'
    
    def file_preview(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">📄 Download</a>',
                obj.file.url
            )
        return '—'
    file_preview.short_description = 'File'


@admin.register(core_models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_preview', 'status_badge', 'created_at')
    list_filter = ('is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_read', 'mark_as_replied']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_preview(self, obj):
        return obj.subject[:60] + '...' if len(obj.subject) > 60 else obj.subject
    subject_preview.short_description = 'Subject'
    
    def status_badge(self, obj):
        if obj.is_replied:
            return format_html(
                '<span style="background-color: #22c55e; color: white; padding: 3px 8px; border-radius: 3px;">✓ Replied</span>'
            )
        elif obj.is_read:
            return format_html(
                '<span style="background-color: #3b82f6; color: white; padding: 3px 8px; border-radius: 3px;">👁️ Read</span>'
            )
        return format_html(
            '<span style="background-color: #f59e0b; color: white; padding: 3px 8px; border-radius: 3px;">🔔 New</span>'
        )
    status_badge.short_description = 'Status'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True, is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as replied.')
    mark_as_replied.short_description = 'Mark as replied'


@admin.register(core_models.ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ('project', 'ip_address', 'viewed_at')
    list_filter = ('project', 'viewed_at')
    search_fields = ('project__title', 'ip_address')
    readonly_fields = ('viewed_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# Custom Admin Site Configuration
admin.site.site_header = "Portfolio CMS Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Admin"
