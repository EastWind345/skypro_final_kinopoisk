import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL


@pytest.fixture(scope="session")
def driver():
    """Фикстура для драйвера."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    """Фикстура для ожидания."""
    return WebDriverWait(driver, 30)


@pytest.fixture(autouse=True)
def setup_teardown(driver):
    """Автоматически выполняется перед каждым тестом."""
    driver.get(BASE_URL)
    yield
