from django.urls import path
from .views import LikeFilmView


urlpatterns = [
   path('likes/<int:film_id>/', LikeFilmView.as_view(), name='like_film'),
]
