# Generated by Django 5.2.2 on 2025-06-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
