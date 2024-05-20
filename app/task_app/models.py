from django.db import models
from app.auth_mgmt.api.v1 import *
from app.auth_mgmt.models  import CustomUser
import pytz

# from django.contrib.auth.models import User 


# Create your models here.
  
class Task(models.Model):
  PRIORITY_CHOICES =[
    ('low','Low'),
    ('medium',"Medium"),
    ('high','High'),
  ]
  STATUS_CHOICES=[
    ('to do','To Do'),
    ('in progress','In Progress'),
    ('completed','Completed'),
    ('cancelled','Cancelled'),
  ]

  task_name= models.CharField(max_length=200)
  assigned_to =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True)
  start_date = models.DateField(null=True, blank=True)
  due_date = models.DateField(null=True, blank=True)
  priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default='medium')
  status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='to do')
  created_by =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks',blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
  dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
  TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
  timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
 
  
  
  
  def __str__(self):
    return self.task_name
  
  
class TaskComment(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_comments')
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
     return str(self.task.title_name)
  
class TaskAttachment(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
  file = models.FileField(upload_to='task_attachments/')
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
     return f"{self.task.task_name} - {self.file.name}"
  
  

   
    
ACTIVITY_CHOICES = [
        ('update', 'Task Updated'),
        ('comment', 'New Comment Added'),
        ('attachment', 'File Attached'),
        ('status_change', 'Status Changed'),
        # Add more activity choices as needed
    ] 

class Collaboration(models.Model):
  
  
    HIGH_PRIORITY = 'High Priority'
    BUG_FIX = 'Bug Fix'
    DESIGN_REVIEW = 'Design Review'
    # Add more predefined choices as needed

    LABEL_CHOICES = [
        (HIGH_PRIORITY, 'High Priority'),
        (BUG_FIX, 'Bug Fix'),
        (DESIGN_REVIEW, 'Design Review'),
        # Add more predefined choices as needed
    ]
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='collaboration')
    labels =models.CharField(max_length=50, choices=LABEL_CHOICES, unique=True)
    activity_log = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    
    
    def __str__(self):
        return f'Collaboration on {self.task.title} by {self.user.username}'
    
LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish')
  
  ]    
class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, choices=[('light', 'Light Mode'), ('dark', 'Dark Mode')])
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
    status = models.CharField(max_length=255, choices= LANGUAGE_CHOICES, default='en')
    
    
    def __str__(self):
      return self.theme

class TaskSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    default_view = models.CharField(max_length=50, choices=[('list', 'List View'), ('grid', 'Grid View'), ('kanban', 'Kanban Board')])
    default_sorting = models.CharField(max_length=50, choices=[('deadline', 'Deadline'), ('priority', 'Priority'), ('status', 'Status')])
    tasks_per_page = models.IntegerField(default=10)
    
    def __str__(self):
      return self.default_view