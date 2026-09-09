from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import django.utils.text
import WEBSITE.models


SEED_ABASOBANUZI = [
    "Yanga", "B-The Great", "Rocky Kimomo", "Junior Giti", "Sankara", "Savimbi", "PK", "Gaheza", "Simba"
]


def seed_abasobanuzi(apps, schema_editor):
    Abasobanuzi = apps.get_model("WEBSITE", "Abasobanuzi")
    for name in SEED_ABASOBANUZI:
        Abasobanuzi.objects.get_or_create(
            name=name,
            defaults={"slug": django.utils.text.slugify(name)},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("WEBSITE", "0004_sitesettings"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Abasobanuzi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True)),
            ],
            options={"ordering": ["name"], "verbose_name": "Umusobanuzi", "verbose_name_plural": "Abasobanuzi"},
        ),
        migrations.AddField(
            model_name="movie",
            name="abasobanuzi",
            field=models.ManyToManyField(blank=True, related_name="movies", to="WEBSITE.abasobanuzi"),
        ),
        migrations.CreateModel(
            name="Short",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("video_file", models.FileField(upload_to="shorts/videos/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("thumbnail_image", models.ImageField(blank=True, upload_to="shorts/thumbnails/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_image_size])),
                ("status", models.CharField(choices=[("pending", "Pending review"), ("published", "Published"), ("rejected", "Rejected")], default="pending", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("movie", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="promo_shorts", to="WEBSITE.movie")),
                ("uploaded_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="uploaded_shorts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="short",
            index=models.Index(fields=["status", "-created_at"], name="WEBSITE_shor_status_7e5b13_idx"),
        ),
        migrations.RunPython(seed_abasobanuzi, migrations.RunPython.noop),
    ]
