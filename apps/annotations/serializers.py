from rest_framework import serializers
from .models import Image, Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'image', 'label', 'polygon_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ImageSerializer(serializers.ModelSerializer):
    annotations = AnnotationSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'file', 'file_url', 'filename', 'uploaded_at', 'updated_at', 'annotations']
        read_only_fields = ['id', 'uploaded_at', 'updated_at', 'file_url', 'annotations']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None
