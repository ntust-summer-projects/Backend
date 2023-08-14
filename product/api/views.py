from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from docs.product_views_docs import *
from .serializers import *
from ..models import *

@readonlyproduct_viewset_doc_list
@readonlyproduct_viewset_doc_retrieve
class ReadOnlyProductViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        search = self.request.GET.get('search', None)
        try:
            offset = int(self.request.GET.get('offset', 0))
        except ValueError:
            raise ValidationError({"offset":'must be integer'})
        try:
            size = int(self.request.GET.get('size', 10))
        except ValueError:
            raise ValidationError({"size":'must be integer'})
        tags = self.request.query_params.getlist('tags', None)
        
        queryset = super().get_queryset()
        for tag in tags:
            queryset = queryset.filter(tag=tag)
                
        if search is not None:
            queryset = queryset.filter(name__contains=search)
        return queryset[offset: offset+size]
    
        
@companyproduct_viewset_doc_list
@companyproduct_viewset_doc_create
@companyproduct_viewset_doc_retrieve
@companyproduct_viewset_doc_update
class ProductViewSet(viewsets.ModelViewSet): # TODO: add index and amount
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(company=self.request.user.id)
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

@log_viewset_doc_list
@log_viewset_doc_retrieve
@log_viewset_doc_create
@log_viewset_doc_update
@log_viewset_doc_delete
class LogViewSet(viewsets.ModelViewSet): # TODO: check role is NORMAL
    queryset = AbstractLog.objects.all()
    serializer_class = LogSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['logType'] = self.kwargs['type'].upper()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        data['logType'] = self.kwargs['type'].upper()
        data['user'] = request.user.id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
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

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# TODO: category material log
