from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tasks.models import Task
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates demo data for testing'

    def handle(self, *args, **options):
        # Create demo user if doesn't exist
        user, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={
                'username': 'demo',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: demo@example.com / demo123'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))
        
        # Create demo tasks
        demo_tasks = [
            {
                'title': 'Design login page',
                'description': 'Create mockups for login and register pages',
                'priority': 'high',
                'status': 'done',
                'due_date': date.today() - timedelta(days=2),
                'tags': 'design,ui',
            },
            {
                'title': 'Setup Django backend',
                'description': 'Configure Django project with REST API',
                'priority': 'high',
                'status': 'done',
                'due_date': date.today() - timedelta(days=1),
                'tags': 'backend,setup',
            },
            {
                'title': 'Implement Kanban board',
                'description': 'Build drag-and-drop task board with columns',
                'priority': 'high',
                'status': 'in_progress',
                'due_date': date.today(),
                'tags': 'frontend,feature',
            },
            {
                'title': 'Add date filtering',
                'description': 'Implement date picker for task filtering',
                'priority': 'medium',
                'status': 'in_progress',
                'due_date': date.today(),
                'tags': 'frontend,feature',
            },
            {
                'title': 'Write unit tests',
                'description': 'Add comprehensive test coverage',
                'priority': 'medium',
                'status': 'todo',
                'due_date': date.today() + timedelta(days=1),
                'tags': 'testing',
            },
            {
                'title': 'Deploy to production',
                'description': 'Setup production servers and CI/CD',
                'priority': 'medium',
                'status': 'todo',
                'due_date': date.today() + timedelta(days=7),
                'tags': 'deployment',
            },
            {
                'title': 'Image annotation feature',
                'description': 'Implement image annotation tools',
                'priority': 'low',
                'status': 'todo',
                'due_date': date.today() + timedelta(days=14),
                'tags': 'future,feature',
            },
        ]
        
        for task_data in demo_tasks:
            task, created = Task.objects.get_or_create(
                user=user,
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created task: {task.title}"))
        
        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
