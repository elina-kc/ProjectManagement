# Generated by Django 5.0.4 on 2024-05-03 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_mgmt', '0002_remove_customuser_groups'),
        ('task_app', '0006_task_assigned_to_task_created_by_taskcomment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth_mgmt.customuser', verbose_name='name'),
            preserve_default=False,
        ),
    ]
