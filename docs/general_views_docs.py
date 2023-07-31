from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from general.api.serializers import *
from django.utils.decorators import method_decorator
register_viewset_doc = method_decorator(name='create', decorator=swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        
    )
))

user_viewset_list_doc = method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Get current user's information"
))