import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait#импорт ожидания для негатива
from selenium.webdriver.support import expected_conditions as EC#усл ожидание набор
from selenium.common.exceptions import TimeoutException #исключение когда элемент не появляется, тож для негатива
from pages.form_page import FormPage #импорт действия


VALID_DATA = {
    "name": "Test User",
    "password": "Test1234",
    "color": "Yellow",
    "email": "testuser@example.com",
    "message": "5 Katalon Studio",# всего 5 инструментов, самый длинный этот
}


@allure.feature("Form Fields")#группировка текста в отчетике
@allure.story("Успешная отправка формы")#подгруппа, что б было видно к какой истории относиться тест
@allure.title("TC-001: Заполнение формы валидными данными и проверка алерта")#название теста для красоты
@allure.severity(allure.severity_level.CRITICAL)#уровень критичности что б не падал
def test_form_submit_positive(driver):#позитив
    page = FormPage(driver)#создание обьекта страницы и передача драйвера

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
    )#то что вводим сохраняем

    assert alert_text == "Message received!", (
        f"Ожидался алерт 'Message received!', получено: '{alert_text}'"
    )#проверяем тест, это надо что б видеть ошибку


@allure.feature("Form Fields")
@allure.story("Отправка формы с пустым обязательным полем")
@allure.title("TC-002: Форма без имени — алерт не должен появиться")
@allure.severity(allure.severity_level.NORMAL)#тож самое ток для негатива
def test_form_invalid_email(driver):
    #в негативном тесте не будет заполняться поле имени, хотя оно обязательное
    #ждем что форма не отправится и алерт не появится

    from selenium.common.exceptions import TimeoutException#еще раз импортируем, пару раз не сработал

    page = FormPage(driver)#как и в позитиве обьект стр

    page.open()#открываем
    page.enter_email(VALID_DATA["email"])
    page.enter_message(VALID_DATA["message"])
    page.click_submit()#заполняем ток почту и пароль, ждем что не сработает отправка

    #проверяем что алерт не появился
    alert_appeared = True
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
    except TimeoutException:
        alert_appeared = False

    assert not alert_appeared, "Алерт не должен появляться без заполнения поля Name"