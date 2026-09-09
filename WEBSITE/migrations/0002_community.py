from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("WEBSITE", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="WEBSITE.movie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="movie_likes", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes": [models.Index(fields=["movie", "created_at"], name="WEBSITE_moveli_movie_i_6d9a6a_idx")]},
        ),
        migrations.CreateModel(
            name="MovieComment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="WEBSITE.movie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="movie_comments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["movie", "-created_at"], name="WEBSITE_movieco_movie_i_1d8f9c_idx")]},
        ),
        migrations.AddConstraint(
            model_name="movielike",
            constraint=models.UniqueConstraint(fields=("movie", "user"), name="unique_movie_like"),
        ),
    ]
