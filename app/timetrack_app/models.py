from django.db import models
from app.auth_mgmt.models import CustomUser
from app.task_app.models import Task
# Create your models here.
class TimeEntry(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  duration = models.DurationField(null=True, blank=True)
  notes = models.TextField(null=True, blank=True)
  
  
  def save(self, *args, **kwargs):
        self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)
        
        