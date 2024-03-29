from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"", views.UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("login", views.AdminObtainAuthToken.as_view()),
]
