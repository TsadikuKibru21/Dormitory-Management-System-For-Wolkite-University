# Generated by Django 5.0.1 on 2024-01-10 10:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('StudentDean', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='block',
            name='Block_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.blocktype'),
        ),
        migrations.AddField(
            model_name='dorm',
            name='Block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block'),
        ),
        migrations.AddField(
            model_name='placement',
            name='Block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block'),
        ),
        migrations.AddField(
            model_name='placement',
            name='Room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.dorm'),
        ),
        migrations.AddField(
            model_name='placement',
            name='Stud_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user'),
        ),
    ]