from django.contrib import admin
from .models import Image, Annotation


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at', 'updated_at']
    ordering = ['-uploaded_at']


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'label', 'created_at']
    list_filter = ['user', 'label', 'created_at']
    search_fields = ['image__filename']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
