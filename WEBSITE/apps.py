from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WEBSITE"

    def ready(self):
        from . import signals  # noqa: F401
