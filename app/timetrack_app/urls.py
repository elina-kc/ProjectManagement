from .views import TimeEntryViewsets
from rest_framework import routers
from django.urls import path, include

app_name ="timetrack_app"

router = routers.DefaultRouter()
router.register(r'time_entries', TimeEntryViewsets)

urlpatterns = [
    path('', include(router.urls)),
]