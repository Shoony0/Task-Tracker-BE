from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default superuser (admin) if not exists'

    def handle(self, *args, **options):
        first_name = 'Super'
        last_name = 'User'
        username = 'admin'
        email = 'admin@admin.com'
        password = 'admin123'

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email} / {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{email}" already exists'))
