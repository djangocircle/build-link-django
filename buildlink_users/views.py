from rest_framework import status
from base.middlewares.renderers import get_clean_errors, get_status
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from buildlink_users import serializers


class AdminObtainAuthToken(ObtainAuthToken):
    """
    To obatin authtoken only when admin logins
    """

    serializer_class = serializers.AdminAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": get_status(status.HTTP_400_BAD_REQUEST),
                    "errors": get_clean_errors(serializer.errors),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "code": status.HTTP_200_OK,
                "status": get_status(status.HTTP_200_OK),
                "data": {"token": token.key},
            },
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for all actions and REST methods related to user.
    """

    model = User
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @action(detail=False, methods=["patch"])
    def status(self, request):
        """
        activate or deactivate list of users
        """
        user_ids = request.data.get("user_ids")
        is_active = request.data.get("is_active")
        User.objects.filter(id__in=user_ids, is_superuser=False).update(
            is_active=is_active
        )
        return Response()

    @action(detail=False, methods=["delete"])
    def delete(self, request):
        """
        delete list of users
        """
        user_ids = request.data.get("user_ids")
        User.objects.filter(id__in=user_ids, is_superuser=False).delete()
        return Response()
