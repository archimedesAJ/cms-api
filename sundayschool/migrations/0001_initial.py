# Generated by Django 5.0.6 on 2024-08-04 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SundaySchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6)),
                ('birthday', models.DateField()),
                ('guardian_contact', models.CharField(max_length=11)),
                ('image', models.ImageField(blank=True, upload_to='photos/sunday_school_photo/')),
                ('location', models.CharField(max_length=100)),
            ],
        ),
    ]
