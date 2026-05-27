from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Project,
    Skill,
    Blog,
    Experience,
    Certification,
    Resume,
    ContactMessage,
    SkillCategory,
    BlogCategory,
    SiteConfiguration,
    SocialLink,
    ProjectCategory,
)
from .forms import ContactForm, BlogCommentForm
from .serializers import ProjectSerializer, SkillSerializer, BlogSerializer


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.filter(is_featured=True)[:6]
        context["featured_skills"] = Skill.objects.filter(is_featured=True)[:12]
        context["featured_blog"] = Blog.objects.filter(is_published=True, is_featured=True).first()
        context["recent_blog"] = Blog.objects.filter(is_published=True)[:3]
        context["social_links"] = SocialLink.objects.filter(is_active=True)
        context["experiences"] = Experience.objects.all()[:5]
        context["certifications"] = Certification.objects.all()[:8]

        # Landing image (admin-uploadable)
        context["landing_profile_image"] = SiteConfiguration.objects.first()
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "core/projects.html"
    context_object_name = "projects"
    paginate_by = settings.ITEMS_PER_PAGE

    def get_queryset(self):
        queryset = Project.objects.all()

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)

        project_type = self.request.GET.get("type")
        if project_type:
            queryset = queryset.filter(project_type=project_type)

        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset.order_by("-is_featured", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProjectCategory.objects.all()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "core/project_detail.html"
    slug_field = "slug"
    context_object_name = "project"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class BlogListView(ListView):
    model = Blog
    template_name = "core/blog.html"
    context_object_name = "posts"
    paginate_by = getattr(settings, "BLOG_ITEMS_PER_PAGE", 12)

    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)

        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))

        return queryset.order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = BlogCategory.objects.all()
        context["featured_post"] = Blog.objects.filter(is_published=True, is_featured=True).first()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = "core/blog_detail.html"
    slug_field = "slug"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_published:
            obj.views += 1
            obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = (
            Blog.objects.filter(
                is_published=True,
                category=self.object.category,
            )
            .exclude(id=self.object.id)[:3]
        )
        # Requires BlogComment model (already in models.py)

        context["comments"] = self.object.comments.filter(is_approved=True)
        context["comment_form"] = BlogCommentForm()
        return context


class BlogCommentCreateView(FormView):
    form_class = BlogCommentForm
    template_name = "core/blog_detail.html"

    def form_valid(self, form):
        blog = get_object_or_404(Blog, slug=self.kwargs["slug"])
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        return JsonResponse({"success": True, "message": "Comment submitted for moderation"})

    def form_invalid(self, form):
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


class ResumeView(TemplateView):
    template_name = "core/resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resume"] = Resume.objects.filter(is_current=True).first()
        context["experiences"] = Experience.objects.all()
        context["certifications"] = Certification.objects.all()
        return context


def ResumeDownloadView(request):
    """Handle resume file download.

    Fixes previous issues by:
    - Removing hardcoded filename (Resume26.pdf)
    - Serving local files via resume.file.path when available
    - For remote (e.g., Cloudinary) URLs, forcing attachment redirect when possible
    """

    from django.http import FileResponse, HttpResponse

    resume = Resume.objects.filter(is_current=True).first()
    if not resume or not resume.file:
        return redirect("/resume/")

    # 1) Local file (preferred)
    try:
        file_path = resume.file.path
        filename = resume.title or "resume"

        # Ensure extension
        if not any(filename.lower().endswith(ext) for ext in (".pdf", ".doc", ".docx")):
            filename += ".pdf"

        with open(file_path, "rb") as f:
            # Let FileResponse infer content_type; provide attachment filename
            response = FileResponse(f)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    except Exception:
        # Not a local path (or file missing) -> try URL redirect below
        pass

    # 2) Remote file URL fallback
    try:
        file_url = resume.file.url
        filename = resume.title or "resume"
        if not any(filename.lower().endswith(ext) for ext in (".pdf", ".doc", ".docx")):
            filename += ".pdf"

        # If it's Cloudinary, add fl_attachment to force download
        if "cloudinary" in file_url and "fl_attachment" not in file_url and "upload/" in file_url:
            file_url = file_url.replace("upload/", "upload/fl_attachment/")

        # Redirect is sufficient for browser download with fl_attachment.
        # (Avoid streaming remote bytes to prevent timeouts/URL issues.)
        resp = redirect(file_url)
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp
    except Exception:
        pass

    return redirect("/resume/")


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "core/contact.html"
    success_url = "/contact/success/"

    def form_valid(self, form):
        form.save()
        try:
            send_mail(
                subject=f"New Contact: {form.cleaned_data['subject']}",
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["email"],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception:
            pass
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "core/contact_success.html"


# API Views
class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "category__name"]


class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    pagination_class = None


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    pagination_class = None


class ProjectFilterAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        category = self.request.query_params.get("category")
        project_type = self.request.query_params.get("type")

        if category:
            queryset = queryset.filter(category__slug=category)
        if project_type:
            queryset = queryset.filter(project_type=project_type)

        return queryset


class BlogSearchAPIView(generics.ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        return Blog.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:10]


