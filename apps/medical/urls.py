from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'images', views.MedicalImageViewSet, basename='medical-image')
router.register(r'annotations', views.AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('', include(router.urls)),
]
