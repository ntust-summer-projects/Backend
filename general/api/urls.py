from django.urls import path, include
from rest_framework import routers
from . import views
app_name = 'api'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('announcements', views.AnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls))
]