from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class KinopoiskMainPage:
    """Page Object для главной страницы Кинопоиска."""

    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='kp_query']")
    FILTER_ITEM = (By.CSS_SELECTOR, ".filter-item, .filter-link")
    HELP_TEXT = (
        By.XPATH,
        "//*[contains(text(), 'помощь') or contains(text(), 'подсказка')]",
    )
    ALL_LINKS = (By.TAG_NAME, "a")
    SEARCH_RESULTS = (
        By.XPATH,
        "//p[@class='header' and contains(text(), 'Скорее всего, вы ищете')]",
    )

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, url: str) -> None:
        """Открыть страницу по указанному URL"""
        self.driver.get(url)

    def search_movie(self, movie_title):
        """Выполняет поиск фильма."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(movie_title)
        search_input.submit()

    def get_text_first(self):
        first = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="element most_wanted"]')
            )
        )
        return first.text

    def get_error(self):
        first = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="block_left_pad"]')
            )
        )
        return first.text

    def search_movie_name(self, movie_title: str) -> None:
        """Выполнить поиск фильма по названию"""
        search_input = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.clear()
        search_input.send_keys(movie_title)
        search_input.submit()

    def is_search_results_loaded(self) -> bool:
        """Проверить, загрузились ли результаты поиска"""
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".search-result-item")
                )
            )
            return True
        except TimeoutException:
            return False

    def click_filter(self):
        """Кликает на первый доступный фильтр."""
        filterbtn = self.wait.until(
            EC.element_to_be_clickable(self.FILTER_ITEM)
        )
        filterbtn.click()

    def get_help_texts(self):
        """Получает все пояснительные тексты."""
        return self.driver.find_elements(*self.HELP_TEXT)

    def get_all_links(self):
        """Получает все активные ссылки."""
        links = self.driver.find_elements(*self.ALL_LINKS)
        return [link for link in links if link.get_attribute("href")]

    def are_search_results_present(self):
        """Проверяет, что результаты поиска загружены."""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.SEARCH_RESULTS)
            )
            return True
        except:
            return False

    def get_main_link(self) -> WebElement:
        """Возвращает элемент — главную ссылку (например, логотип Кинопоиска).
        :return: WebElement — элемент ссылки"""
        try:
            main_link = self.driver.find_element(
                By.CSS_SELECTOR, ".header__logo a"
            )
            return main_link
        except NoSuchElementException:
            raise Exception("Главная ссылка (логотип) не найдена на странице")

    def apply_year_filter(self, year: str) -> None:
        """Применить фильтр по году (ввод в поле)"""
        year_input = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".year-filter-input"))
        )
        year_input.clear()
        year_input.send_keys(year)

        apply_btn = self.driver.find_element(
            By.CSS_SELECTOR, ".apply-filters-btn"
        )
        apply_btn.click()

    def get_movie_count(self) -> int:
        """Получить количество фильмов в результатах"""
        movies = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".movie-item")
            )
        )
        return len(movies)
