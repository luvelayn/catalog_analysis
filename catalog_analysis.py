import math
from collections.abc import Iterator

movies = [
    {
        "title": "The Dune Chronicles",
        "year": 2021,
        "genres": {"sci-fi", "drama"},
        "rating": 8.6,
        "duration_min": 155,
        "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"],
    },
    {
        "title": "Kitchen Stories",
        "year": 2019,
        "genres": {"comedy", "drama"},
        "rating": 7.1,
        "duration_min": 98,
        "actors": ["A. Novak", "M. Ferguson"],
    },
    {
        "title": "silent hours",
        "year": 2016,
        "genres": {"thriller", "drama"},
        "rating": 6.4,
        "duration_min": 112,
        "actors": ["J. Bloom", "K. Lee"],
    },
    {
        "title": "Comet Racers",
        "year": 2023,
        "genres": {"sci-fi", "action"},
        "rating": 5.9,
        "duration_min": 101,
        "actors": ["O. Isaac", "P. Diaz"],
    },
    {
        "title": "The Last Bakery",
        "year": 2014,
        "genres": {"comedy"},
        "rating": 7.8,
        "duration_min": 89,
        "actors": ["A. Novak", "T. Chalamet"],
    },
    {
        "title": "midnight in oslo",
        "year": 2020,
        "genres": {"thriller", "mystery"},
        "rating": 8.9,
        "duration_min": 124,
        "actors": ["K. Lee", "R. Ferguson"],
    },
    {
        "title": "Garden of Static",
        "year": 2022,
        "genres": {"drama"},
        "rating": 4.8,
        "duration_min": 137,
        "actors": ["P. Diaz", "J. Bloom"],
    },
    {
        "title": "The Quiet Algorithm",
        "year": 2024,
        "genres": {"sci-fi", "drama"},
        "rating": 9.2,
        "duration_min": 118,
        "actors": ["M. Ferguson", "O. Isaac"],
    },
    {
        "title": "Two Left Shoes",
        "year": 2011,
        "genres": {"comedy"},
        "rating": 6.0,
        "duration_min": 95,
        "actors": ["A. Novak", "K. Lee"],
    },
    {
        "title": "Red Harbor",
        "year": 2018,
        "genres": {"action", "thriller"},
        "rating": 7.3,
        "duration_min": 129,
        "actors": ["P. Diaz", "T. Chalamet"],
    },
]


def _ensure_not_empty(movies: list[dict]) -> None:
    if not movies:
        raise ValueError("Каталог фильмов пуст")


def average_rating(movies: list[dict]) -> float:
    _ensure_not_empty(movies)
    total_rating = sum(movie["rating"] for movie in movies)
    return round(total_rating / len(movies), 1)


def catalog_age_stats(
    movies: list[dict], current_year: int = 2026
) -> tuple[int, int, int]:
    _ensure_not_empty(movies)
    ages = [current_year - movie["year"] for movie in movies]
    return max(ages), min(ages), math.ceil(sum(ages) / len(ages))


def duration_in_hours(minutes: int) -> str:
    return f"{minutes // 60}ч {minutes % 60}м"


def rating_tier(rating: float) -> str:
    if rating >= 7:
        return "шедевр" if rating >= 9 else "хорошо"
    elif rating >= 5:
        return "средне"
    else:
        return "слабо"


def decade_label(year: int) -> str:
    match year:
        case _ if year > 2020:
            return "новые"
        case _ if 2015 <= year <= 2020:
            return "недавние"
        case _ if year < 2015:
            return "старые"


def print_non_comedies(movies: list[dict]) -> None:
    for movie in movies:
        if "comedy" in movie["genres"]:
            continue
        print("•", normalize_title(movie["title"]))


def print_first_masterpiece(movies: list[dict], threshold: float = 9.0) -> None:
    i = 0
    while i < len(movies):
        if movies[i]["rating"] > threshold:
            print("•", normalize_title(movies[i]["title"]))
            break
        i += 1
    else:
        print("Шедевров не найдено")


def count_long_movies(movies: list[dict], threshold: int = 120) -> int:
    count = 0
    for movie in movies:
        if movie["duration_min"] > threshold:
            count += 1
    return count


