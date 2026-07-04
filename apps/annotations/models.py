from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annotation_images')
    file = models.FileField(upload_to='annotations/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename


class Annotation(models.Model):
    LABEL_CHOICES = [
        ('tumor', 'Tumor'),
        ('organ', 'Organ'),
        ('vessel', 'Vessel'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annotations')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='annotations')
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, default='tumor')
    polygon_points = models.JSONField(help_text='Stores annotation coordinates and metadata')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.label} annotation on {self.image.filename}"
