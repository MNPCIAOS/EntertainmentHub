from urllib.parse import parse_qs, urlparse
import mimetypes

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, CommentForm, FeedbackForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponseBadRequest, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import get_valid_filename

from .models import Abasobanuzi, Country, Episode, Genre, Movie, MovieComment, MovieLike, Feedback


def home(request):
    q = request.GET.get("q", "").strip()
    genre_slug = request.GET.get("genre", "").strip()
    year = request.GET.get("year", "").strip()
    narrator_slug = request.GET.get("umusobanuzi", "").strip()
    content_type = request.GET.get("type", "").strip()
    country_slug = request.GET.get("country", "").strip()
    min_rating = request.GET.get("rating", "").strip()
    max_duration = request.GET.get("duration", "").strip()
    featured_only = request.GET.get("featured", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    movies = Movie.objects.filter(is_published=True).prefetch_related("genres", "abasobanuzi", "countries")
    if q:
        movies = movies.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(abasobanuzi__name__icontains=q)
            | Q(genres__name__icontains=q)
            | Q(countries__name__icontains=q)
        )
    if genre_slug:
        movies = movies.filter(genres__slug=genre_slug)
    if year.isdigit():
        movies = movies.filter(release_year=int(year))
    if narrator_slug:
        movies = movies.filter(abasobanuzi__slug=narrator_slug)
    if content_type in {"movie", "series"}:
        movies = movies.filter(content_type=content_type)
    if country_slug:
        movies = movies.filter(countries__slug=country_slug)
    try:
        if min_rating:
            rating_value = float(min_rating)
            if 0 <= rating_value <= 10:
                movies = movies.filter(rating__gte=rating_value)
    except ValueError:
        pass
    try:
        if max_duration:
            duration_value = int(max_duration)
            if duration_value > 0:
                movies = movies.filter(duration_minutes__lte=duration_value)
    except ValueError:
        pass
    if featured_only == "1":
        movies = movies.filter(featured=True)

    sort_map = {
        "newest": "-created_at",
        "oldest": "created_at",
        "year_desc": "-release_year",
        "year_asc": "release_year",
        "rating": "-rating",
        "title": "title",
    }
    movies = movies.order_by(sort_map.get(sort, "-created_at"))
    paginator = Paginator(movies.distinct(), 24)
    page = paginator.get_page(request.GET.get("page"))

    featured = Movie.objects.filter(is_published=True, featured=True).prefetch_related("genres", "abasobanuzi", "countries")[:6]
    genres = Genre.objects.all()
    narrators = Abasobanuzi.objects.all()
    countries = Country.objects.all()
    selected_country = Country.objects.filter(slug=country_slug).first() if country_slug else None
    years = Movie.objects.filter(is_published=True, release_year__isnull=False).values_list("release_year", flat=True).distinct().order_by("-release_year")

    # Keep the existing library/filter view, and additionally group the published
    # library into genre rows for the homepage.
    genre_sections = []
    for genre in genres:
        genre_movies = list(
            Movie.objects.filter(
                is_published=True, genres=genre
            ).prefetch_related("genres", "abasobanuzi", "countries").order_by("-created_at")[:8]
        )
        if genre_movies:
            genre_sections.append({"genre": genre, "movies": genre_movies})

    filter_params = request.GET.copy()
    filter_params.pop("page", None)

    return render(request, "WEBSITE/home.html", {
        "page": page, "featured": featured, "genres": genres, "narrators": narrators, "countries": countries, "years": years,
        "q": q, "active_genre": genre_slug, "active_year": year, "active_narrator": narrator_slug,
        "active_type": content_type, "active_country": country_slug, "active_country_name": selected_country.name if selected_country else "", "active_rating": min_rating,
        "active_duration": max_duration, "active_featured": featured_only, "active_sort": sort,
        "filter_query": filter_params.urlencode(), "genre_sections": genre_sections,
    })


