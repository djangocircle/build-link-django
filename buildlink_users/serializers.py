from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_active",
        ]


class AdminAuthTokenSerializer(AuthTokenSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages["required"] = (
                "%s field is required." % field.capitalize()
            )

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value.lower())
            if not user.is_superuser:
                raise serializers.ValidationError(
                    "Invalid username or password",
                    code="authorization",
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid username or password",
                code="authorization",
            )

        return value.lower()

    def validate(self, attrs):
        username = attrs.get("username")
        print("username")
        user = User.objects.get(username=username)
        if not user.is_active:
            raise serializers.ValidationError(
                "You are trying to access an inactive account.",
                code="authorization",
            )

        return super().validate(attrs)
