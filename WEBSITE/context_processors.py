from django.conf import settings
from .models import Abasobanuzi, Country, Genre


def navigation(request):
    is_content_admin = (
        request.user.is_authenticated
        and request.user.username == settings.CONTENT_ADMIN_USERNAME
        and request.user.is_staff
    )
    return {
        "nav_genres": Genre.objects.all(),
        "nav_narrators": Abasobanuzi.objects.all(),
        "nav_countries": Country.objects.all(),
        "is_content_admin": is_content_admin,
    }
