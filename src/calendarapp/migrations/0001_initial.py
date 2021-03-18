# Generated by Django 3.1.5 on 2021-03-14 19:33
from django.conf import settings

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventColors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=24, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('color', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendarapp.eventcolors')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.eventstatus')),
                ('typeOf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.eventtypes')),
            ],
        ),
    ]