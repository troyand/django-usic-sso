django-usic-sso
===============

Authentication backend for Django that utilizes USIC Redis SSO cookie.

------------
Installation
------------

1. Run ``pip install ...``.

2. Set AUTHENTICATION_BACKENDS to::

   AUTHENTICATION_BACKENDS = ('django_usic_sso.backends.RedisCookieBackend',)

3. Configure Redis server::

    SSO_REDIS_HOST = '127.0.0.1'
    SSO_REDIS_PORT = 6379
    SSO_REDIS_DB = 0
    SSO_REDIS_PASSWORD = ''

4. Configure cookie name and prefix::

    SSO_COOKIE_NAME = 'PHPSESSID'
    SSO_COOKIE_PREFIX = 'usic.at'

5. Configure SSO login url::

    SSO_URL = 'https://my.usic.at/'

6. Add login view to Django urls.py::

    url(r'^accounts/login/$', 'django_usic_sso.views.login', name='login'),
