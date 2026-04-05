import requests
from config import API_URL, AUTH_TOKEN


class ApiHelper:
    """Вспомогательные методы для API‑тестов."""

    @staticmethod
    def search_movie(title: str) -> dict:
        """Ищет фильм по названию."""
        response = requests.get(
            f"{API_URL}/search",
            params={"query": title}
        )
        return response.json(), response.status_code

    @staticmethod
    def get_movie_reviews(movie_id: int) -> dict:
        """Получает отзывы к фильму."""
        response = requests.get(f"{API_URL}/movies/{movie_id}/reviews")
        return response.json(), response.status_code

    @staticmethod
    def add_to_watchlist(movie_id: int) -> dict:
        """Добавляет фильм в список 'Буду смотреть'."""
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {"movie_id": movie_id, "action": "add"}
        response = requests.post(f"{API_URL
                                    }/watchlist", json=data, headers=headers)
        return response.json(), response.status_code
