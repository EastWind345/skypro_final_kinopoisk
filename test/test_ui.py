import allure
import pytest
from page.pages import KinopoiskMainPage
from config import BASE_URL


@allure.feature("UI-тесты Кинопоиска")
@pytest.mark.ui
class TestKinopoiskUI:

    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        self.page = KinopoiskMainPage(driver, wait)

    @allure.title("Проверка поисковой строки")
    def test_search_original(self):
        film = "Начало"
        self.page.open(BASE_URL)
        self.page.search_movie(film)
        print(self.page.get_text_first())
        assert film in self.page.get_text_first()

    @allure.title("Проверка поисковой строки")
    def test_search_english(self):
        film = "Up"
        self.page.open(BASE_URL)
        self.page.search_movie(film)
        print(self.page.get_text_first())
        assert film in self.page.get_text_first()

    @allure.title("Проверка поисковой строки")
    def test_search_number(self):
        film = "1948"
        self.page.open(BASE_URL)
        self.page.search_movie(film)
        print(self.page.get_text_first())
        assert film in self.page.get_text_first()

    @allure.title("Проверка поисковой строки")
    def test_search_perevod(self):
        film = "집"
        res = "дом"
        self.page.open(BASE_URL)
        self.page.search_movie(film)
        print(self.page.get_text_first())
        assert res in self.page.get_text_first()

    @allure.title("Проверка поисковой строки")
    def test_search_error(self):
        film = "йцукен123"
        error_text = "К сожалению, по вашему запросу ничего не найдено..."
        self.page.open(BASE_URL)
        self.page.search_movie(film)
        print(self.page.get_error())
        assert error_text in self.page.get_error()
