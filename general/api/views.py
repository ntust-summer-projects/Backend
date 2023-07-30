from rest_framework import viewsets,status,mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AnnouncementSerializer,RegistrationSerializer,LoginSerializer,LogoutSerializer
from ..models import User, Announcement
from product.models import *
from product.api.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
# TODO: profile
class UserLogViewSet(viewsets.ModelViewSet):
    queryset = AbstractLog.objects.all()
    serializer_class = LogSerializer
    
    def get_queryset(self):
        return AbstractLog.objects.filter(user_id=self.kwargs.get('user_id', None))

class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class RegisrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    
    @action(detail = False, methods=['post'])
    def login(self, request):
        username = request.data['username']
        password = request.data['password']
    
        user = User.objects.filter(username=username).first()
        
        if user is None:
            return Response('User not found!',status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response('Incorrect password!',status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        
        response = Response(status=status.HTTP_200_OK)
        
        response.set_cookie(key='jwt',value=str(token),httponly=True)
        
        response.data = {
            'refresh':str(refresh),
            'access':str(token),
            'phone':user.phone,
            'email':user.email
        }
        
        return response
    
class LogoutViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer
    
    @action(detail=False, methods=['post'])
    def logout(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response
    