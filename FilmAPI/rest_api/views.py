from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Film, WatchedFilm, FilmBoxUser
from .serializers import FilmSerializer

def get_user_from_token(request):
    auth = request.headers.get('Authorization')

    if not auth or not auth.startswith('Bearer '):
        return None

    token = auth.split(' ')[1]

    try:
        return FilmBoxUser.objects.get(session_token=token)
    except FilmBoxUser.DoesNotExist:
        return None


class GetMovieView(APIView):

    def get(self, request, film_id):
        try:
            film = Film.objects.get(pk=film_id)
        except Film.DoesNotExist:
            return Response(
                {"error": "Movie not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FilmSerializer(film)
        return Response(serializer.data, status=status.HTTP_200_OK)

class   MarkWatchedView(APIView):

    def put(self, request, movie_id):
        user = get_user_from_token(request)
        if not user:
            return Response(
                {"detail": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            film = Film.objects.get(id=movie_id)
        except Film.DoesNotExist:
            return Response(
                {"detail": "The film does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if WatchedFilm.objects.filter(user=user, film=film).exists():
            return Response(
                {"detail": "Film was already marked as watched."},
                status=status.HTTP_200_OK
            )

        WatchedFilm.objects.create(user=user, film=film)
        return Response(
            {"detail": "Film marked as watched for the first time."},
            status=status.HTTP_201_CREATED
        )