def contact(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_authenticated and not feedback.name:
            feedback.name = request.user.get_full_name() or request.user.username
        if request.user.is_authenticated and not feedback.email:
            feedback.email = request.user.email
        feedback.save()
        from django.contrib import messages
        messages.success(request, "Thank you. Your feedback has been received.")
        return redirect("contact")
    return render(request, "WEBSITE/contact.html", {"form": form})


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    movies = Movie.objects.filter(is_published=True, genres=genre).prefetch_related("genres")
    paginator = Paginator(movies.distinct(), 24)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "WEBSITE/genre.html", {"genre": genre, "page": page})


def movie_detail(request, slug):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres", "abasobanuzi", "countries", "episodes", "comments__user"),
        slug=slug, is_published=True
    )
    episodes = movie.episodes.filter(is_published=True)
    seasons = {}
    for episode in episodes:
        seasons.setdefault(episode.season_number, []).append(episode)
    comments = movie.comments.select_related("user").all()[:50]
    liked = request.user.is_authenticated and MovieLike.objects.filter(movie=movie, user=request.user).exists()
    comment_form = CommentForm()

    trailer_player = None
    if movie.trailer_file:
        trailer_player = {
            "kind": "video",
            "url": reverse("stream_trailer", kwargs={"slug": movie.slug}),
        }
    elif movie.trailer_url:
        trailer_player = normalize_video_url(movie.trailer_url)

    return render(request, "WEBSITE/movie_detail.html", {
        "movie": movie, "seasons": seasons, "comments": comments,
        "comment_form": comment_form, "liked": liked,
        "like_count": movie.likes.count(),
        "trailer_player": trailer_player,
    })


def watch(request, slug, episode_id=None):
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    media = get_object_or_404(Episode, pk=episode_id, movie=movie, is_published=True) if episode_id else movie
    video_url = media.video_src
    if not video_url:
        raise Http404("No video has been configured for this item.")
    if getattr(media, "video_file", None):
        player = {"kind": "video", "url": reverse("stream_episode" if episode_id else "stream_movie", kwargs={"slug": slug, **({"episode_id": episode_id} if episode_id else {})})}
    else:
        player = normalize_video_url(video_url)
    return render(request, "WEBSITE/watch.html", {
        "movie": movie, "media": media, "player": player, "download_url": media.download_src,
        "like_count": movie.likes.count(),
    })


def _range_response(request, file_field, content_type=None):
    try:
        size = file_field.size
        file_obj = file_field.open("rb")
        content_type = content_type or mimetypes.guess_type(file_field.name)[0] or "application/octet-stream"
    except (FileNotFoundError, ValueError, OSError):
        raise Http404("The video file is missing.")

    range_header = request.headers.get("Range")
    if not range_header or not range_header.startswith("bytes="):
        response = FileResponse(file_obj, content_type=content_type)
        response["Content-Length"] = str(size)
        response["Accept-Ranges"] = "bytes"
        response["Cache-Control"] = "public, max-age=3600"
        return response

    try:
        start_s, end_s = range_header.replace("bytes=", "", 1).split("-", 1)
        start = int(start_s) if start_s else max(0, size - int(end_s))
        end = int(end_s) if end_s else size - 1
        if start < 0 or start >= size or end < start:
            raise ValueError
        end = min(end, size - 1)
    except (ValueError, TypeError):
        file_obj.close()
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{size}"
        return response

    length = end - start + 1
    file_obj.seek(start)

    def iterator():
        remaining = length
        try:
            while remaining:
                chunk = file_obj.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk
        finally:
            file_obj.close()

    response = StreamingHttpResponse(iterator(), status=206, content_type=content_type)
    response["Content-Length"] = str(length)
    response["Content-Range"] = f"bytes {start}-{end}/{size}"
    response["Accept-Ranges"] = "bytes"
    response["Cache-Control"] = "public, max-age=3600"
    return response


