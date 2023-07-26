from rest_framework import serializers
from product.models import Product, Material, AbstractLog

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        
#TODO: product update log
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('company', )
        # fields = '__all__'
        depth = 1

class LogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbstractLog
        fields = '__all__'
        depth = 0
        
# class CategorySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length = 50)
#     parent = serializers.IntegerField()
#     class Meta:
#         fields = '__all__'
