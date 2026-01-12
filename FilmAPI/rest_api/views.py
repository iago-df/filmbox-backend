from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Film, FavoriteFilm, FilmBoxUser


def get_user_from_token(request):
   auth_header = request.headers.get('Authorization')
   if not auth_header:
       return None


   try:
       token = auth_header.split(' ')[1]
       return FilmBoxUser.objects.get(session_token=token)
   except:
       return None






class LikeFilmView(APIView):
   def put(self, request, film_id):


       user = get_user_from_token(request)
       if not user:
           return Response(
               status=status.HTTP_401_UNAUTHORIZED,
           )



       try:
           film = Film.objects.get(id=film_id)
       except Film.DoesNotExist:
           return Response(
               status=status.HTTP_404_NOT_FOUND,
           )



       if film.year < 1800:
           return Response(
           status=status.HTTP_422_UNPROCESSABLE_ENTITY
       )



       if FavoriteFilm.objects.filter(user=user,film=film).exists():
           return Response(
               status=status.HTTP_200_OK
           )



       FavoriteFilm.objects.create(
           user=user,
           film=film
       )

       return Response(
           status=status.HTTP_201_CREATED
       )

