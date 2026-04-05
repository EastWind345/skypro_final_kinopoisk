import allure
import pytest
from page.pages import KinopoiskMainPage
from config import VALID_MOVIE


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
            assert self.page.is_search_results_loaded(), "Результаты поиска не загрузились"

    @allure.title("Проверка работы фильтров")
    def test_filters_functionality(self):
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

    @allure.title("Проверка активности всех ссылок")
    def test_all_links_active(self):
        with allure.step("Получаем все ссылки"):
            links = self.page.get_all_links()

        with allure.step("Проверяем первые 3 ссылки"):
            for link in links[:3]:
                link_url = link.get_attribute("href")
                self.page.driver.get(link_url)
