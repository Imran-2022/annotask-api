from rest_framework import serializers
from .models import MedicalImage, Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'image', 'label', 'polygon_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_polygon_points(self, value):
        """Validate polygon points is a list of objects with x, y coordinates"""
        if not isinstance(value, list):
            raise serializers.ValidationError("polygon_points must be a list")
        if len(value) < 3:
            raise serializers.ValidationError("Polygon must have at least 3 points")
        for point in value:
            if not isinstance(point, dict) or 'x' not in point or 'y' not in point:
                raise serializers.ValidationError("Each point must have 'x' and 'y' coordinates")
            if not isinstance(point['x'], (int, float)) or not isinstance(point['y'], (int, float)):
                raise serializers.ValidationError("Coordinates must be numbers")
        return value

class MedicalImageSerializer(serializers.ModelSerializer):
    annotations = AnnotationSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicalImage
        fields = ['id', 'file', 'file_url', 'filename', 'uploaded_at', 'updated_at', 'annotations']
        read_only_fields = ['id', 'uploaded_at', 'updated_at', 'file_url']
    
    def get_file_url(self, obj):
        """Return the full media URL for the file"""
        if obj.file and hasattr(obj.file, 'url'):
            request = self.context.get('request') if hasattr(self, 'context') else None
            try:
                if request is not None:
                    return request.build_absolute_uri(obj.file.url)
            except Exception:
                # If something goes wrong building absolute URI, fall back to relative URL
                pass
            # Return relative media URL as a fallback
            return obj.file.url
        return None
    
    def create(self, validated_data):
        if not validated_data.get('filename') and validated_data.get('file'):
            validated_data['filename'] = validated_data['file'].name
        return super().create(validated_data)