def normalize_title(title: str) -> str:
    return " ".join(word[0].upper() + word[1:] for word in title.split())


def make_slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def format_report_line(movie: dict) -> str:
    title = normalize_title(movie["title"])
    duration = duration_in_hours(movie["duration_min"])
    genres = ", ".join(sorted(movie["genres"]))

    return (
        f'"{title}" ({movie["year"]}) — '
        f"{movie['rating']}/10, {duration}, жанры: {genres}"
    )


def sort_by_rating(movies: list[dict]) -> list[dict]:
    return sorted(movies, key=lambda movie: movie["rating"], reverse=True)


def titles_sorted_by_rating(movies: list[dict]) -> list[str]:
    return [movie["title"] for movie in sort_by_rating(movies)]


def top_n_by_rating(movies: list[dict], n: int = 3) -> list[tuple[str, float]]:
    return [(movie["title"], movie["rating"]) for movie in sort_by_rating(movies)[:n]]


def count_by_genre(movies: list[dict]) -> dict[str, int]:
    genres_dict = {}
    for movie in movies:
        for genre in movie["genres"]:
            genres_dict[genre] = genres_dict.get(genre, 0) + 1
    return genres_dict


def actor_filmography(movies: list[dict]) -> dict[str, list[str]]:
    actors_dict = {}
    for movie in movies:
        for actor in movie["actors"]:
            actors_dict.setdefault(actor, []).append(movie["title"])
    return actors_dict


def above_average(movies: list[dict]) -> dict[str, float]:
    avg_rating = average_rating(movies)
    return {
        movie["title"]: movie["rating"]
        for movie in movies
        if movie["rating"] > avg_rating
    }


def all_genres(movies: list[dict]) -> set[str]:
    genres = set()
    for movie in movies:
        genres.update(movie["genres"])
    return genres


def common_actors(movie1: dict, movie2: dict) -> set[str]:
    return set(movie1["actors"]) & set(movie2["actors"])


def genres_only_in_one(movies_a: list[dict], movies_b: list[dict]) -> set[str]:
    return all_genres(movies_a) - all_genres(movies_b)


def iter_high_rated(movies: list[dict], min_rating: float = 8.0) -> Iterator[dict]:
    for movie in movies:
        if movie["rating"] >= min_rating:
            yield movie


def build_report(movies: list[dict]) -> None:
    age_stats = catalog_age_stats(movies)
    top_3 = top_n_by_rating(movies)
    movies_by_title = {movie["title"]: movie for movie in movies}
    genre_stats = count_by_genre(movies)
    genre_stats_keys = sorted(genre_stats, key=lambda g: (-genre_stats[g], g))

    print("ОТЧЕТ ПО КАТАЛОГУ")
    print("Средний рейтинг:", average_rating(movies))
    print(f"Средний возраст фильмов: {age_stats[-1]} лет")
    print("\nТоп-3 фильма:")
    for title, _ in top_3:
        print("\u2022", format_report_line(movies_by_title[title]))
    print("\nКоличество фильмов по жанрам:")
    for key in genre_stats_keys:
        print(f"\u2022 {key} — {genre_stats.get(key)}")
    print("\nВсе жанры каталога:", ", ".join(sorted(all_genres(movies))))


def main() -> None:
    print("Все фильмы кроме комедий:")
    print_non_comedies(movies)

    print("\nФильмы с рейтингом выше 9.0:")
    print_first_masterpiece(movies)
    print("\nФильмы с рейтингом выше 9.5:")
    print_first_masterpiece(movies, threshold=9.5)

    print("\nФильмы с рейтингом выше среднего:")
    print(above_average(movies))

    print("\nФильмы с рейтингом не ниже 8.0:")
    for movie in iter_high_rated(movies):
        print("\u2022", format_report_line(movie))

    sum_duration = sum(movie["duration_min"] for movie in movies if movie["rating"] > 7)
    print("\nСуммарная длительность фильмов с рейтингом выше 7.0:", sum_duration)

    print()

    build_report(movies)


if __name__ == "__main__":
    main()
