import datetime

import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication, get_authorization_header

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode("utf-8")
            id = decode_access_token(token)

            try:
                user = User.objects.get(id=id)

            except Exception:
                raise exceptions.AuthenticationFailed(
                    {
                        "message": "unauthenticated user",
                        "status": status.HTTP_403_FORBIDDEN,
                    }
                )
            return (user, None)

        raise exceptions.AuthenticationFailed(
            {"message": "unauthenticated user", "status": status.HTTP_403_FORBIDDEN}
        )


def create_access_token(id):
    user = User.objects.get(id=id)
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=90),
            "iat": datetime.datetime.utcnow(),
        },
        "access_secret",
        algorithm="HS256",
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, "access_secret", algorithms="HS256")
        return payload["user_id"]
    except Exception:
        raise exceptions.AuthenticationFailed(
            {"message": "unauthenticated user", "status": status.HTTP_403_FORBIDDEN}
        )


def create_refresh_token(id):
    user = User.objects.get(id=id)
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=90),
            "iat": datetime.datetime.utcnow(),
        },
        "refresh_secret",
        algorithm="HS256",
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms="HS256")
        return payload["user_id"]
    except Exception:
        raise exceptions.AuthenticationFailed(
            {"message": "unauthenticated user", "status": status.HTTP_403_FORBIDDEN}
        )
