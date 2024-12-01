# Generated by Django 5.1.3 on 2024-12-01 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentDean', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Device Name')),
                ('ip', models.GenericIPAddressField(verbose_name='Device IP')),
                ('port', models.PositiveIntegerField(verbose_name='Device Port')),
                ('status', models.CharField(choices=[('Connected', 'Connected'), ('Not-Connected', 'Not-Connected')], max_length=255)),
                ('block_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block')),
            ],
        ),
    ]
