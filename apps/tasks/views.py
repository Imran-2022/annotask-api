from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['order', '-created_at']
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Get tasks for a specific date"""
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'date parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = Task.objects.filter(user=request.user, due_date=date_obj).order_by('order', '-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """Get tasks for a date range"""
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response({'error': 'start_date and end_date parameters required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = Task.objects.filter(
            user=request.user,
            due_date__gte=start_date,
            due_date__lte=end_date
        ).order_by('due_date', 'order', '-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder tasks within a status"""
        tasks_data = request.data.get('tasks', [])
        
        for task_data in tasks_data:
            try:
                task = Task.objects.get(id=task_data['id'], user=request.user)
                task.status = task_data.get('status', task.status)
                task.order = task_data.get('order', task.order)
                task.save()
            except Task.DoesNotExist:
                return Response({'error': f'Task {task_data["id"]} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message': 'Tasks reordered successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change task status"""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = new_status
        task.save()
        return Response(TaskSerializer(task).data)

