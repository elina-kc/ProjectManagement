from django.shortcuts import render
from rest_framework import viewsets, status
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskComment, TaskAttachment, Collaboration, UserSettings, TaskSettings
from .serializers import TaskSerializer, TaskCommentSerializer, TaskAttachementSerializer,CollaborationSerializer, UserSettingsSerializer, TaskSettingsSerializer
import logging
from app.auth_mgmt.utlis import get_user_details
# from .filters import TaskPriorityFilter, TaskStatusFilter
# from common.utils.common_utils import get_authenticated_headers

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    logger = logging.getLogger(__name__)

    def create(self, request, *args, **kwargs):
        
        get_user_details(self.request)

        # Create the task with token-based authentication
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the serialized data
        # self.perform_create(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskCommentViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

    def create(self, request, *args, **kwargs):
        get_user_details(self.request)
        serializer = TaskCommentSerializer(data=request.data)
        
        # Create the task with token-based authentication
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the serialized data
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        task_comment = self.get_object()
        serializer = TaskCommentSerializer(task_comment)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        task_comment = self.get_object()
        serializer = TaskCommentSerializer(task_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        task_comment = self.get_object()
        serializer = TaskCommentSerializer(task_comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        task_comment = self.get_object()
        task_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachementSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = TaskAttachementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        task_attachment = self.get_object()
        serializer = TaskAttachementSerializer(task_attachment)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        task_attachment = self.get_object()
        serializer =TaskAttachementSerializer(task_attachment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        task_attachment = self.get_object()
        serializer = TaskAttachementSerializer(task_attachment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        task_attachment = self.get_object()
        task_attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assuming you have authentication implemented
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer

class TaskSettingsViewSet(viewsets.ModelViewSet):
    queryset = TaskSettings.objects.all()
    serializer_class = TaskSettingsSerializer




