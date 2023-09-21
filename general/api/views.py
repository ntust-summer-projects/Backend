from rest_framework import viewsets, status, mixins, views
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import *
from ..models import User, Announcement, FindPasswordRecord
from product.models import *
from product.api.serializers import *
from docs.general_views_docs import *
from django.views.decorators.csrf import csrf_exempt

import smtplib
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import Template, Context
from pathlib import Path

@user_viewset_list_doc
class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.request.user.id
        if user_id is None:
            raise ValidationError("You need login first")
        else:
            return User.objects.filter(id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset[0], many=False)
        return Response(serializer.data)


@user_update_doc
@api_view(['PUT'])
def user_update(request):
    instance = request.user
    
    if instance.id is None:
        raise ValidationError("You need login first")
    
    serializer = UserSerializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if getattr(instance, '_prefetched_objects_cache', None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
        instance._prefetched_objects_cache = {}

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
        role = request.data.get("role", None)
        if role not in ['COMPANY', "NORMAL"]:
            raise ValidationError("Invalid Role")
        profiles = request.data.get('profile', None)
        if role == "COMPANY":
            if profiles is None:
                raise ValidationError("Profile is required")
            required_profiles = ['companyName', 'address', 'phone', 'vatNumber', 'chairman', 'contactPerson', 'contact1']
            for p in required_profiles:
                if profiles.get(p, None) is None:
                    raise ValidationError(f'profile "{p}" is required')
        
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = serializer.data.copy()
        data.pop('password')
        return Response(data, status=status.HTTP_201_CREATED)

class LoginViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = ()
    authentication_classes = ()
        
    @csrf_exempt 
    def create(self, request):
        try:
            data = json.loads(request.body)
            url = "https://www.google.com/recaptcha/api/siteverify"
            params = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': data["token"],
            }
            verify_rs = requests.get(url, params=params, verify=True).json()
            is_success = verify_rs.get("success", False)
            
            if not is_success:
                response_data = {'message': 'Request processed failed!'}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            error_response = {
                'error_message': 'Invalid JSON format in request body',
                'error_details': str(e)
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        
        response.data = {
            'refresh':str(refresh),
            'access':str(token)
        }
        return response

class LogoutViewset(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        response=Response()
        response.data = {
            'message': 'success'
        }
        
        return response

@passwordforgot_vieswet_create_doc
@passwordforgot_vieswet_reset_doc
class PasswordForgot(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = PasswordForgotSerializer
    permission_classes = ()
    authentication_classes = ()
    
    def create(self,request):

        username = request.data['username']
        email = request.data['email']
        try:
            user = User.objects.get(username=username)
        except:
            return Response('User not found!',status=status.HTTP_400_BAD_REQUEST)
        
        if not user.email == email:
            return Response('Incorrect email!',status=status.HTTP_400_BAD_REQUEST)

        tokenGenerator = PasswordResetTokenGenerator()
        token = tokenGenerator.make_token(user)
        
        FindPasswordRecord.objects.create(user=user,token=token)
        # FindPasswordRecord.save()

        url = f"http://{request.get_host()}/api/reset-password/{token}/"

        SendEmail(email,url)

        response = Response()
        response.data = {
            'message':'email send successfully' ,
    
        }
        return response

    @action(detail=False, methods=['post'], url_path="(?P<token>[^/.]+)")
    def reset_with_token(self, request, token=None):
        new_password = request.data['new_password']
        
        try:
            instance = FindPasswordRecord.objects.get(token=token)
        except:
            return Response({'message': 'Invalid token'})
        
        if instance.isExpiried:
            return Response({'message': 'token expiried'})
        
        user = instance.user
        user.set_password(new_password)
        user.save()

        instance.isExpiried = True
        instance.save()

        return Response({'message': 'Password reset successfully'})



def SendEmail(receiver,url):
    content = MIMEMultipart() 
    content["subject"] = "Reset your password"  
    content["from"] = settings.EMAIL_HOST_USER  
    content["to"] = receiver 
    
    template = Template(Path("test/templates/email.html").read_text())
    context = Context({'verifyUrl': url})
    body = template.render(context)
    content.attach(MIMEText(body, 'html'))  
    
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  
        try:
            smtp.ehlo()  
            smtp.starttls()  
            smtp.login(settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD) 
            smtp.send_message(content)  
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
