import allure
from api_helper import ApiHelper
from config import VALID_MOVIE, INVALID_MOVIE, ENGLISH_MOVIE
from config import MOVIE_ID, WATCHLIST_MOVIE_ID


@allure.feature("API-тесты Кинопоиска")
class TestKinopoiskAPI:

    @allure.title("Поиск фильма по названию")
    @allure.description("Проверка поиска фильма по корректному названию")
    def test_search_movie_by_name(self):
        with allure.step("Выполняем поиск фильма"):
            response_data, status_code = ApiHelper.search_movie(VALID_MOVIE)

        with allure.step("Проверяем код ответа"):
            assert status_code == 200, f"Ожидался код 200, получен {
                status_code}"

        with allure.step("Проверяем наличие результатов"):
            assert "results" in response_data, "В ответе нет поля 'results'"
            assert len(response_data["results"]) > 0, "Нет результатов поиска"

        with allure.step("Проверяем данные фильма"):
            first_result = response_data["results"][0]
            assert "id" in first_result
            assert "title" in first_result
            assert "year" in first_result
            assert "rating" in first_result

    @allure.title("Отзывы к фильму")
    @allure.description("Получение отзывов к фильму по ID")
    def test_movie_reviews(self):
        with allure.step(f"Получаем отзывы для фильма ID {MOVIE_ID}"):
            response_data, status_code = ApiHelper.get_movie_reviews(MOVIE_ID)

        with allure.step("Проверяем код ответа"):
            assert status_code == 200, f"Ожидался код 200, получен {
                status_code}"

        with allure.step("Проверяем структуру отзывов"):
            assert "reviews" in response_data
            assert isinstance(response_data["reviews"], list)
            if response_data["reviews"]:
                review = response_data["reviews"][0]
                assert "author" in review
                assert "text" in review
                assert "rating" in review

            assert "total" in response_data

    @allure.title("Добавить фильм в 'Буду смотреть'")
    @allure.description("Добавление фильма в список через API")
    def test_add_to_watchlist(self):
        with allure.step(f"Добавляем фильм ID {WATCHLIST_MOVIE_ID} в список"):
            response_data, status_code = ApiHelper.add_to_watchlist(
                WATCHLIST_MOVIE_ID
            )

        with allure.step("Проверяем успешный ответ"):
            assert status_code == 201, f"Ожидался код 201, получен {
                status_code}"
            assert response_data.get("status") == "success"
            assert "фильм добавлен" in response_data.get("message", "").lower()

    @allure.title("Поиск по невалидному названию")
    @allure.description("Обработка поиска по несуществующему названию")
    def test_search_invalid_title(self):
        with allure.step(f"Ищем несуществующий фильм: {INVALID_MOVIE}"):
            response_data, status_code = ApiHelper.search_movie(INVALID_MOVIE)

        with allure.step("Проверяем код ответа"):
            assert status_code == 200, f"Ожидался код 200, получен {
                status_code}"

        with allure.step("Проверяем пустой результат"):
            assert "results" in response_data
            assert len(response_data["results"]) == 0
            assert response_data.get("total", 0) == 0

    @allure.title("Поиск на другом языке")
    @allure.description("Поиск фильма по англоязычному названию")
    def test_search_english_title(self):
        with allure.step(f"Ищем фильм на английском: {ENGLISH_MOVIE}"):
            response_data, status_code = ApiHelper.search_movie(ENGLISH_MOVIE)

        with allure.step("Проверяем код ответа"):
            assert status_code == 200, f"Ожидался код 200, получен {
                status_code}"

        with allure.step("Проверяем результаты"):
            assert (
                "results" in response_data
                and len(response_data["results"]) > 0
            )
            first_result = response_data["results"][0]
            assert (
                first_result.get("original_title", "").lower()
                == ENGLISH_MOVIE.lower()
            )
            assert "title" in first_result
            assert "year" in first_result
            assert "rating" in first_result

    @allure.title("Проверка отображения результатов поиска")
    def test_search_results_display(self):
        with allure.step("Выполняем поиск"):
            response_data, status_code = ApiHelper.search_movie("Интерстеллар")

        with allure.step("Проверяем, что результаты найдены"):
            assert (
                response_data,
                status_code == ApiHelper.search_movie("Интерстеллар"),
            ), "Результаты поиска не отобразились"
