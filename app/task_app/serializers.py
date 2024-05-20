from rest_framework import serializers
from .models import  Task , TaskComment, TaskAttachment, Collaboration, UserSettings, TaskSettings

class TaskAttachementSerializer(serializers.ModelSerializer):
  class Meta:
    model= TaskAttachment
    fields =['task','file','uploaded_at']
    read_only_fields =['uploaded_at']
    
    
class TaskCommentSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = TaskComment
    fields = [ 'task','author','comment','created_at']
    read_only_fields = [ 'created_at']
    
  def __str__(self):
        return f"{self.task.task_name} - Comment by {self.author.username}"

class TaskSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Task
    fields ='__all__'
   
  def __str__(self):
    return self.task_name
    

class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = '__all__'
        
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'

class TaskSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSettings
        fields = '__all__'
        
