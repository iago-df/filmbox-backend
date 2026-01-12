from django.urls import path
from . import views
from .views import DeleteWatchedView

urlpatterns = [
    path('watched/<int:movie_id>', DeleteWatchedView.as_view(), name='delete_watched_movie'),
]