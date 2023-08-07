from rest_framework import viewsets, status, mixins, views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AnnouncementSerializer,RegistrationSerializer,LoginSerializer
from ..models import User, Announcement
from product.models import *
from product.api.serializers import *
from docs.general_views_docs import *


@user_viewset_list_doc
class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        try:
            return User.objects.filter(id=self.request.user.id)
        except:
            raise ValidationError("You need login first")
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset[0], many=False)
        return Response(serializer.data)
    
# TODO: profile amount
class UserLogViewSet(viewsets.ModelViewSet):
    queryset = AbstractLog.objects.all()
    serializer_class = LogSerializer
    
    def get_queryset(self):
        return AbstractLog.objects.filter(user_id=self.kwargs.get('user_id', None))

class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

@register_viewset_doc
class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()
    
    def create(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = ()
    authentication_classes = ()
    
    def create(self, request):
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
            'email':user.email
        }
        return response

class LogoutViewset(views.APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def get(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response
    