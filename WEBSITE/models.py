from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from urllib.parse import parse_qs, urlparse


VIDEO_EXTENSIONS = ["mp4", "webm", "ogg"]
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
MAX_MEDIA_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB per uploaded video/download
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB per uploaded image


def validate_media_size(file):
    if file and file.size > MAX_MEDIA_SIZE:
        raise ValidationError("The uploaded file is larger than the 2 GB limit.")


def video_validators():
    return [FileExtensionValidator(VIDEO_EXTENSIONS), validate_media_size]


def validate_image_size(file):
    if file and file.size > MAX_IMAGE_SIZE:
        raise ValidationError("The uploaded image is larger than the 10 MB limit.")

def image_validators():
    return [FileExtensionValidator(IMAGE_EXTENSIONS), validate_image_size]

def normalize_image_url(url):
    """Convert common image-hosting page URLs into browser-displayable image URLs."""
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
        host = parsed.netloc.lower().split(":", 1)[0]
        if host == "drive.google.com" or host.endswith(".drive.google.com"):
            parts = [part for part in parsed.path.split("/") if part]
            file_id = ""
            if "d" in parts:
                idx = parts.index("d")
                if idx + 1 < len(parts):
                    file_id = parts[idx + 1]
            if not file_id:
                file_id = parse_qs(parsed.query).get("id", [""])[0]
            if file_id:
                return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1600"
        if host == "dropbox.com" or host.endswith(".dropbox.com"):
            if "dl=0" in parsed.query:
                return url.replace("dl=0", "raw=1")
        return url.strip()
    except (TypeError, ValueError):
        return url


def unique_slug(instance, value, queryset):
    base = slugify(value) or "item"
    slug = base
    counter = 2
    while queryset.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.slug = unique_slug(self, self.name, Genre.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Abasobanuzi(models.Model):
    """People credited as Abasobanuzi; managed through the custom dashboard."""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Umusobanuzi"
        verbose_name_plural = "Abasobanuzi"

    def save(self, *args, **kwargs):
        self.slug = unique_slug(self, self.name, Abasobanuzi.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    """Country associated with a film's production, filming, or cast origin."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.slug = unique_slug(self, self.name, Country.objects)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Movie(models.Model):
    TYPE_CHOICES = [("movie", "Movie"), ("series", "Series")]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)

    poster_url = models.URLField(blank=True, help_text="Public poster image URL (optional).")
    poster_image = models.ImageField(upload_to="movies/posters/", blank=True, validators=image_validators())
    backdrop_url = models.URLField(blank=True, help_text="Public backdrop image URL (optional).")
    backdrop_image = models.ImageField(upload_to="movies/backdrops/", blank=True, validators=image_validators())

    video_url = models.URLField(blank=True, help_text="Cloud/direct video URL. Use the upload field below for local files.")
    video_file = models.FileField(upload_to="movies/videos/", blank=True, validators=video_validators())
    download_url = models.URLField(blank=True, help_text="Authorized download URL (optional).")
    download_file = models.FileField(upload_to="movies/downloads/", blank=True, validators=video_validators())
    trailer_url = models.URLField(blank=True)
    trailer_file = models.FileField(upload_to="movies/trailers/", blank=True, validators=video_validators())

    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="movie")
    release_year = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1888), MaxValueValidator(2100)])
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10000)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    abasobanuzi = models.ManyToManyField(Abasobanuzi, related_name="movies", blank=True)
    countries = models.ManyToManyField(Country, related_name="movies", blank=True, help_text="Production, filming, or cast-origin countries.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_published", "featured"])]

    def save(self, *args, **kwargs):
        self.slug = unique_slug(self, self.title, Movie.objects)
        super().save(*args, **kwargs)

    @property
    def poster_src(self):
        return self.poster_image.url if self.poster_image else normalize_image_url(self.poster_url)

    @property
    def poster_fallback_src(self):
        return normalize_image_url(self.poster_url)

    @property
    def backdrop_src(self):
        return self.backdrop_image.url if self.backdrop_image else normalize_image_url(self.backdrop_url)

    @property
    def video_src(self):
        return self.video_file.url if self.video_file else self.video_url

    @property
    def download_src(self):
        return self.download_file.url if self.download_file else self.download_url

    @property
    def trailer_src(self):
        return self.trailer_file.url if self.trailer_file else self.trailer_url

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Episode(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="episodes")
    season_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    episode_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    thumbnail_image = models.ImageField(upload_to="episodes/thumbnails/", blank=True, validators=image_validators())
    video_url = models.URLField(blank=True, help_text="Cloud/direct video URL. Use the upload field below for local files.")
    video_file = models.FileField(upload_to="episodes/videos/", blank=True, validators=video_validators())
    download_url = models.URLField(blank=True, help_text="Authorized download URL (optional).")
    download_file = models.FileField(upload_to="episodes/downloads/", blank=True, validators=video_validators())
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10000)])
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["season_number", "episode_number"]
        constraints = [
            models.UniqueConstraint(fields=["movie", "season_number", "episode_number"], name="unique_episode")
        ]

    @property
    def thumbnail_src(self):
        return self.thumbnail_image.url if self.thumbnail_image else normalize_image_url(self.thumbnail_url)

    @property
    def thumbnail_fallback_src(self):
        return normalize_image_url(self.thumbnail_url)

    @property
    def video_src(self):
        return self.video_file.url if self.video_file else self.video_url

    @property
    def download_src(self):
        return self.download_file.url if self.download_file else self.download_url

    def __str__(self):
        return f"{self.movie.title} — S{self.season_number:02d}E{self.episode_number:02d} — {self.title}"



class Feedback(models.Model):
    """Feedback submitted by visitors, including users who are not registered."""
    CATEGORY_CHOICES = [
        ("feedback", "General feedback"),
        ("request", "Movie / series request"),
        ("recommendation", "Movie / series recommendation"),
        ("problem", "Report a problem"),
        ("correction", "Content correction"),
        ("partnership", "Partnership / business"),
        ("other", "Other"),
    ]
    CONTACT_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone call"),
        ("whatsapp", "WhatsApp"),
        ("none", "No reply needed"),
    ]
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="feedback")
    subject = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=160, blank=True, help_text="City, country or area (optional).")
    preferred_contact = models.CharField(max_length=20, choices=CONTACT_CHOICES, default="email")
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject or f"Feedback from {self.name or 'Anonymous'}"


class MovieLike(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="movie_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "user"], name="unique_movie_like"),
        ]
        indexes = [models.Index(fields=["movie", "created_at"])]

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"


class MovieComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="movie_comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["movie", "-created_at"])]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie.title}"

