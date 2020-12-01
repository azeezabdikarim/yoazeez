from django.contrib import admin
from .models import BlogPost, Post, Post2, Comment, Photo


# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Post, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Post2, admin.ModelAdmin)
admin.site.register(Photo, admin.ModelAdmin)
