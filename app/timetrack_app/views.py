from django.shortcuts import render
from rest_framework import viewsets
from .serailizers import TimeEntrySerializers
from .models import TimeEntry
# Create your views here.

class TimeEntryViewsets(viewsets.ModelViewSet):
  queryset = TimeEntry.objects.all()
  serializer_class = TimeEntrySerializers
  
  