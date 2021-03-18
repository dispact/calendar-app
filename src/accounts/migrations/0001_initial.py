# Generated by Django 3.1.5 on 2021-03-08 17:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=126, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=126, null=True, verbose_name='Last Name')),
                ('sick_days', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Sick Days')),
                ('personal_days', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Personal Days')),
                ('vacation_days', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Vacation Days')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
