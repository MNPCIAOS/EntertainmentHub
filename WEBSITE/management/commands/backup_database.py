import os
import shutil
import subprocess
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

class Command(BaseCommand):
    help = "Create a timestamped backup of the configured database."

    def handle(self, *args, **options):
        backup_dir = Path(settings.BASE_DIR) / "backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        db = settings.DATABASES["default"]
        engine = db.get("ENGINE", "")
        if "sqlite" in engine:
            source = Path(db["NAME"])
            if not source.exists():
                raise CommandError(f"SQLite database not found: {source}")
            target = backup_dir / f"entertainmenthub_{stamp}.sqlite3"
            shutil.copy2(source, target)
        elif "postgresql" in engine:
            target = backup_dir / f"entertainmenthub_{stamp}.sql"
            cmd = ["pg_dump", "--dbname", db["NAME"], "--file", str(target)]
            if db.get("HOST"): cmd += ["--host", db["HOST"]]
            if db.get("PORT"): cmd += ["--port", str(db["PORT"])]
            if db.get("USER"): cmd += ["--username", db["USER"]]
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
            except (OSError, subprocess.CalledProcessError) as exc:
                raise CommandError(f"pg_dump failed: {exc}")
        else:
            raise CommandError("Unsupported database engine.")
        self.stdout.write(self.style.SUCCESS(f"Backup created: {target}"))
