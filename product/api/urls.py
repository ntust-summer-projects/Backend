from django.urls import path, include
from rest_framework import routers
from . import views
app_name = 'api'
from general.api.views import UserViewSet
router = routers.DefaultRouter()
router.register('products', views.ReadOnlyProductViewSet)
router.register('materials', views.MaterialViewSet)
router.register('user/logs/(?P<type>[^/.]+)', views.LogViewSet)
router.register('user/product', views.ProductViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls))
]