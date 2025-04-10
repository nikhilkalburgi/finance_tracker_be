from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creates a test user for the application'

    def handle(self, *args, **kwargs):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpassword123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
            return
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        
        UserProfile.objects.create(user=user)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created test user: {username}'))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')