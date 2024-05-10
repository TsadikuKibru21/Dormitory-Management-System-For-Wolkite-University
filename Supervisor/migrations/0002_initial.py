# Generated by Django 4.1.4 on 2024-05-10 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Supervisor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StudentDean', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='procotor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proctorassignment',
            name='Block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block'),
        ),
        migrations.AddField(
            model_name='proctorassignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
