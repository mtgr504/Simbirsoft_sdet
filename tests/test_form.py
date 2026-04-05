import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.form_page import FormPage


VALID_DATA = {
    "name": "Test User",
    "password": "Test1234",
    "color": "Yellow",
    "email": "testuser@example.com",
    "message": "5 Katalon Studio",
}


@allure.feature("Form Fields")
@allure.story("Успешная отправка формы")
@allure.title("TC-001: Заполнение формы валидными данными и проверка алерта")
@allure.severity(allure.severity_level.CRITICAL)
def test_form_submit_positive(driver):
    page = FormPage(driver)

    alert_text = (
        page.open()
            .enter_name(VALID_DATA["name"])
            .enter_password(VALID_DATA["password"])
            .select_drink_milk()
            .select_drink_coffee()
            .select_color(VALID_DATA["color"])
            .select_automation_yes()
            .enter_email(VALID_DATA["email"])
            .enter_message(VALID_DATA["message"])
            .click_submit()
            .get_alert_text()
    )

    assert alert_text == "Message received!", (
        f"Ожидался алерт 'Message received!', получено: '{alert_text}'"
    )


@allure.feature("Form Fields")
@allure.story("Отправка формы с пустым обязательным полем")
@allure.title("TC-002: Форма без имени — алерт не должен появиться")
@allure.severity(allure.severity_level.NORMAL)
def test_form_invalid_email(driver):
    """
    Негативный тест: не заполняем обязательное поле Name.
    Ожидаем что форма не отправится и алерт не появится.
    """
    from selenium.common.exceptions import TimeoutException

    page = FormPage(driver)

    page.open()
    # Name намеренно не заполняем — оно обязательное (required)
    page.enter_email(VALID_DATA["email"])
    page.enter_message(VALID_DATA["message"])
    page.click_submit()

    # Проверяем что алерт НЕ появился
    alert_appeared = True
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
    except TimeoutException:
        alert_appeared = False

    assert not alert_appeared, "Алерт не должен появляться без заполнения поля Name"