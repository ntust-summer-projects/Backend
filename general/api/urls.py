from django.urls import path, include
from rest_framework_nested import routers
from . import views
app_name = 'api'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('announcements', views.AnnouncementViewSet)

user_log_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
user_log_router.register(r'logs', views.UserLogViewSet, basename='user-logs')

router.register('registration',views.RegisrationViewSet)
router.register('login',views.LoginViewSet)
router.register('logout',views.LogoutViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_log_router.urls))
]