from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FilmBoxUser, Film, WatchedFilm


def get_authenticated_user(request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth[len("Bearer "):].strip()
    try:
        return FilmBoxUser.objects.get(session_token=token)
    except FilmBoxUser.DoesNotExist:
        return None


class DeleteWatchedView(APIView):

    def delete(self, request, movie_id):
        # 401 – Usuario no autenticado
        user = get_authenticated_user(request)
        if user is None:
            return Response(
                {"detail": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 404 – La película no existe
        try:
            film = Film.objects.get(pk=movie_id)
        except Film.DoesNotExist:
            return Response(
                {"detail": "Movie not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 404 – La película no estaba en watched de este usuario
        try:
            entry = WatchedFilm.objects.get(user=user, film=film)
        except WatchedFilm.DoesNotExist:
            return Response(
                {"detail": "Movie not in watched list."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 200 – Se elimina
        entry.delete()
        return Response(
            {"detail": "Movie removed from watched list."},
            status=status.HTTP_200_OK
        )
