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
# category_viewset_doc_list = method_decorator(name='list', decorator=swagger_auto_schema(
#     manual_parameters=[
#         category_choice
#     ],
#     operation_summary="Get categories"
# ))
# category_viewset_doc_create = method_decorator(name='create', decorator=swagger_auto_schema(
#     manual_parameters=[
#         category_choice
#     ],
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'name': openapi.Schema(
#                 type=openapi.TYPE_STRING,
#                 description='User Name'
#             ),
#             'parent': openapi.Schema(
#                 type=openapi.TYPE_INTEGER,
#                 description='Category parent',
#                 example=None
#             )
#         },
#         required=['name'],
#     ),
#     operation_summary="Create category"
# ))

log_viewset_doc_list = method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[
        log_choice
    ],
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
            )
        }
    ),
    operation_summary="Add new user"
))
