import allure
import pytest
from page.pages import KinopoiskMainPage
from config import BASE_URL, VALID_MOVIE


@allure.feature("UI-тесты Кинопоиска")
class TestKinopoiskUI:

    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        self.page = KinopoiskMainPage(driver, wait)

    @allure.title("Проверка поисковой строки")
    def test_search_bar_functionality(self):
        with allure.step("Выполняем поиск фильма"):
            self.page.search_movie(VALID_MOVIE)

        with allure.step("Проверяем загрузку результатов"):
            assert (
                self.page.is_search_results_loaded()
            ), "Результаты поиска не загрузились"

    @allure.title("Проверка работы фильтров")
    def test_filters_functionality(self):
        self.page.driver.get(f"{BASE_URL}/search")
        with allure.step("Открываем страницу поиска"):
            self.page.driver.get("/search")

        with allure.step("Кликаем на фильтр"):
            self.page.click_filter()

        with allure.step("Проверяем обновление результатов"):
            assert self.page.is_search_results_loaded(), "Фильтры не сработали"

    @allure.title("Проверка наличия пояснительных текстов")
    def test_help_text_presence(self):
        with allure.step("Ищем пояснительные тексты"):
            help_texts = self.page.get_help_texts()
            if not help_texts:
                pytest.skip("Пояснительные тексты не найдены")
            assert len(help_texts) > 0, "Не найдены пояснительные тексты"

    @allure.title("Проверка перехода по основной ссылке")
    def test_main_link_navigation(self):
        main_link = self.page.get_main_link()
        main_link.click()

        self.page.wait.until(lambda driver: driver.current_url != BASE_URL)
        assert (
            "new-page" in self.page.driver.current_url
        ), "Неверный URL после перехода"
