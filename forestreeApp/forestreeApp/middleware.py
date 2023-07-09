from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).

        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            UntypedToken(token)
        except (KeyError, InvalidToken, TokenError) as e:
            scope['user'] = AnonymousUser()
        else:
            decoded_data = jwt_decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            scope['user'] = await get_user(decoded_data['user_id'])

        return await self.app(scope, receive, send)
