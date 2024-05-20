from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, TaskAttachmentViewSet, TaskCommentViewSet, CollaborationViewSet, UserSettingsViewSet,TaskSettingsViewSet


app_name = "task_app"

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task_app_tasks")
router.register(r"tasksattachment", TaskAttachmentViewSet, basename="task_app_attachment")
router.register(r"taskscomment", TaskCommentViewSet, basename="task_app_comment")
router.register(r'collaborations', CollaborationViewSet, basename="task_collaborations")
router.register(r'user-settings', UserSettingsViewSet,basename="user_settings")
router.register(r'task-settings', TaskSettingsViewSet,basename="task_settings")

urlpatterns = [
    path("", include(router.urls)),
]
