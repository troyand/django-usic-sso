import phpserialize
import redis

from django.conf import settings
from django.contrib.auth.models import User


redis_server = redis.StrictRedis(
        host=settings.SSO_REDIS_HOST,
        port=settings.SSO_REDIS_PORT,
        db=settings.SSO_REDIS_DB,
        password=settings.SSO_REDIS_PASSWORD
        )


class RedisCookieBackend(object):
    def __init__(self):
        self.server = redis_server

    def authenticate(self, cookie):
        prefixed_cookie = settings.SSO_COOKIE_PREFIX + cookie
        if self.server.exists(prefixed_cookie):
            php_session = self.server.get(prefixed_cookie)
            data = phpserialize.loads(php_session)
            user_data = phpserialize.loads(data[0])
            for key, val in user_data.items():
                if isinstance(val, str):
                    user_data[key] = val.decode('utf8')
            try:
                if 'login' not in user_data:
                    return None
                user = User.objects.get(username=user_data['login'])
            except User.DoesNotExist:
                user = User(username=user_data['login'])
            user.first_name = user_data.get('name', '')
            user.last_name = user_data.get('surname', '')
            user.email = user_data.get('email')
            user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

