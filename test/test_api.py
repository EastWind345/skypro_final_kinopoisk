import pytest
import allure
from page.api_helper import ApiHelper
from config import VALID_MOVIE, MOVIE_ID, INVALID_MOVIE


@allure.feature("API-тесты Кинопоиска")
class TestKinopoiskAPI:

    def setup_method(self):
        """Инициализация ApiHelper перед каждым тестом"""
        self.api = ApiHelper()
        self.VALID_MOVIE = "Интерстеллар"
        self.INVALID_MOVIE = "НесуществующийФильм123"
        self.MOVIE_ID = 447301

    @allure.title("Поиск фильма по названию")
    def test_search_movie_by_name(self):
        data, status_code = self.api.search_movie(self.VALID_MOVIE)
        assert status_code == 200
        assert "films" in data
        assert len(data["films"]) > 0

    @allure.title("Получение отзывов о фильме")
    def test_movie_reviews(self):
        data, status_code = self.api.get_movie_reviews(self.MOVIE_ID)
        assert status_code == 200
        assert "reviews" in data or "items" in data

    @allure.title("Добавление фильма в список просмотра")
    def test_add_to_watchlist(self):
        data, status_code = self.api.add_to_watchlist(self.MOVIE_ID)
        assert status_code in [200, 201]

    @allure.title("Поиск по несуществующему названию")
    def test_search_invalid_title(self):
        data, status_code = self.api.search_movie(self.INVALID_MOVIE)
        assert status_code == 200
        assert "films" in data
        assert len(data["films"]) == 0

    @allure.title("Поиск фильма на английском")
    def test_search_english_title(self):
        data, status_code = self.api.search_movie("Interstellar")
        assert status_code == 200
        assert "films" in data
        assert len(data["films"]) > 0
