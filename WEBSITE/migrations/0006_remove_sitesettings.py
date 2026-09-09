from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("WEBSITE", "0005_abasobanuzi_short")]

    operations = [migrations.DeleteModel(name="SiteSettings")]
