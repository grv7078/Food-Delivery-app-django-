# Generated by Django 5.1.4 on 2025-01-09 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='longitude',
        ),
    ]
