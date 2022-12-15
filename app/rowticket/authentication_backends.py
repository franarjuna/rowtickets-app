from django.contrib.auth.backends import ModelBackend
from users.models import User


class CaseInsensitiveEmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.pop('email', None)

        if not email and username:
            email = username

        if not (email and password):
            return None

        try:
            user = User.objects.get(email__iexact=email)

            if user.check_password(password):
                return user

            return None

        except User.DoesNotExist:
            return None
