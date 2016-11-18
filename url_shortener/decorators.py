from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings


def anonymous_required(function=None, redirect_url=None, redirect_field_name=None):
    if not redirect_url:
        redirect_url = getattr(settings, "LOGIN_REDIRECT_URL", "/")

    decorator = user_passes_test(
        lambda u: u.is_anonymous(), login_url=redirect_url, redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
