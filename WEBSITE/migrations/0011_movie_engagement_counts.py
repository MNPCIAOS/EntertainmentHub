from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WEBSITE", "0010_feedback_contact_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="view_count",
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="movie",
            name="download_count",
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
