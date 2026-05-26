from django.http import HttpResponse
from django.urls import path


def robots_txt(request):
    return HttpResponse(
        """User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: http://example.com/sitemap.xml\n""",
        content_type="text/plain",
    )


urlpatterns = [
    path('', robots_txt, name='robots_txt'),
]

