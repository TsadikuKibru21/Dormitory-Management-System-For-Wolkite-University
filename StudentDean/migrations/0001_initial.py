# Generated by Django 4.1.4 on 2024-05-10 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100, null=True)),
                ('Content', models.TextField(blank=True, max_length=3000, null=True)),
                ('File', models.FileField(blank=True, null=True, upload_to='files/')),
                ('Active_Date', models.DateField()),
                ('End_Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Block_name', models.CharField(max_length=100)),
                ('Block_purpose', models.CharField(choices=[('Males Block', 'Males Block'), ('Females Block', 'Females Block')], max_length=100)),
                ('Block_Capacity', models.IntegerField()),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('InActive', 'InActive')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dorm_name', models.CharField(max_length=100)),
                ('Floor', models.CharField(choices=[('Floor-1', 'Floor-1'), ('Floor-2', 'Floor-2'), ('Floor-3', 'Floor-3'), ('Floor-4', 'Floor-4'), ('Floor-5', 'Floor-5'), ('Floor-6', 'Floor-6'), ('Floor-7', 'Floor-7')], max_length=100)),
                ('Capacity', models.CharField(max_length=10)),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('InActive', 'InActive')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.block')),
                ('Room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentDean.dorm')),
            ],
        ),
    ]
