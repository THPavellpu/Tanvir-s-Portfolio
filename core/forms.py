from django import forms

from .models import BlogComment, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Phone (optional)"}
            ),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Your Message", "rows": 5}
            ),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ["author_name", "author_email", "content"]
        widgets = {
            "author_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Name"}
            ),
            "author_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your Email"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Your Comment", "rows": 4}
            ),
        }

