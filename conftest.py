import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


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
