from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Create or repair the single configured content administrator account."

    def add_arguments(self, parser):
        parser.add_argument("--username", default=settings.CONTENT_ADMIN_USERNAME)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"].strip()
        if not username:
            raise CommandError("CONTENT_ADMIN_USERNAME cannot be empty.")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True, "is_active": True},
        )

        if not user.is_active:
            user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        password = self.get_password(username)
        user.set_password(password)
        if user.last_login is None:
            user.last_login = timezone.now()
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(
            f"Content administrator '{username}' {action}. You can now log in at /account/login/ and you will be sent to /dashboard/."
        ))

    def get_password(self, username):
        import os
        from django.contrib.auth.password_validation import validate_password

        password = os.environ.get("CONTENT_ADMIN_PASSWORD", "").strip()

        if not password:
            raise CommandError(
                "CONTENT_ADMIN_PASSWORD is not set."
            )

        User = get_user_model()
        temp = User(username=username)

        try:
            validate_password(password, user=temp)
        except Exception as exc:
            for error in exc.error_list:
                raise CommandError(f"Password error: {error.message}")

        return password
