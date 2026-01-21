import requests
from django.conf import settings
from .models import Film, Category, CategoryFilm

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def fetch_tmdb_movie(tmdb_id: int):
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "es-ES",
        "append_to_response": "credits,videos",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def import_movie_from_tmdb(tmdb_id: int) -> Film:
    data = fetch_tmdb_movie(tmdb_id)

    # --- Director ---
    director_name = "Unknown"
    credits = data.get("credits", {})
    for member in credits.get("crew", []):
        if member.get("job") == "Director":
            director_name = member.get("name") or "Unknown"
            break

    # --- Poster ---
    poster_path = data.get("poster_path")
    image_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""

    # --- Trailer (YouTube) ---
    trailer_url = ""
    videos = data.get("videos", {}).get("results", [])
    for v in videos:
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
            break

    # --- Año ---
    release_date = data.get("release_date")
    year = int(release_date[:4]) if release_date else 0

    # --- Duración ---
    length = data.get("runtime") or 0

    # --- Descripción ---
    overview = data.get("overview") or ""
    overview = overview[:100]  # porque tu modelo solo permite 100 chars

    # DEDUPLICACIÓN (por title+year)
    existing = Film.objects.filter(title=data.get("title"), year=year).first()
    if existing:
        return existing

    # --- Crear Film ---
    film = Film.objects.create(
        title=data.get("title") or data.get("original_title") or "Sin título",
        description=overview,
        image_url=image_url,
        film_url=f"https://www.themoviedb.org/movie/{tmdb_id}",
        trailer_url=trailer_url,
        year=year,
        length=length,
        director=director_name,
    )

    # --- Categorías ---
    for g in data.get("genres", []):
        cat_title = g.get("name")
        if not cat_title:
            continue

        category, _ = Category.objects.get_or_create(
            title=cat_title,
            defaults={"image_url": ""},
        )
        CategoryFilm.objects.create(category=category, film=film)

    return film


# ============================
# IMPORTACIÓN MASIVA /popular
# ============================

def fetch_popular_movies(page=1):
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "es-ES",
        "page": page,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def import_popular_movies(max_pages=10):
    for page in range(1, max_pages + 1):
        print(f"IMPORTANDO PÁGINA {page}...")
        data = fetch_popular_movies(page)
        results = data.get("results", [])
        for item in results:
            tmdb_id = item["id"]
            film = import_movie_from_tmdb(tmdb_id)
            print(f"  OK -> {film.title}")
