from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'tags', 'tags_list', 'created_at', 'updated_at', 'order']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_tags_list(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []

