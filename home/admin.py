from django.contrib import admin
from . models import PostImages, Post


admin.site.register(Post)
admin.site.register(PostImages)