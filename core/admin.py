from django.contrib import admin

from .models import (
    SiteConfiguration,
    SocialLink,
    SkillCategory,
    Skill,
    ProjectCategory,
    ProjectTechnology,
    Project,
    Experience,
    Certification,
    BlogCategory,
    Blog,
    BlogComment,
    Resume,
    ContactMessage,
    ProjectView,
)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("site_name", "tagline", "created_at", "updated_at")
    search_fields = ("site_name", "tagline", "bio")
    # Make it easy to upload a landing profile image
    fieldsets = (
        (None, {
            'fields': (
                'site_name',
                'tagline',
                'bio',
                'profile_image',
                'resume_file',
            )
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        ('Contact', {
            'fields': ('email', 'phone'),
        }),
        ('Theme', {
            'fields': ('primary_color', 'secondary_color'),
        }),
    )



@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    ordering = ("display_order", "platform")
    search_fields = ("platform", "url")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name", "description", "icon")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_featured", "display_order")
    list_filter = ("category", "is_featured", "proficiency")
    list_editable = ("is_featured", "display_order")
    search_fields = ("name", "description", "icon")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name", "slug", "description")


@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    search_fields = ("name", "slug")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "project_type",
        "status",
        "is_featured",
        "views",
        "created_at",
    )
    list_filter = ("is_featured", "project_type", "status", "category")
    search_fields = ("title", "slug", "description", "github_url", "live_url", "demo_url")
    ordering = ("-is_featured", "-created_at")
    filter_horizontal = ("technologies",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_or_issuer",
        "experience_type",
        "role",
        "start_date",
        "end_date",
        "is_current",
        "display_order",
    )
    list_filter = ("experience_type", "is_current")
    search_fields = ("title", "company_or_issuer", "description", "technologies")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "platform", "issued_date", "display_order")
    list_filter = ("platform",)
    search_fields = ("name", "organization")


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name", "slug", "description")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "is_published",
        "is_featured",
        "views",
        "likes",
        "published_at",
    )
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "slug", "content", "excerpt")


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("author_name", "blog", "is_approved", "is_spam", "created_at")
    list_filter = ("is_approved", "is_spam")
    search_fields = ("author_name", "author_email", "content")
    actions = ["approve_comments", "mark_as_spam"]

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True, is_spam=False)

    @admin.action(description="Mark selected comments as spam")
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "is_current", "uploaded_at")
    list_filter = ("is_current",)
    search_fields = ("title",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "is_replied", "created_at")
    list_filter = ("is_read", "is_replied")
    search_fields = ("name", "email", "subject", "message")


@admin.register(ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ("project", "ip_address", "user_agent", "viewed_at")
    search_fields = ("ip_address", "user_agent", "project__title")

