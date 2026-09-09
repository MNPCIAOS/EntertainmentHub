from django.db import migrations, models
from django.core.validators import FileExtensionValidator
import WEBSITE.models


class Migration(migrations.Migration):
    dependencies = [("WEBSITE", "0002_community")]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="poster_image",
            field=models.ImageField(blank=True, upload_to="movies/posters/", validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name="movie",
            name="backdrop_image",
            field=models.ImageField(blank=True, upload_to="movies/backdrops/", validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name="episode",
            name="thumbnail_image",
            field=models.ImageField(blank=True, upload_to="episodes/thumbnails/", validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), WEBSITE.models.validate_image_size]),
        ),
    ]
