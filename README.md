# build-link-django
Django rest framework API for login and user CRUD Operations

# Covered Points
- User login with [TokenAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication).
- User CRUD endpoints with the use of [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) of Django Rest Framework.
- Override the `DEFAULT_PARSER_CLASSES` to format the API response.
- Use of environment file to load the secret data
- Created `seed` function to apply django migrations and create super user.