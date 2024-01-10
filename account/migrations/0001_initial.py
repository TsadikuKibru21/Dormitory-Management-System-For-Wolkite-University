# Generated by Django 5.0.1 on 2024-01-10 10:44

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchieveAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='BlockType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Block_Type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('R_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=500)),
                ('Abrevation_name', models.CharField(max_length=100)),
                ('background_image', models.ImageField(upload_to='images/')),
                ('logo', models.ImageField(upload_to='images/')),
                ('slogan', models.CharField(max_length=600)),
                ('descrption1', models.TextField(max_length=1000)),
                ('slogan1', models.CharField(max_length=600)),
                ('descrption2', models.TextField(max_length=1000)),
                ('slogan2', models.CharField(max_length=600)),
                ('descrption3', models.TextField(max_length=1000)),
                ('streat', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('location', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=200, null=True, unique=True)),
                ('password', models.CharField(max_length=500)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('Role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.role')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField()),
                ('status_code', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='csender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FingerPrint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finger_print', models.BinaryField(blank=True, null=True)),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Id_no', models.CharField(max_length=200)),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('Gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=6)),
                ('phone_no', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('is_Employee', models.BooleanField(default=False)),
                ('stream', models.CharField(blank=True, choices=[('social', 'social'), ('natural', 'natural')], default='nan', max_length=200, null=True)),
                ('collage', models.CharField(blank=True, default='nan', max_length=200, null=True)),
                ('Department', models.CharField(blank=True, default='nan', max_length=200, null=True)),
                ('Year_of_Student', models.CharField(blank=True, default='nan', max_length=50, null=True)),
                ('Region', models.CharField(blank=True, max_length=200, null=True)),
                ('Emergency_responder_name', models.CharField(blank=True, max_length=200, null=True)),
                ('Emergency_responder_address', models.CharField(blank=True, max_length=200, null=True)),
                ('Emergency_responder_phone_no', models.CharField(blank=True, max_length=13, null=True)),
                ('Disability', models.CharField(blank=True, choices=[('Disable', 'Disable'), ('Not_Disable', 'Not_Disable')], max_length=100, null=True)),
                ('Campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.blocktype')),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='User',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.user'),
        ),
    ]