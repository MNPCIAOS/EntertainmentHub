from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("account/signup/", views.signup, name="signup"),
    path("account/login/", views.ContentLoginView.as_view(), name="login"),
    path("account/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("account/profile/", views.account_profile, name="profile"),
    path("account/credentials/", views.update_credentials, name="update_credentials"),
    path("account/password/", views.update_password, name="update_password"),
    path("account/premium/pay/", views.start_premium_payment, name="start_premium_payment"),
    path("account/premium/status/<uuid:reference_id>/", views.payment_status, name="payment_status"),
    path("payments/mtn/callback/", views.mtn_callback, name="mtn_callback"),
    path("download/<slug:slug>/", views.download, name="download_movie"),
    path("download/<slug:slug>/episode/<int:episode_id>/", views.download, name="download_episode"),
    path("stream/<slug:slug>/", views.stream_movie, name="stream_movie"),
    path("stream/<slug:slug>/episode/<int:episode_id>/", views.stream_episode, name="stream_episode"),
    path("stream/<slug:slug>/trailer/", views.stream_trailer, name="stream_trailer"),
    path("movie/<slug:slug>/like/", views.toggle_like, name="toggle_like"),
    path("movie/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("contact/", views.contact, name="contact"),
    path("", views.home, name="home"),
    path("genre/<slug:slug>/", views.genre_detail, name="genre_detail"),
    path("movie/<slug:slug>/", views.movie_detail, name="movie_detail"),
    path("/<slug:slug>/", views.watch, name="watch_movie"),
    path("watch/<slug:slug>/episode/<int:episode_id>/", views.watch, name="watch_episode"),
]
