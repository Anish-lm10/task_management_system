# Generated by Django 5.1.1 on 2024-10-11 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0008_remove_assign_task_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_task',
            name='clear_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]