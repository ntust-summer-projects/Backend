from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# category_choice = openapi.Parameter(
#             'type',
#             openapi.IN_PATH,
#             description='The type of categories.',
#             type=openapi.TYPE_STRING,
#             enum=['MATERIAL', 'PRODUCT'],
#         )
log_choice = openapi.Parameter(
            'type',
            openapi.IN_PATH,
            description='The type of logs.',
            type=openapi.TYPE_STRING,
            enum=['TRANSPORTATION', 'ITEM'],
        )

log_viewset_doc_list = method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
    operation_summary="Get all logs of a certain type for a user"
))
log_viewset_doc_retrieve = method_decorator(name='retrieve', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
    operation_summary="Get a certain log of user"
))
log_viewset_doc_delete = method_decorator(name='destroy', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
    operation_summary="Remove a certain log of user"
))
log_viewset_doc_update = method_decorator(name='update', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
    request_body=openapi.Schema(
        title='log properties',
        type=openapi.TYPE_OBJECT,
        properties={
            'timestamp': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME
            ),
            'product': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The product id.<br/>Only required if the type is ITEM'
            ),
            'amount': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The amount of items.<br/>Only required if the type is ITEM'
            ),
            'transportation': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The transportation id.<br/>Only required if the type is TRANSPORTATION'
            ),
            'distance': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                description='The transportation id.<br/>Only required if the type is TRANSPORTATION'
            ),
        }
    ),
    operation_summary="Update a certain log"
))

log_viewset_doc_create = method_decorator(name='create', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
    request_body=openapi.Schema(
        title='log properties',
        type=openapi.TYPE_OBJECT,
        properties={
            'timestamp': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME
            ),
            'product': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The product id.<br/>Only required if the type is ITEM'
            ),
            'amount': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The amount of items.<br/>Only required if the type is ITEM'
            ),
            'transportation': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The transportation id.<br/>Only required if the type is TRANSPORTATION'
            ),
            'distance': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                description='The transportation id.<br/>Only required if the type is TRANSPORTATION'
            ),
        }
    ),
    operation_summary="Create new log of a certain type"
))


readonlyproduct_viewset_doc_list = method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Get all products list (search)',
    manual_parameters=[
        openapi.Parameter(
            name='search',
            in_=openapi.IN_QUERY,
            description='Query keyword',
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            name='offset',
            in_=openapi.IN_QUERY,
            description='Offset for search results<br/>Default: 0',
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            name='size',
            in_=openapi.IN_QUERY,
            description='The maximum number of search results<br/>Default: 10',
            type=openapi.TYPE_INTEGER
        )
    ]
))

readonlyproduct_viewset_doc_retrieve = method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Get certain product by ID'
))

companyproduct_viewset_doc_list = method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Get current company\'s product list'
))

from rest_framework import serializers
class ComponentInSerializer(serializers.Serializer):
    material_id = serializers.IntegerField()
    weight = serializers.FloatField()

product_request_body = openapi.Schema(
    title='Product',
    type=openapi.TYPE_OBJECT,
    required=['name', 'number'],
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            example='Motor'
        ),
        'number': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Product\'s serial number',
            example='00183758'
        ),
        'tag': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='Array of tag id',
            items=openapi.Items(type=openapi.TYPE_INTEGER),
            example=[1, 2]
        ),
        'components': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='Array of the materials and weights of this product',
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'material_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'weights': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                },
            ),
            examples={'material_id':3, 'weights':38.2}
        )
    }
)

companyproduct_viewset_doc_create = method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Add product to current company.',
    request_body=product_request_body
))
companyproduct_viewset_doc_retrieve = method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Get current company\'s certain product by ID'
))
companyproduct_viewset_doc_update = method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update current company\'s certain product',
    request_body=product_request_body
))