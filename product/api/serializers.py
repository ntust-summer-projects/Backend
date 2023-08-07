from rest_framework import serializers
from product.models import *
from auditlog.models import LogEntry
from rest_framework.exceptions import ValidationError

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(many=False, read_only=True)
    material_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Component
        exclude = ('product', )
        
    def to_internal_value(self, data):
        if Material.objects.filter(id=data['material_id']) is None:
            raise ValidationError("Invalid Material ID")
        return super().to_internal_value(data)
        
        
        

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
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)
        
    

#TODO: product update log
class ProductSerializer(serializers.ModelSerializer):
    logs = ProductLogSerializer(many=True, source='get_log', required=False, read_only=True)
    
    # materials = MaterialSerializer(many=True)
    components = ComponentSerializer(many=True, source='get_component')
    class Meta:
        model = Product
        exclude = ('materials', )
        
    def create(self, validated_data):
        components = validated_data.pop('get_component')
        product = super().create(validated_data)
        materials_id = []
        for component in components:
            material_id = component['material_id']
            if material_id in materials_id:
                raise ValidationError("You can't have components with the same material id.")
            materials_id.append(material_id)
            component['product_id'] = product.id
            Component.objects.create(**component)
        return product
        
    def update(self, instance, validated_data):
        components = validated_data.pop('get_component', None)
        # m_ids = [c['material_id'] for c in components]
        
        if components is not None:
            oringinal_components = Component.objects.filter(product_id=instance.id)
            om_ids = [oc.material_id for oc in oringinal_components]
            for component in components:
                weight, material_id = component.get('weight', None), component.get('material_id', None)
                
                if weight is None or material_id is None:
                    raise ValidationError("You need provide both material_id and weight")
                try:
                    Material.objects.get(id=material_id)
                except:
                    raise ValidationError(f"Invalid material id={material_id}")
                if material_id in om_ids:
                    obj = Component.objects.get(product_id=instance.id, material_id=material_id)
                    obj.weight = weight
                    obj.save()
                    om_ids.remove(material_id)
                else:
                    component['product_id'] = instance.id
                    Component.objects.create(**component)
                    
            for om_id in om_ids:
                obj = Component.objects.filter(product_id=instance.id, material_id=om_id)
                obj.delete()
                
        return super().update(instance, validated_data)


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
        
    def to_internal_value(self, data):
        logType = data.get('logType', None)
        if logType == 'ITEM':
            logI = LogISerializer(data=data)
            logI.is_valid(raise_exception=True)
            return logI.data
        elif logType == "TRANSPORTATION":
            logT = LogTSerializer(data=data)
            logT.is_valid(raise_exception=True)
            return logT.data
        else:
            raise ValidationError("Invalid log type")
        
    def create(self, validated_data):
        logType = validated_data.get('logType', None)
        if logType == 'ITEM':
            logI = LogISerializer(data=validated_data)
            logI.is_valid()
            return logI.save()
        elif logType == "TRANSPORTATION":
            logT = LogTSerializer(data=validated_data)
            logT.is_valid()
            return logT.save()
        
    def update(self, instance, validated_data):
        logType = validated_data.get('logType', None)
        if logType == 'ITEM':
            instance.amount = validated_data.get('amount', instance.amount)
            product_id = validated_data.get('product', None)
            if product_id:
                instance.product = Product.objects.filter(id=product_id)[0]
        elif logType == "TRANSPORTATION":
            instance.distance = validated_data.get('distance', instance.distance)
            transportation_id = validated_data.get('transportation', None)
            if transportation_id:
                instance.product = Product.objects.filter(id=transportation_id)[0]
        if instance.user.id != validated_data['user']:
            raise ValidationError("You can't change user")
        instance.user = User.objects.filter(id=validated_data['user'])[0]
        instance.save()
        return instance

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
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        