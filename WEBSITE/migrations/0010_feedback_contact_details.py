from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WEBSITE", "0009_remove_short_add_feedback"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="phone",
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name="feedback",
            name="category",
            field=models.CharField(
                choices=[
                    ("feedback", "General feedback"),
                    ("request", "Movie / series request"),
                    ("recommendation", "Movie / series recommendation"),
                    ("problem", "Report a problem"),
                    ("correction", "Content correction"),
                    ("partnership", "Partnership / business"),
                    ("other", "Other"),
                ],
                default="feedback",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="location",
            field=models.CharField(blank=True, help_text="City, country or area (optional).", max_length=160),
        ),
        migrations.AddField(
            model_name="feedback",
            name="preferred_contact",
            field=models.CharField(
                choices=[
                    ("email", "Email"),
                    ("phone", "Phone call"),
                    ("whatsapp", "WhatsApp"),
                    ("none", "No reply needed"),
                ],
                default="email",
                max_length=20,
            ),
        ),
    ]
