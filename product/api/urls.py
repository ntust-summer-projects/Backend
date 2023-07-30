from django.urls import path, include
from rest_framework import routers
from . import views
app_name = 'api'

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('materials', views.MaterialViewSet)
router.register('logs/(?P<type>[^/.]+)', views.LogViewSet)

urlpatterns = [
    path('', include(router.urls))
]