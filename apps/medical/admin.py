from django.contrib import admin
from .models import MedicalImage, Annotation

@admin.register(MedicalImage)
class MedicalImageAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at', 'updated_at']
    ordering = ['-uploaded_at']

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['image', 'user', 'label', 'created_at']
    list_filter = ['label', 'user', 'created_at']
    search_fields = ['image__filename', 'label']
    readonly_fields = ['created_at', 'updated_at', 'polygon_points']
    ordering = ['-created_at']
