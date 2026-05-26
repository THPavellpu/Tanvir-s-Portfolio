from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    # Home
    path("", views.IndexView.as_view(), name="index"),

    # Projects
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("projects/api/filter/", views.ProjectFilterAPIView.as_view(), name="project_filter_api"),

    # Blog
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("blog/<slug:slug>/comment/", views.BlogCommentCreateView.as_view(), name="blog_comment"),
    path("blog/api/search/", views.BlogSearchAPIView.as_view(), name="blog_search_api"),

    # Resume
    path("resume/", views.ResumeView.as_view(), name="resume"),
    path("resume/download/", views.ResumeDownloadView, name="resume_download"),

    # Contact
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("contact/success/", views.ContactSuccessView.as_view(), name="contact_success"),

    # APIs
    path("api/skills/", views.SkillListAPIView.as_view(), name="api_skills"),
    path("api/projects/", views.ProjectListAPIView.as_view(), name="api_projects"),
    path("api/blog/", views.BlogListAPIView.as_view(), name="api_blog"),
]

