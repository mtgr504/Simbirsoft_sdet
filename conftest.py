import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    chrome_driver = webdriver.Chrome(options=options)

    yield chrome_driver

    # Закрыть алерт если он открыт перед скриншотом
    try:
        alert = chrome_driver.switch_to.alert
        alert.accept()
    except Exception:
        pass

    try:
        allure.attach(
            chrome_driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass

    chrome_driver.quit()