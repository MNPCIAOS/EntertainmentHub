from django.urls import path
from . import dashboard

urlpatterns = [
    path('', dashboard.dashboard, name='dashboard'),
    path('movies/', dashboard.movie_list, name='dashboard_movies'),
    path('movies/new/', dashboard.movie_create, name='dashboard_movie_create'),
    path('movies/<int:pk>/edit/', dashboard.movie_edit, name='dashboard_movie_edit'),
    path('movies/<int:pk>/delete/', dashboard.movie_delete, name='dashboard_movie_delete'),
    path('episodes/', dashboard.episode_list, name='dashboard_episodes'),
    path('episodes/new/', dashboard.episode_create, name='dashboard_episode_create'),
    path('episodes/<int:pk>/edit/', dashboard.episode_edit, name='dashboard_episode_edit'),
    path('episodes/<int:pk>/delete/', dashboard.episode_delete, name='dashboard_episode_delete'),
    path('genres/', dashboard.genre_list, name='dashboard_genres'),
    path('genres/new/', dashboard.genre_create, name='dashboard_genre_create'),
    path('genres/<int:pk>/edit/', dashboard.genre_edit, name='dashboard_genre_edit'),
    path('genres/<int:pk>/delete/', dashboard.genre_delete, name='dashboard_genre_delete'),
    path('narrators/', dashboard.narrator_list, name='dashboard_narrators'),
    path('narrators/new/', dashboard.narrator_create, name='dashboard_narrator_create'),
    path('narrators/<int:pk>/edit/', dashboard.narrator_edit, name='dashboard_narrator_edit'),
    path('narrators/<int:pk>/delete/', dashboard.narrator_delete, name='dashboard_narrator_delete'),
    path('comments/', dashboard.comment_list, name='dashboard_comments'),
    path('comments/<int:pk>/delete/', dashboard.comment_delete, name='dashboard_comment_delete'),
    path('shorts/', dashboard.short_list, name='dashboard_shorts'),
    path('shorts/new/', dashboard.short_create_admin, name='dashboard_short_create'),
    path('shorts/<int:pk>/edit/', dashboard.short_edit, name='dashboard_short_edit'),
    path('shorts/<int:pk>/delete/', dashboard.short_delete, name='dashboard_short_delete'),
    path('shorts/<int:pk>/<str:status>/', dashboard.short_status, name='dashboard_short_status'),
]
