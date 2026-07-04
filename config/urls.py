from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        'message': 'Task Management & Image Annotation API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'auth': '/api/auth/',
            'tasks': '/api/tasks/',
        },
        'frontend': {
            'annotate': '/annotate',
            'tasks': '/tasks',
        }
    })

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    path('api/', include('apps.annotations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
