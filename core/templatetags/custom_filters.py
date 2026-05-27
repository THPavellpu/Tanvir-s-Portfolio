from django import template

register = template.Library()


@register.filter
def force_download(url):
    """
    Add Cloudinary attachment flag to force download on mobile devices.
    Transforms: https://res.cloudinary.com/.../upload/v123/file.pdf
    To: https://res.cloudinary.com/.../upload/fl_attachment/v123/file.pdf
    """
    if not url:
        return url
    
    if "cloudinary" in url and "upload/" in url:
        # Check if attachment flag is already present
        if "fl_attachment" not in url:
            # Insert fl_attachment after upload/
            url = url.replace("upload/", "upload/fl_attachment/")
    
    return url
