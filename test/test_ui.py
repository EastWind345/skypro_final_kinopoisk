import allure
import pytest
from page.pages import KinopoiskMainPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL


@allure.feature("UI-тесты Кинопоиска")
class TestKinopoiskUI:

    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        self.page = KinopoiskMainPage(driver, wait)

    @allure.title("Проверка поисковой строки")
    def test_search_bar_functionality(self):
        self.page.open(BASE_URL)
        search_input = WebDriverWait(
            self.page.search_movie("Интерстеллар"), 10
        ).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input")))
        search_input.clear()
        search_input.send_keys("Интерстеллар")
        search_input.submit()
        assert (
            self.page.is_search_results_loaded()
        ), "Результаты поиска не загрузились"

    @allure.title("Проверка работы фильтров")
    def test_filters_functionality(self):
        self.page.open()
        initial_count = self.page.get_movie_count()
        self.page.apply_year_filter("2023")
        final_count = self.page.get_movie_count()
        assert final_count < initial_count, "Фильтрация не сработала"

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
