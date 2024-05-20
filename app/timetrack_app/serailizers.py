from django.db import models
from .models import TimeEntry
from rest_framework import serializers
from django.utils.dateparse import parse_duration

class TimeEntrySerializers(serializers.ModelSerializer):
  duration = serializers.DurationField(required=False)

  def to_internal_value(self, data):
        duration_str = data.get('duration')
        if duration_str:
            data['duration'] = parse_duration(duration_str)
        return super().to_internal_value(data)
      
  class Meta:
    model = TimeEntry
    fields=['user', 'task', 'start_time', 'end_time', 'duration', 'notes']
    read_only_field=['user']
    
    

   