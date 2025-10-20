from django.shortcuts import redirect
from django.urls import reverse

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is authenticated and accessing '/'
        if request.path == '/' and request.user.is_authenticated:
            return redirect('/index/')
        response = self.get_response(request)
        return response
