from django.urls import path
from .views import MovieReviewView

urlpatterns = [
    path('movies/<int:id>/reviews', MovieReviewView.as_view(), name='movie_review'),
]
