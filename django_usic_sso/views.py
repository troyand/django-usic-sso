import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect, resolve_url
from django.utils.http import is_safe_url
from urllib import urlencode


def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Performs SSO-cookie based authentication.
    User is redirected to SSO_URL if not authenticated.
    User is reidrected to next page if authenticated.

    Security checks are based on code from
    django.contrib.auth.views.login
    """
    sso_redirect_url = '%slogin?%s' % (settings.SSO_URL, urlencode({
        'from': request.build_absolute_uri()
        }))
    redirect_to = request.POST.get(redirect_field_name,
            request.GET.get(redirect_field_name, ''))
    if settings.SSO_COOKIE_NAME in request.COOKIES:
        logging.debug('Cookie %s with value %s was found in request, authenticating',
                      settings.SSO_COOKIE_NAME,
                      request.COOKIES[settings.SSO_COOKIE_NAME])
        user = authenticate(cookie=request.COOKIES[settings.SSO_COOKIE_NAME])
        if not user:
            logging.debug('Authenticate did not return user, redirecting to %s',
                          sso_redirect_url)
            return redirect(sso_redirect_url)
        else:
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            logging.debug('Authenticate returned user %s, redirecting to %s',
                          user, redirect_to)
            auth_login(request, user)
            return redirect(redirect_to)
    else:
        logging.debug('Cookie %s was not found in request, redirecting to %s',
                      settings.SSO_COOKIE_NAME, sso_redirect_url)
        return redirect(sso_redirect_url)

def logout(request):
    sso_redirect_url = '%slogout' % settings.SSO_URL
    auth_logout(request)
    return redirect(sso_redirect_url)
