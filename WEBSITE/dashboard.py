from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EpisodeForm, GenreForm, MovieForm
from .models import Abasobanuzi, Country, Episode, Genre, Movie, MovieComment, Feedback


def is_content_admin(user):
    return user.is_authenticated and user.is_staff and user.username == settings.CONTENT_ADMIN_USERNAME


admin_required = user_passes_test(is_content_admin, login_url="login")


@admin_required
def dashboard(request):
    context = {
        "movie_count": Movie.objects.count(),
        "published_count": Movie.objects.filter(is_published=True).count(),
        "genre_count": Genre.objects.count(),
        "country_count": Country.objects.count(),
        "episode_count": Episode.objects.count(),
        "comment_count": MovieComment.objects.count(),
        "narrator_count": Abasobanuzi.objects.count(),
        "feedback_count": Feedback.objects.count(),
        "recent_movies": Movie.objects.prefetch_related("genres", "abasobanuzi", "countries")[:8],
    }
    return render(request, "WEBSITE/dashboard.html", context)


@admin_required
def movie_list(request):
    movies = Movie.objects.prefetch_related("genres", "abasobanuzi", "countries").all()
    return render(request, "WEBSITE/dashboard_movies.html", {"movies": movies})


@admin_required
def movie_create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        movie = form.save()
        messages.success(request, f'“{movie.title}” was saved successfully.')
        return redirect("dashboard_movies")
    return render(request, "WEBSITE/dashboard_movie_form.html", {"form": form, "heading": "Host & Publish New Movie", "submit_text": "Save Movie"})


@admin_required
def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if request.method == "POST" and form.is_valid():
        movie = form.save()
        messages.success(request, f'“{movie.title}” was updated successfully.')
        return redirect("dashboard_movies")
    return render(request, "WEBSITE/dashboard_movie_form.html", {"form": form, "heading": f"Edit: {movie.title}", "submit_text": "Update Movie", "movie": movie})


@admin_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        title = movie.title
        movie.delete()
        messages.success(request, f'“{title}” was deleted.')
        return redirect("dashboard_movies")
    return render(request, "WEBSITE/dashboard_confirm.html", {"object": movie, "kind": "movie", "cancel_url": "dashboard_movies"})


@admin_required
def episode_list(request):
    episodes = Episode.objects.select_related("movie").all()
    return render(request, "WEBSITE/dashboard_episodes.html", {"episodes": episodes})


@admin_required
def episode_create(request):
    form = EpisodeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        episode = form.save()
        messages.success(request, f'Episode “{episode.title}” was saved successfully.')
        return redirect("dashboard_episodes")
    return render(request, "WEBSITE/dashboard_episode_form.html", {"form": form, "heading": "Add Episode", "submit_text": "Save Episode"})


@admin_required
def episode_edit(request, pk):
    episode = get_object_or_404(Episode, pk=pk)
    form = EpisodeForm(request.POST or None, request.FILES or None, instance=episode)
    if request.method == "POST" and form.is_valid():
        episode = form.save()
        messages.success(request, f'Episode “{episode.title}” was updated successfully.')
        return redirect("dashboard_episodes")
    return render(request, "WEBSITE/dashboard_episode_form.html", {"form": form, "heading": f"Edit: {episode.title}", "submit_text": "Update Episode", "episode": episode})


@admin_required
def episode_delete(request, pk):
    episode = get_object_or_404(Episode, pk=pk)
    if request.method == "POST":
        title = episode.title
        episode.delete()
        messages.success(request, f'Episode “{title}” was deleted.')
        return redirect("dashboard_episodes")
    return render(request, "WEBSITE/dashboard_confirm.html", {"object": episode, "kind": "episode", "cancel_url": "dashboard_episodes"})


@admin_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "WEBSITE/dashboard_genres.html", {"genres": genres})


@admin_required
def genre_create(request):
    form = GenreForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        genre = form.save()
        messages.success(request, f'Genre “{genre.name}” was created.')
        return redirect("dashboard_genres")
    return render(request, "WEBSITE/dashboard_genre_form.html", {"form": form, "heading": "Create genre", "submit_text": "Create genre"})


@admin_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    form = GenreForm(request.POST or None, instance=genre)
    if request.method == "POST" and form.is_valid():
        genre = form.save()
        messages.success(request, f'Genre “{genre.name}” was updated.')
        return redirect("dashboard_genres")
    return render(request, "WEBSITE/dashboard_genre_form.html", {"form": form, "heading": f"Edit: {genre.name}", "submit_text": "Update genre", "genre": genre})


@admin_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == "POST":
        name = genre.name
        genre.delete()
        messages.success(request, f'Genre “{name}” was deleted.')
        return redirect("dashboard_genres")
    return render(request, "WEBSITE/dashboard_confirm.html", {"object": genre, "kind": "genre", "cancel_url": "dashboard_genres"})


@admin_required
def comment_list(request):
    comments = MovieComment.objects.select_related("movie", "user").all()
    return render(request, "WEBSITE/dashboard_comments.html", {"comments": comments})


@admin_required
def comment_delete(request, pk):
    comment = get_object_or_404(MovieComment, pk=pk)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("dashboard_comments")
    return render(request, "WEBSITE/dashboard_confirm.html", {"object": comment, "kind": "comment", "cancel_url": "dashboard_comments"})


@admin_required
def narrator_list(request):
    from .models import Abasobanuzi
    narrators = Abasobanuzi.objects.all()
    return render(request, "WEBSITE/dashboard_narrators.html", {"narrators": narrators})


@admin_required
def narrator_create(request):
    from .forms import AbasobanuziForm
    form = AbasobanuziForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        narrator = form.save()
        messages.success(request, f'Umusobanuzi “{narrator.name}” was created.')
        return redirect("dashboard_narrators")
    return render(request, "WEBSITE/dashboard_narrator_form.html", {"form": form, "heading": "Add Umusobanuzi", "submit_text": "Create"})


@admin_required
def narrator_edit(request, pk):
    from .forms import AbasobanuziForm
    from .models import Abasobanuzi
    narrator = get_object_or_404(Abasobanuzi, pk=pk)
    form = AbasobanuziForm(request.POST or None, instance=narrator)
    if request.method == "POST" and form.is_valid():
        narrator = form.save()
        messages.success(request, f'Umusobanuzi “{narrator.name}” was updated.')
        return redirect("dashboard_narrators")
    return render(request, "WEBSITE/dashboard_narrator_form.html", {"form": form, "heading": f"Edit: {narrator.name}", "submit_text": "Update", "narrator": narrator})


@admin_required
def narrator_delete(request, pk):
    from .models import Abasobanuzi
    narrator = get_object_or_404(Abasobanuzi, pk=pk)
    if request.method == "POST":
        name = narrator.name
        narrator.delete()
        messages.success(request, f'Umusobanuzi “{name}” was deleted.')
        return redirect("dashboard_narrators")
    return render(request, "WEBSITE/dashboard_confirm.html", {"object": narrator, "kind": "umusobanuzi", "cancel_url": "dashboard_narrators"})



@admin_required
def feedback_list(request):
    feedback = Feedback.objects.all()
    return render(request, "WEBSITE/dashboard_feedback.html", {"feedback": feedback})


@admin_required
def feedback_delete(request, pk):
    item = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Feedback deleted.")
        return redirect("dashboard_feedback")
    return render(request, "WEBSITE/dashboard_confirm.html", {
        "object": item, "kind": "feedback", "cancel_url": "dashboard_feedback"
    })
