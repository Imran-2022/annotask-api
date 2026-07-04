from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import MedicalImage, Annotation
from .serializers import MedicalImageSerializer, AnnotationSerializer

class MedicalImageViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [OrderingFilter]
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        return MedicalImage.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        files = request.FILES.getlist('file')
        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        for file_obj in files:
            serializer = self.get_serializer(data={
                'file': file_obj,
                'filename': file_obj.name,
            })
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            created_images.append(serializer.data)

        return Response(created_images, status=status.HTTP_201_CREATED)

class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['image']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Annotation.objects.filter(user=self.request.user)
        image_id = self.request.query_params.get('image') or self.request.query_params.get('image_id')
        if image_id:
            queryset = queryset.filter(image_id=image_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_image(self, request):
        """Get all annotations for a specific image"""
        image_id = request.query_params.get('image_id')
        if not image_id:
            return Response({'error': 'image_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image = MedicalImage.objects.get(id=image_id, user=request.user)
        except MedicalImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        
        annotations = Annotation.objects.filter(image=image, user=request.user)
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)
