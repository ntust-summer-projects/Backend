from rest_framework import serializers
from general.models import User, Profile, Announcement
from rest_framework.exceptions import ValidationError
from rest_framework_recaptcha import ReCaptchaField



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user', )
    
    def update(self, instance, validated_data):
        if(validated_data['meta_key'] == 'vatNumber'):
            raise ValidationError("vatNumber should not be changed.")
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True, source='get_profile')
    class Meta:
        model = User
        fields = ('id', 'username', 'profile', 'last_login', 'role', 'date_joined', 'email')
        depth = 1
    
    def create(self, validated_data):
        profile_data = validated_data.pop('get_profile')
        user = User.objects.create(**validated_data) # TODO: check role
        for item in profile_data:
            item['user'] = user
            Profile.objects.create(**item)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('get_profile')
        original_profile = Profile.objects.filter(user=instance.id)
        if validated_data.pop('username', False) != instance.username:
            raise ValidationError("username should not be changed")
        for item in profile_data:
            key = item['meta_key']
            profile = original_profile.filter(meta_key=key)
            try:
                profile[0]
            except:
                raise ValidationError(f'Invalid profile key "{key}"')
            profile.update(meta_value=item['meta_value'])
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)
    
    def to_internal_value(self, data):
        profile_data = data.pop('profile')
        data['profile'] = [{'meta_key': key, 'meta_value':value} for key, value in profile_data.items()]
        validated_data = super().to_internal_value(data)
        password = data.pop('password', None)
        if password is not None:
            validated_data['password'] = password
        return validated_data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        profiles = data.pop('profile')
        temp = {}
        for profile in profiles:
            key = profile['meta_key']
            value = profile['meta_value']
            temp[key] = value
        data['profile'] = temp
        return data
        

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ['username','password','email','role', 'profile']
        required = ['username', 'password', 'email', 'role']
        
    extra_kwargs = {
        'password' : {'write_only': True}
    }
    
    def create(self, validated_data):
        
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        
        profile_data = validated_data.pop('profile', None)
        if profile_data is not None:
            for item in profile_data:
                item['user'] = user
                Profile.objects.create(**item)
        return user
    
    
    def to_internal_value(self, data):
        profile_data = data.pop('profile', None)
        if profile_data is not None:
            data['profile'] = [{'meta_key': key, 'meta_value':value} for key, value in profile_data.items()]
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profiles = data.pop('profile', None)
        if profiles is not None:
            temp = {}
            for profile in profiles:
                key = profile['meta_key']
                value = profile['meta_value']
                temp[key] = value
            data['profile'] = temp
        return data
    
class LoginSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaField()
    
    class Meta:
        model = User
        fields = ['username','password']
        
class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
class PasswordForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
