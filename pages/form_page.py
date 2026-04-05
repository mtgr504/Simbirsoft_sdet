import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class FormPage:
    URL = "https://practice-automation.com/form-fields/"

    # ID-селекторы
    _NAME_INPUT = (By.ID, "name-input")
    _EMAIL_INPUT = (By.ID, "email")
    _SUBMIT_BUTTON = (By.ID, "submit-btn")

    # CSS-селекторы
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    _COLOR_YELLOW = (By.CSS_SELECTOR, "input[value='Yellow']")

    # XPath-селекторы
    _DRINK_MILK = (By.XPATH, "//input[@value='Milk']")
    _DRINK_COFFEE = (By.XPATH, "//input[@value='Coffee']")
    _AUTOMATION_SELECT = (By.XPATH, "//select[@name='automation']")
    _MESSAGE_INPUT = (By.XPATH, "//textarea[@name='message']")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=20)

    def _scroll_to(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    @allure.step("Открыть страницу формы")
    def open(self) -> "FormPage":
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self._NAME_INPUT))
        return self

    @allure.step("Заполнить поле Name")
    def enter_name(self, name: str) -> "FormPage":
        field = self.wait.until(EC.element_to_be_clickable(self._NAME_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(name)
        return self

    @allure.step("Заполнить поле Password")
    def enter_password(self, password: str) -> "FormPage":
        field = self.wait.until(EC.element_to_be_clickable(self._PASSWORD_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(password)
        return self

    @allure.step("Выбрать напиток Milk")
    def select_drink_milk(self) -> "FormPage":
        cb = self.wait.until(EC.presence_of_element_located(self._DRINK_MILK))
        self._scroll_to(cb)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)
        return self

    @allure.step("Выбрать напиток Coffee")
    def select_drink_coffee(self) -> "FormPage":
        cb = self.wait.until(EC.presence_of_element_located(self._DRINK_COFFEE))
        self._scroll_to(cb)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)
        return self

    @allure.step("Выбрать цвет Yellow")
    def select_color(self, color: str) -> "FormPage":
        rb = self.wait.until(EC.presence_of_element_located(self._COLOR_YELLOW))
        self._scroll_to(rb)
        if not rb.is_selected():
            self.driver.execute_script("arguments[0].click();", rb)
        return self

    @allure.step("Выбрать Yes в поле automation")
    def select_automation_yes(self) -> "FormPage":
        el = self.wait.until(EC.element_to_be_clickable(self._AUTOMATION_SELECT))
        self._scroll_to(el)
        Select(el).select_by_visible_text("Yes")
        return self

    @allure.step("Заполнить поле Email")
    def enter_email(self, email: str) -> "FormPage":
        field = self.wait.until(EC.element_to_be_clickable(self._EMAIL_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(email)
        return self

    @allure.step("Заполнить поле Message")
    def enter_message(self, message: str) -> "FormPage":
        field = self.wait.until(EC.element_to_be_clickable(self._MESSAGE_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(message)
        return self

    @allure.step("Нажать Submit")
    def click_submit(self) -> "FormPage":
        btn = self.wait.until(EC.presence_of_element_located(self._SUBMIT_BUTTON))
        self._scroll_to(btn)
        self.driver.execute_script("arguments[0].click();", btn)
        return self

    @allure.step("Получить текст алерта")
    def get_alert_text(self) -> str:
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text