from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from general.api.serializers import *
from django.utils.decorators import method_decorator
register_viewset_doc = method_decorator(name='create', decorator=swagger_auto_schema(
    request_body=openapi.Schema(
    title='User',
    type=openapi.TYPE_OBJECT,
    required=['name', 'password'],
    properties={
        'role': openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=['COMPANY', 'NORMAL']
        ),
        'username': openapi.Schema(
            type=openapi.TYPE_STRING
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING
        ),
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
        ),
        'profile': openapi.Schema(
            description="Only required if the role is COMPANY",
            type=openapi.TYPE_OBJECT,
            properties={
                'companyName': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'address': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'vatNumber': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'chairman': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'contactPerson': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
                'contact1': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
            }
        )
    }
)
))

user_viewset_list_doc = method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Get current user's information"
))