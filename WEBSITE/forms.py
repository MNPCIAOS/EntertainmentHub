from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import Abasobanuzi, Country, Genre, Movie, Episode, MovieComment, Feedback


class SignupForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        if username.casefold() == settings.CONTENT_ADMIN_USERNAME.casefold():
            raise forms.ValidationError("That username is reserved for the content administrator.")
        return username


class MovieForm(forms.ModelForm):
    abasobanuzi = forms.ModelMultipleChoiceField(
        queryset=Abasobanuzi.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 7, "class": "multi-select"}),
    )
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 7, "class": "multi-select"}),
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        error_messages={"required": "Select at least one genre."},
    )

    class Meta:
        model = Movie
        fields = [
            "title", "description", "abasobanuzi", "genres", "countries", "poster_url", "poster_image", "backdrop_url", "backdrop_image",
            "video_url", "video_file", "download_url", "download_file", "trailer_url", "trailer_file",
            "content_type", "release_year", "duration_minutes", "rating", "featured", "is_published",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6, "placeholder": "Umusobanuzi / description y’umukino..."}),
            "release_year": forms.NumberInput(attrs={"min": 1888, "max": 2100}),
            "duration_minutes": forms.NumberInput(attrs={"min": 1, "max": 10000}),
            "rating": forms.NumberInput(attrs={"min": 0, "max": 10, "step": "0.1"}),
            "video_url": forms.URLInput(attrs={"placeholder": "Cloud/direct video URL (optional if uploading a file)"}),
            "download_url": forms.URLInput(attrs={"placeholder": "Authorized download URL (optional)"}),
            "poster_url": forms.URLInput(attrs={"placeholder": "Poster image URL (optional if uploading a file)"}),
            "backdrop_url": forms.URLInput(attrs={"placeholder": "Backdrop image URL (optional if uploading a file)"}),
            "trailer_url": forms.URLInput(attrs={"placeholder": "Trailer URL (optional)"}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("video_url") and not cleaned.get("video_file"):
            self.add_error("video_url", "Add a video URL or upload a video file.")
        return cleaned


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = [
            "movie", "season_number", "episode_number", "title", "description", "thumbnail_url", "thumbnail_image",
            "video_url", "video_file", "download_url", "download_file", "duration_minutes", "is_published",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "video_url": forms.URLInput(attrs={"placeholder": "Episode video URL (optional if uploading a file)"}),
            "download_url": forms.URLInput(attrs={"placeholder": "Authorized download URL (optional)"}),
            "thumbnail_url": forms.URLInput(attrs={"placeholder": "Episode thumbnail URL (optional if uploading a file)"}),
            "duration_minutes": forms.NumberInput(attrs={"min": 1, "max": 10000}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("video_url") and not cleaned.get("video_file"):
            self.add_error("video_url", "Add an episode video URL or upload a video file.")
        return cleaned


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "maxlength": 1000, "placeholder": "Write your comment..."}),
        }
        labels = {"text": "Comment"}


class AbasobanuziForm(forms.ModelForm):
    class Meta:
        model = Abasobanuzi
        fields = ["name"]



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "phone", "category", "subject", "location", "preferred_contact", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name (optional)", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com (optional)", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+250 7xx xxx xxx (optional)", "autocomplete": "tel"}),
            "category": forms.Select(),
            "subject": forms.TextInput(attrs={"placeholder": "Give your message a short title"}),
            "location": forms.TextInput(attrs={"placeholder": "City / country (optional)"}),
            "preferred_contact": forms.Select(),
            "message": forms.Textarea(attrs={"rows": 8, "placeholder": "Tell us what you need. You can request a movie, recommend a title, report a problem, suggest a feature, or simply share your experience..."}),
        }
        labels = {
            "name": "Your name",
            "email": "Email address",
            "phone": "Phone / WhatsApp",
            "category": "What can we help with?",
            "subject": "Subject",
            "location": "Your location",
            "preferred_contact": "Preferred reply",
            "message": "Your message",
        }
