from django.contrib import admin
from .models import Task,TaskAttachment, TaskComment, Collaboration, TaskSettings, UserSettings
# Register your models here.
admin.site.register(Task)
admin.site.register(TaskAttachment)
admin.site.register(TaskComment)
admin.site.register(Collaboration)
admin.site.register(TaskSettings)
admin.site.register(UserSettings)