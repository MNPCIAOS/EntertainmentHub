from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("WEBSITE", "0003_image_size_validation")]

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("singleton_key", models.CharField(default="default", editable=False, max_length=20, unique=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("tiktok_url", models.URLField(blank=True)),
                ("instagram_url", models.URLField(blank=True)),
                ("x_url", models.URLField(blank=True)),
                ("youtube_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Site settings", "verbose_name_plural": "Site settings"},
        ),
    ]
