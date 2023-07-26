from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['logType'] = self.kwargs['type'].upper()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def get_serializer_class(self):
    #     logtype = self.kwargs['type'].upper()
    #     if logtype == "ITEM":
    #         return LogISerializer
    #     elif logtype == "TRANSPORTATION":
    #         return LogTSerializer
    #     else:
    #         return super().get_serializer_class()
    
    def get_queryset(self):
        logtype = self.kwargs['type'].upper()
        data = AbstractLog.objects.filter(logType=logtype)
        if len(data):
            return data
        # else:
        
        #     raise ValidationError("Invalid type")
        return super().get_queryset()
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # def get_serializer_class(self):
    #     logtype = self.kwargs['type'].upper()
    #     if logtype == "ITEM":
    #         return LogISerializer
    #     elif logtype == "TRANSPORTATION":
    #         return LogTSerializer
    #     else:
    #         return super().get_serializer_class()
    
    # def get_queryset(self):
    #     logtype = self.kwargs['type'].upper()
    #     data = AbstractLog.objects.filter(logType=logtype)
    #     if len(data):
    #         return data
    #     # else:
    #     #     raise ValidationError("Invalid type")
    #     return super().get_queryset()

class LogTypeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return AbstractLog.objects.filter(logtype=self.kwargs['log_type_pk'])

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = CategoryManager.all(type="ITEM")
#     serializer_class = CategorySerializer

# TODO: category material log
