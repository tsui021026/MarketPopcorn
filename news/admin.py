from django.contrib import admin
from django.db import models
from .models import Post, Subscriber, Newsletter
from tinymce.widgets import TinyMCE


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"


class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]


class PostAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget':TinyMCE()}
    }


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Subscriber)
admin.site.register(Newsletter, NewsletterAdmin)

