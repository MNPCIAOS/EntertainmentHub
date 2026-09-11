
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = "Create or repair the single configured content administrator account."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default=settings.CONTENT_ADMIN_USERNAME,
        )

    def handle(self, *args, **options):
        User = get_user_model()

        username = options["username"].strip()

        if not username:
            raise CommandError(
                "CONTENT_ADMIN_USERNAME cannot be empty."
            )

        password = os.environ.get(
            "CONTENT_ADMIN_PASSWORD",
            ""
        ).strip()

        if not password:
            raise CommandError(
                "CONTENT_ADMIN_PASSWORD is not set in the environment."
            )

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        try:
            validate_password(password, user=user)
        except Exception as exc:
            for error in exc.error_list:
                raise CommandError(
                    f"Password error: {error.message}"
                )

        user.set_password(password)
        user.save()

        action = "created" if created else "updated"

        self.stdout.write(
            self.style.SUCCESS(
                f"Content administrator '{username}' {action} successfully. "
                "You can now log in at /account/login/ and you will be "
                "sent to /dashboard/."
            )
        )

