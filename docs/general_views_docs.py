from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

user_viewset_doc = swagger_auto_schema(
    manual_parameters=[
        # Add your custom parameters here
    ],
    responses={
        # Add your custom responses here
    },
    operation_summary="Summary of the operation",
    operation_description="Detailed description of the operation",
)