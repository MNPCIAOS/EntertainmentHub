# Generated manually for the current FILMS schema.
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import WEBSITE.models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True)),
                ("description", models.TextField(blank=True)),
                ("poster_url", models.URLField(blank=True, help_text="Public poster image URL (optional).")),
                ("poster_image", models.ImageField(blank=True, upload_to="movies/posters/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_media_size])),
                ("backdrop_url", models.URLField(blank=True, help_text="Public backdrop image URL (optional).")),
                ("backdrop_image", models.ImageField(blank=True, upload_to="movies/backdrops/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_media_size])),
                ("video_url", models.URLField(blank=True, help_text="Cloud/direct video URL. Use the upload field below for local files.")),
                ("video_file", models.FileField(blank=True, upload_to="movies/videos/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("download_url", models.URLField(blank=True, help_text="Authorized download URL (optional).")),
                ("download_file", models.FileField(blank=True, upload_to="movies/downloads/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("trailer_url", models.URLField(blank=True)),
                ("trailer_file", models.FileField(blank=True, upload_to="movies/trailers/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("content_type", models.CharField(choices=[("movie", "Movie"), ("series", "Series")], default="movie", max_length=10)),
                ("release_year", models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1888), django.core.validators.MaxValueValidator(2100)])),
                ("duration_minutes", models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ("rating", models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ("featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("genres", models.ManyToManyField(blank=True, related_name="movies", to="WEBSITE.genre")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Episode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("season_number", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("episode_number", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("thumbnail_url", models.URLField(blank=True)),
                ("thumbnail_image", models.ImageField(blank=True, upload_to="episodes/thumbnails/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_media_size])),
                ("video_url", models.URLField(blank=True, help_text="Cloud/direct video URL. Use the upload field below for local files.")),
                ("video_file", models.FileField(blank=True, upload_to="episodes/videos/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("download_url", models.URLField(blank=True, help_text="Authorized download URL (optional).")),
                ("download_file", models.FileField(blank=True, upload_to="episodes/downloads/", validators=[django.core.validators.FileExtensionValidator(["mp4", "webm", "ogg"]), WEBSITE.models.validate_media_size])),
                ("duration_minutes", models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="episodes", to="WEBSITE.movie")),
            ],
            options={"ordering": ["season_number", "episode_number"]},
        ),
        migrations.AddIndex(
            model_name="movie",
            index=models.Index(fields=["is_published", "featured"], name="WEBSITE_movi_is_publ_8c1b10_idx"),
        ),
        migrations.AddConstraint(
            model_name="episode",
            constraint=models.UniqueConstraint(fields=("movie", "season_number", "episode_number"), name="unique_episode"),
        ),
    ]
