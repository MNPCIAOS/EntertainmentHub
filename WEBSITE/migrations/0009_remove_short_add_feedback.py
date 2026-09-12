from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WEBSITE", "0008_rename_website_movi_is_publ_8c1b10_idx_website_mov_is_publ_de4ba4_idx_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Short",
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("subject", models.CharField(blank=True, max_length=200)),
                ("message", models.TextField(max_length=3000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
