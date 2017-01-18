import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.steps_lib import StartEnd, Converter

@pytest.allure.feature('End-to-end сценарий')
@pytest.allure.story('Ввод суммы, выбор некоторых опций, конвертация валюты')
class TestEndToEnd(StartEnd):
    def test_end_to_end(self):
        converter = Converter(self.driver)
        with pytest.allure.step('Ввод суммы'):
            #кликаем поле для ввода суммы
            summa = converter.find("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']")
            summa.click()
            assert 'Не удалось найти и кликнуть в поле ввода суммы'

            #очищаем поле для ввода суммы
            summa.clear() 
            assert 'Не удалось очистить поле ввода суммы'

            #вводим сумму
            summa.send_keys('2450') 
            assert 'Не удалось ввести сумму'

        with pytest.allure.step('Выбор опций'):
            #выбираем валюту, из которой конвертируем
            currency = converter.find("//div[@data-reactid='.0.$1.$0.0.2.1']")
            currency.click()
            assert 'Список валют "из" не открывается'

            #выбираем EUR
            eur = converter.find("//div[@data-reactid='.0.$1.$0.0.2.1']//span[contains(text(), 'EUR')]")
            eur.click()            
            assert 'Не удалось выбрать валюту (EUR)'

            #выбираем валюту, в которую конвертируем
            currency = converter.find("//div[@data-reactid='.0.$1.$0.0.3.1']")
            currency.click()
            assert 'Список валют "в" не открывается'

            #выбираем GBP
            gbp = converter.find("//div[@data-reactid='.0.$1.$0.0.3.1']//span[contains(text(), 'GBP')]")
            gbp.click()
            assert 'Не удалось выбрать валюту (GBP)'

            #в блоке "Источник" выбираем "Наличные"
            ist = converter.find("//p[@data-reactid='.0.$1.$0.1.1:$2.2']")
            ist.click()
            assert 'Не удалось выбрать "Источник" - "Наличные"'

            #в блоке "Получение" выбираем "Выбрать наличные"
            recieve = converter.find("//p[@data-reactid='.0.$1.$0.2.1:$2.2']")
            recieve.click()
            assert 'Не удалось выбрать "Получение" - "Выбрать наличные"'

        with pytest.allure.step('Вывод результата с помощью кнопки "Показать"'):
            #нажимаем "Показать"
            button = converter.find("//button[@data-reactid='.0.$1.$0.6.0']")
            button.click()

            #ждем, когда появится блок с результатом
            try:
                WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//span[@data-reactid='.0.$1.$1.1.0']"), '2 450,00'))
            except TimeoutException:
                raise Exception('Значение не получено')

            a = converter.find("//span[@data-reactid='.0.$1.$1.1.1']").text
            b = converter.find("//span[@data-reactid='.0.$1.$1.2.1']").text
            with pytest.allure.step('Проверка результата'):
                assert a == 'EUR', 'Неверная валюта "из"'
                assert b == 'GBP', 'Неверная валюта "в"'

