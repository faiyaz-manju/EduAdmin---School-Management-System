from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [
    '/account/login/',
    '/account/register/',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)