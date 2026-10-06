from pathlib import Path
from django.test import TestCase

from .models import AccountProfile, PaymentTransaction, Movie


class PremiumFeatureTests(TestCase):
    def test_premium_models_and_movie_flag_exist(self):
        self.assertTrue(hasattr(Movie, "is_premium"))
        self.assertTrue(hasattr(AccountProfile, "premium_active"))
        self.assertTrue(hasattr(PaymentTransaction, "reference_id"))

    def test_premium_status_defaults(self):
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.create_user(username="test-user", password="StrongPass123!")
        profile = AccountProfile.objects.create(user=user)
        self.assertEqual(profile.account_type, "free")
        self.assertEqual(profile.premium_status, "free")
