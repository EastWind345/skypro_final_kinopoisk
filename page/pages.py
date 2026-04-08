from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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

    def search_movie(self, movie_title):
        """Выполняет поиск фильма."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(movie_title)
        search_input.submit()

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
