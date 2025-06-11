from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default superuser (admin) if not exists'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@test.com'
        password = 'admin123'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {username} / {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists'))
