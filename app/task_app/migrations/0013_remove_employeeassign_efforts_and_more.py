# Generated by Django 5.0.4 on 2024-05-08 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0012_efforts_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeassign',
            name='efforts',
        ),
        migrations.RemoveField(
            model_name='employeeassign',
            name='assignees',
        ),
        migrations.RemoveField(
            model_name='employeeassign',
            name='task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='title',
            new_name='task_name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='project',
        ),
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('to do', 'To Do'), ('in progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='to do', max_length=255),
        ),
        migrations.DeleteModel(
            name='Efforts',
        ),
        migrations.DeleteModel(
            name='EmployeeAssign',
        ),
    ]
