from django.contrib.auth.views import redirect_to_login

from django.urls import reverse

class LoginObrigatorioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        liberadas = (
            reverse('auth-login'),
            '/admin/',
        )

        if not request.user.is_authenticated and not request.path.startswith(liberadas):
            return redirect_to_login(request.get_full_path())
        return self.get_response(request)