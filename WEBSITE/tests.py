from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Genre, Movie


class FilmSiteTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Action")
        self.admin = get_user_model().objects.create_user(username="admin", password="StrongTestPass123!", is_staff=True)
        self.user = get_user_model().objects.create_user(username="viewer", password="StrongTestPass123!")

    @override_settings(CONTENT_ADMIN_USERNAME="admin")
    def test_dashboard_requires_configured_staff_account(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="viewer", password="StrongTestPass123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.client.login(username="admin", password="StrongTestPass123!")
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_public_home_only_shows_published_movies(self):
        published = Movie.objects.create(title="Published", video_url="https://example.com/movie.mp4", is_published=True)
        published.genres.add(self.genre)
        Movie.objects.create(title="Draft", video_url="https://example.com/draft.mp4", is_published=False)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Draft")

    def test_movie_requires_video_source(self):
        self.client.login(username="admin", password="StrongTestPass123!")
        response = self.client.post(reverse("dashboard_movie_create"), {"title": "No Video", "genres": [self.genre.pk], "is_published": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Movie.objects.filter(title="No Video").exists())

    def test_movie_can_upload_video(self):
        self.client.login(username="admin", password="StrongTestPass123!")
        fake_mp4 = SimpleUploadedFile("movie.mp4", b"not-a-real-video", content_type="video/mp4")
        response = self.client.post(
            reverse("dashboard_movie_create"),
            {"title": "Local Movie", "genres": [self.genre.pk], "video_file": fake_mp4, "is_published": "on"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(title="Local Movie").exists())