def stream_movie(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    if not movie.video_file:
        raise Http404("No local video file is configured.")
    return _range_response(request, movie.video_file)


def stream_episode(request, slug, episode_id):
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    episode = get_object_or_404(Episode, pk=episode_id, movie=movie, is_published=True)
    if not episode.video_file:
        raise Http404("No local episode video file is configured.")
    return _range_response(request, episode.video_file)


def stream_trailer(request, slug):
    """Stream a locally uploaded trailer with byte-range support."""
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    if not movie.trailer_file:
        raise Http404("No local trailer file is configured.")
    return _range_response(request, movie.trailer_file)


def download(request, slug, episode_id=None):
    """Download a locally uploaded authorized media file. Cloud URLs remain provider links."""
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    media = get_object_or_404(Episode, pk=episode_id, movie=movie, is_published=True) if episode_id else movie
    local_file = getattr(media, "download_file", None)
    if not local_file:
        return HttpResponseBadRequest("No local download file is configured.")
    try:
        filename = get_valid_filename(local_file.name.rsplit("/", 1)[-1]) or "download"
        return FileResponse(local_file.open("rb"), as_attachment=True, filename=filename)
    except (FileNotFoundError, ValueError):
        raise Http404("The download file is missing.")



@login_required
def toggle_like(request, slug):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required.")
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    like, created = MovieLike.objects.get_or_create(movie=movie, user=request.user)
    if not created:
        like.delete()
    return redirect(f"{reverse('movie_detail', kwargs={'slug': slug})}#community")


@login_required
def add_comment(request, slug):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required.")
    movie = get_object_or_404(Movie, slug=slug, is_published=True)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
    return redirect(f"{reverse('movie_detail', kwargs={'slug': slug})}#community")


@login_required
def delete_comment(request, comment_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required.")
    comment = get_object_or_404(MovieComment, pk=comment_id)
    if comment.user_id != request.user.id and request.user.username.casefold() != settings.CONTENT_ADMIN_USERNAME.casefold():
        return HttpResponse("Not allowed.", status=403)
    slug = comment.movie.slug
    comment.delete()
    return redirect(f"{reverse('movie_detail', kwargs={'slug': slug})}#community")



def normalize_video_url(url):
    """Return a player-safe representation for YouTube, Google Drive, or direct media URLs."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":", 1)[0]
    if host.endswith("youtube.com") or host == "youtu.be":
        video_id = ""
        if host == "youtu.be":
            video_id = parsed.path.strip("/").split("/")[0]
        else:
            video_id = parse_qs(parsed.query).get("v", [""])[0]
            if not video_id and parsed.path.startswith("/embed/"):
                video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        if video_id:
            return {"kind": "iframe", "url": f"https://www.youtube.com/embed/{video_id}?rel=0"}
    if host == "drive.google.com" or host.endswith(".drive.google.com"):
        parts = [p for p in parsed.path.split("/") if p]
        if "d" in parts:
            idx = parts.index("d")
            if idx + 1 < len(parts):
                file_id = parts[idx + 1]
                return {"kind": "iframe", "url": f"https://drive.google.com/file/d/{file_id}/preview"}
        file_id = parse_qs(parsed.query).get("id", [""])[0]
        if file_id:
            return {"kind": "iframe", "url": f"https://drive.google.com/file/d/{file_id}/preview"}
    return {"kind": "video", "url": url}


class ContentLoginView(LoginView):
    template_name = "WEBSITE/login.html"

    def get_success_url(self):
        # The configured content administrator goes straight to the publishing dashboard.
        if (self.request.user.is_authenticated
                and self.request.user.username.casefold() == settings.CONTENT_ADMIN_USERNAME.casefold()
                and self.request.user.is_staff):
            return reverse("dashboard")
        return super().get_success_url()


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "WEBSITE/signup.html", {"form": form})


@login_required
def account_profile(request):
    return render(request, "WEBSITE/profile.html")
