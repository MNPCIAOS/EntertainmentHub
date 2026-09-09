from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse


class SingleAdminGuardMiddleware:
    """Allow only the configured, staff-enabled content account into admin URLs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected = request.path == "/dashboard" or request.path.startswith("/dashboard/") or request.path == "/admin" or request.path.startswith("/admin/")
        if protected:
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), reverse("login"))
            if request.user.username != settings.CONTENT_ADMIN_USERNAME or not request.user.is_staff:
                return redirect("home")
        return self.get_response(request)
