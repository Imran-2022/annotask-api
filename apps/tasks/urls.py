from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from apps.annotations.views import AnnotationViewSet

router = DefaultRouter()
router.register(r'', views.TaskViewSet, basename='task')
router.register(r'annotations', AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('', include(router.urls)),
]
