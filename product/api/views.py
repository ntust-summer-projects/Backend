from rest_framework import viewsets
from .serializers import *
from ..models import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    
class LogViewSet(viewsets.ModelViewSet):
    queryset = AbstractLog.objects.all()
    serializer_class = LogSerializer

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = CategoryManager.all(type="ITEM")
#     serializer_class = CategorySerializer

# TODO: category material log
