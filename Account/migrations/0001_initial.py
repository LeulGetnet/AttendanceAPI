# Generated by Django 3.2.3 on 2021-06-06 14:21

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Locations', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('profile_pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('adress', models.CharField(max_length=500)),
                ('is_approved', models.BooleanField(default=False)),
                ('location', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Locations.locations')),
            ],
        ),
    ]
