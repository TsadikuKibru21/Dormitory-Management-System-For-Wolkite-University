# Generated by Django 5.0.1 on 2024-01-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exit_Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materials', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Exit_Permission_Requst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materials', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Property_id', models.CharField(max_length=100, unique=True)),
                ('Propery_name', models.CharField(max_length=100)),
                ('property_category', models.CharField(choices=[('Key', 'Key'), ('Locker', 'Locker'), ('Desk', 'Desk'), ('Chair', 'Chair'), ('Bed', 'Bed'), ('Mattress', 'Mattress'), ('Pillow', 'Pillow')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ReportProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('is_solve', models.CharField(default='Un-Approved', max_length=50)),
            ],
        ),
    ]
