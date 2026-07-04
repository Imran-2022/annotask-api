from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Image, Annotation
from .serializers import ImageSerializer, AnnotationSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_images = []
        for file in files:
            image = Image.objects.create(
                user=request.user,
                file=file,
                filename=file.name
            )
            serializer = self.get_serializer(image)
            uploaded_images.append(serializer.data)
        
        return Response(uploaded_images, status=status.HTTP_201_CREATED)


class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get_queryset(self):
        queryset = Annotation.objects.filter(user=self.request.user)
        image_id = self.request.query_params.get('image')
        if image_id:
            queryset = queryset.filter(image_id=image_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
