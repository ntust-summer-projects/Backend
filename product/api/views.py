from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from docs.product_views_docs import *
from .serializers import *
from ..models import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

@log_viewset_doc_list
@log_viewset_doc_create
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
        
        log_type = self.kwargs.get('type', None)
        if log_type:
            log_type = log_type.upper()
        data = AbstractLog.objects.filter(logType=log_type)
        if len(data):
            return data
        # else:
        
        #     raise ValidationError("Invalid type")
        return super().get_queryset()

class LogTypeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return AbstractLog.objects.filter(logtype=self.kwargs['log_type_pk'])

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = CategoryManager.all(type="ITEM")
#     serializer_class = CategorySerializer

# TODO: category material log
