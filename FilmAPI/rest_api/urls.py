from django.urls import path
from .views import DeleteLikeView

urlpatterns = [
    path('favorites/<int:movie_id>', DeleteLikeView.as_view(), name='delete_like'),
]
