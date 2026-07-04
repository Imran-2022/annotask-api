from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MedicalImage(models.Model):
    """Medical image file for annotation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_images')
    file = models.FileField(upload_to='medical_images/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
        ]
    
    def __str__(self):
        return self.filename

class Annotation(models.Model):
    """Polygon annotation on medical image"""
    LABEL_CHOICES = [
        ('tumor', 'Tumor'),
        ('organ', 'Organ'),
        ('vessel', 'Vessel'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_annotations')
    image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE, related_name='annotations')
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, default='tumor')
    polygon_points = models.JSONField(
        help_text='Array of points: [{"x": 120, "y": 220}, {"x": 140, "y": 260}, ...]'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['image', 'user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.label} annotation on {self.image.filename}"
