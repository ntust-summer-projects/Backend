from rest_framework import viewsets
from .serializers import UserSerializer, AnnouncementSerializer
from ..models import User, Announcement

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
