from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    """
    Page Factory: фабрика для создания экземпляра WebDriver.
    Паттерн Factory изолирует логику создания драйвера.
    """

    @staticmethod
    def get_driver(headless: bool = False) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)