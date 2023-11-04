from django.contrib import admin
from .models import Tag, Comment, Blog

# Register your models here.

@admin.register(Blog)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","title", "owner")


# admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Comment)