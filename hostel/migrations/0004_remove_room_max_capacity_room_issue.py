# Generated by Django 5.1.4 on 2025-05-28 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0003_room_max_capacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='max_capacity',
        ),
        migrations.AddField(
            model_name='room',
            name='issue',
            field=models.TextField(blank=True, null=True),
        ),
    ]
