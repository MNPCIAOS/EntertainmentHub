from django.contrib import admin
from .models import Episode, Genre, Movie, MovieComment, MovieLike, Feedback, AccountProfile, PaymentTransaction


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
    list_display = ("title", "content_type", "view_count", "download_count", "is_published", "featured", "created_at")
    list_filter = ("content_type", "is_published", "featured", "genres")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("genres",)
    inlines = [EpisodeInline]
    readonly_fields = ("view_count", "download_count")


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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "category", "name", "email", "phone", "preferred_contact", "created_at")
    list_filter = ("category", "preferred_contact", "created_at")
    search_fields = ("subject", "name", "email", "phone", "location", "message")
    readonly_fields = ("created_at",)


@admin.register(AccountProfile)
class AccountProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "account_type", "premium_status", "payment_number", "approved_at", "subscription_expires_at")
    list_filter = ("account_type", "premium_status")
    search_fields = ("user__username", "user__email", "payment_number")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "currency", "phone_number", "status", "created_at")
    list_filter = ("provider", "status", "currency")
    search_fields = ("user__username", "phone_number", "reference_id", "external_id")
    readonly_fields = ("reference_id", "created_at", "updated_at")
