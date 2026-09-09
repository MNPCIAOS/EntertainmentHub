from django.contrib import admin
from .models import Episode, Genre, Movie, MovieComment, MovieLike


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    fields = ("season_number", "episode_number", "title", "video_file", "video_url", "is_published")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "content_type", "is_published", "featured", "created_at")
    list_filter = ("content_type", "is_published", "featured", "genres")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("genres",)
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("movie", "season_number", "episode_number", "title", "is_published")
    list_filter = ("is_published", "movie")
    search_fields = ("title", "description", "movie__title")


@admin.register(MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "created_at", "text_preview")
    list_filter = ("created_at",)
    search_fields = ("movie__title", "user__username", "text")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Comment")
    def text_preview(self, obj):
        return obj.text[:80]


@admin.register(MovieLike)
class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("movie__title", "user__username")
    readonly_fields = ("created_at",)
