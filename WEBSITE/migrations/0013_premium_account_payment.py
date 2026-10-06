from django.db import migrations, models
import django.db.models.deletion
import django.db.models

class Migration(migrations.Migration):
    dependencies = [("WEBSITE", "0012_announcement")]
    operations = [
        migrations.AddField(
            model_name="movie",
            name="is_premium",
            field=models.BooleanField(default=False, help_text="Only active premium subscribers can watch this content."),
        ),
        migrations.CreateModel(
            name="AccountProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("account_type", models.CharField(choices=[("free","Free"),("premium","Premium")], default="free", max_length=10)),
                ("premium_status", models.CharField(choices=[("free","Free"),("pending","Pending approval"),("active","Active"),("expired","Expired"),("rejected","Rejected")], default="free", max_length=12)),
                ("payment_number", models.CharField(blank=True, max_length=20)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("subscription_expires_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="account_profile", to="auth.user")),
            ],
        ),
        migrations.CreateModel(
            name="PaymentTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference_id", models.UUIDField(unique=True)),
                ("provider", models.CharField(choices=[("mtn_momo","MTN Mobile Money")], default="mtn_momo", max_length=20)),
                ("phone_number", models.CharField(max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="RWF", max_length=5)),
                ("status", models.CharField(choices=[("pending","Pending"),("successful","Successful"),("failed","Failed"),("cancelled","Cancelled")], default="pending", max_length=12)),
                ("external_id", models.CharField(blank=True, max_length=160)),
                ("provider_message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payment_transactions", to="auth.user")),
            ],
            options={"ordering":["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="paymenttransaction",
            index=models.Index(fields=["user","status","-created_at"], name="WEBSITE_pay_user_id_8b2c18_idx"),
        ),
    ]
