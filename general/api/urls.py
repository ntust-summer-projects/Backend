from django.urls import path, include
from rest_framework_nested import routers
from . import views
app_name = 'api'

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('announcements', views.AnnouncementViewSet)

# user_log_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
# user_log_router.register(r'logs', views.UserLogViewSet, basename='user-logs')

router.register('register',views.RegisterViewSet, basename='user-register')
router.register('login',views.LoginViewSet, basename='user-login')
router.register('reset-password',views.PasswordForgot, basename='reset-password')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include(user_log_router.urls)),
    path(r'logout', views.LogoutViewset.as_view(), name='user-logout')
]