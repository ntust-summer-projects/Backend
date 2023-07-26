from rest_framework import serializers
from product.models import *
from auditlog.models import LogEntry
from general.api.serializers import UserSerializer

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ProductLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        # fields = '__all__'
        exclude = ('additional_data', 'content_type')
        depth = 0
        
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        action_id = data.pop('action')
        action_dict = ['CREATE', 'UPDATE', 'DELETE', 'ACCESS']
        data['action'] = action_dict[action_id]
        return data
        

#TODO: product update log
class ProductSerializer(serializers.ModelSerializer):
    logs = ProductLogSerializer(many=True, source='getLog', required=False, read_only=True)
    
    materials = MaterialSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
        

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractLog
        fields = '__all__'
        depth = 0
    
    def to_representation(self, instance):
        if instance.logType == 'ITEM':
            data = super().to_representation(instance)
            temp = LogI.objects.filter(abstractlog_ptr_id=data['id'])[0]
            return LogISerializer(temp, context=self.context).data
        elif instance.logType == "TRANSPORTATION":
            data = super().to_representation(instance)
            temp = LogT.objects.filter(abstractlog_ptr_id=data['id'])[0]
            return LogTSerializer(temp, context=self.context).data
        else:
            return super().to_representation(instance)

class LogISerializer(serializers.ModelSerializer):
    class Meta:
        model = LogI
        fields = '__all__'
        depth = 0
    
class LogTSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogT
        fields = '__all__'
        depth = 0
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
