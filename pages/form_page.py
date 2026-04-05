import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select #select для выпадающих списков
from selenium.webdriver.support import expected_conditions as EC #EC набор для готовых условий ожидания (эл видимый например)
from selenium.webdriver.remote.webdriver import WebDriver #wd нужен для подсказок(type hints)

class FormPage:
    URL = "https://practice-automation.com/form-fields/" #Если менять url, на всякий случай

    # ID-селекторы
    _NAME_INPUT = (By.ID, "name-input")#в коде стр было name-input, не name + приватная переменная класса
    _EMAIL_INPUT = (By.ID, "email")# локатор
    _SUBMIT_BUTTON = (By.ID, "submit-btn")# тоже локатор

    # CSS-селекторы
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")# локатор для пароля уже через css
    _COLOR_YELLOW = (By.CSS_SELECTOR, "input[value='Yellow']")# локатор радио-кнопки тоже через ccs

    # XPath-селекторы
    _DRINK_MILK = (By.XPATH, "//input[@value='Milk']")# //input выбирает любой ввод милк
    _DRINK_COFFEE = (By.XPATH, "//input[@value='Coffee']")# для кофе тоже самое
    _AUTOMATION_SELECT = (By.XPATH, "//select[@name='automation']")# здесь ищет тег select
    _MESSAGE_INPUT = (By.XPATH, "//textarea[@name='message']")# здесь тег textarea

    def __init__(self, driver: WebDriver):
        self.driver = driver#создаем обьект, он принимает драйвер браузера и сохраняет его
        self.wait = WebDriverWait(driver, timeout=20)#обьект ожидания с таймером 20 сек, это минимум которого хватает

    def _scroll_to(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element# метод для прокрутки к none, вспомогательный, что бы ничего не перекрылось
        )

    @allure.step("Открыть страницу формы")
    def open(self) -> "FormPage":# 34 для пометки как шага в allure, открываем стр и возвращаем сам обьект
        self.driver.get(self.URL)# открываем урл
        self.wait.until(EC.presence_of_element_located(self._NAME_INPUT))# ждем поле нэйм
        return self

    @allure.step("Заполнить поле Name")
    def enter_name(self, name: str) -> "FormPage":#заполняем имя
        field = self.wait.until(EC.element_to_be_clickable(self._NAME_INPUT))# когда по полю можно кликнуть сохраняем его
        self._scroll_to(field)# прокрутка стр
        field.clear()# чистим
        field.send_keys(name)# вводим
        return self

    @allure.step("Заполнить поле Password")
    def enter_password(self, password: str) -> "FormPage":# тот же принцип, что и в имени
        field = self.wait.until(EC.element_to_be_clickable(self._PASSWORD_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(password)
        return self

    @allure.step("Выбрать напиток Milk")
    def select_drink_milk(self) -> "FormPage":#
        cb = self.wait.until(EC.presence_of_element_located(self._DRINK_MILK))#ждем появление чекбокса
        self._scroll_to(cb)# прокручиваем к нему
        if not cb.is_selected():# проверяем есть отметка на нем или нет
            self.driver.execute_script("arguments[0].click();", cb)# кликаем через джаву, а то вылезает ошибка
        return self

    @allure.step("Выбрать напиток Coffee")
    def select_drink_coffee(self) -> "FormPage":# тот же самый принцип что и в милк
        cb = self.wait.until(EC.presence_of_element_located(self._DRINK_COFFEE))
        self._scroll_to(cb)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)
        return self

    @allure.step("Выбрать цвет Yellow")
    def select_color(self, color: str) -> "FormPage":# тож самое
        rb = self.wait.until(EC.presence_of_element_located(self._COLOR_YELLOW))
        self._scroll_to(rb)
        if not rb.is_selected():
            self.driver.execute_script("arguments[0].click();", rb)
        return self

    @allure.step("Выбрать Yes в поле automation")
    def select_automation_yes(self) -> "FormPage":
        el = self.wait.until(EC.element_to_be_clickable(self._AUTOMATION_SELECT))# ждем когда можно кликнуть
        self._scroll_to(el)# прокрутка
        Select(el).select_by_visible_text("Yes")# превращаем в селект и выбираем да
        return self

    @allure.step("Заполнить поле Email")
    def enter_email(self, email: str) -> "FormPage":# как и имя
        field = self.wait.until(EC.element_to_be_clickable(self._EMAIL_INPUT))
        self._scroll_to(field)
        field.clear()
        field.send_keys(email)
        return self

    @allure.step("Заполнить поле Message")
    def enter_message(self, message: str) -> "FormPage":# тож самое
        field = self.wait.until(EC.element_to_be_clickable(self._MESSAGE_INPUT))#
        self._scroll_to(field)#
        field.clear()
        field.send_keys(message)#
        return self

    @allure.step("Нажать Submit")
    def click_submit(self) -> "FormPage":
        btn = self.wait.until(EC.presence_of_element_located(self._SUBMIT_BUTTON))# ждем появления  submit
        self._scroll_to(btn)#прокрутка
        self.driver.execute_script("arguments[0].click();", btn)#кликаем через джаву
        return self

    @allure.step("Получить текст алерта")
    def get_alert_text(self) -> str:
        self.wait.until(EC.alert_is_present())# ждем когда появится всплывающее окно
        alert = self.driver.switch_to.alert#переключаем на него управление
        text = alert.text#запись в переменную того что он вывел
        alert.accept()#кликаем ок
        return text