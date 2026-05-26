from .models import SiteConfiguration, SocialLink


def site_context(request):
    try:
        config = SiteConfiguration.objects.first()
        social_links = SocialLink.objects.filter(is_active=True)
    except Exception:
        config = None
        social_links = []

    return {
        'site_config': config,
        'social_links': social_links,
    }

