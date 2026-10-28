from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_host() == f"www.{settings.CANONICAL_HOST}":
            return HttpResponsePermanentRedirect(f"https://{settings.CANONICAL_HOST}{request.get_full_path()}")
        return self.get_response(request)
