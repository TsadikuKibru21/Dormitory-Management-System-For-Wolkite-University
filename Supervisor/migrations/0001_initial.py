# Generated by Django 5.0.1 on 2024-01-10 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('StudentDean', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('num_shift_per_day', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProctorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block')),
            ],
        ),
    ]