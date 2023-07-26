from rest_framework import viewsets
from .serializers import UserSerializer, AnnouncementSerializer
from ..models import User, Announcement
from product.models import *
from product.api.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class UserLogViewSet(viewsets.ModelViewSet):
    queryset = AbstractLog.objects.all()
    serializer_class = LogSerializer
    
    def get_queryset(self):
        return AbstractLog.objects.filter(user_id=self.kwargs['user_id'])

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
