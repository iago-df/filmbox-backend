from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FavoriteFilm, FilmBoxUser


def get_user_from_token(request):
    auth = request.headers.get('Authorization')

    if not auth or not auth.startswith('Bearer '):
        return None

    token = auth.split(' ')[1]

    try:
        return FilmBoxUser.objects.get(session_token=token)
    except FilmBoxUser.DoesNotExist:
        return None


class DeleteLikeView(APIView):

    def delete(self, request, movie_id):
        user = get_user_from_token(request)
        if not user:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            like = FavoriteFilm.objects.get(user=user, film_id=movie_id)
        except FavoriteFilm.DoesNotExist:
            return Response(
                {"detail": "Like not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        like.delete()
        return Response(
            {"detail": "Like deleted"},
            status=status.HTTP_204_NO_CONTENT
        )



# Create your views here.
