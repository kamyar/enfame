from django.contrib import admin
from .models import Post, UrlEntry

admin.site.register(Post)
admin.site.register(UrlEntry)