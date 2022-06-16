from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import UserViewSet, UserEmailValidate, UserPhoneValidate


router = DefaultRouter()
#router.register(r'user/(?P<user_id>[0-9]+)/email_validate', UserEmailValidate)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/email_validate', UserEmailValidate.as_view()),
    path('user/<int:user_id>/phone_validate', UserPhoneValidate.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
