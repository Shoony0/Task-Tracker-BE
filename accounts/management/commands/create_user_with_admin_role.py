from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a user and assign the "admin" role'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='admin@gmail.com')
        parser.add_argument('--password', type=str, default='admin123')

    def handle(self, *args, **options):
        first_name = "Admin"
        last_name = "User"
        email = options['email']
        username = email
        password = options['password']

        # Ensure the 'admin' role exists
        admin_role, created = Role.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Role "admin" created'))

        user, created = User.objects.get_or_create(first_name=first_name, last_name=last_name, username=username, defaults={
            'email': email
        })

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User created: {username} / {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))

        user.roles.add(admin_role)
        self.stdout.write(self.style.SUCCESS(f'Assigned "admin" role to {username}'))
