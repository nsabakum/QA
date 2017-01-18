from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest
import allure

class StartEnd:
    #открыть браузер, загрузить страницу
    def setup_class(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        self.driver.get('http://www.sberbank.ru/ru/quotes/converter')
        with pytest.allure.step('Загрузка страницы'):
            assert 'Калькулятор иностранных валют' in self.driver.title, 'Страница не загрузилась'

    #закрыть браузер
    def teardown_class(self):
        self.driver.quit()

class Driver:
    def __init__(self, driver):
        self.driver = driver

class Converter(Driver):
    #найти элемент
    def find(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    #ввод суммы и конвертация
    def converter_func(self, input, output):
        with pytest.allure.step('Ввод новых данных в поле "Сумма"'):
            #находим и кликаем поле для ввода суммы
            summa = self.find("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']")
            summa.click()
            assert 'Не удалось выделить поле для ввода суммы'

            #очищаем поле для ввода суммы
            summa.clear()
            assert 'Не удалось очистить поле для ввода суммы'

            #вводим данные
            summa.send_keys(input) 
            assert 'Не удалось ввести данные'

            with pytest.allure.step('Вывод результата'):
                #кликаем по кнопке "Показать"
                button = self.find("//button[@data-reactid='.0.$1.$0.6.0']")
                button.click()
                assert 'Не удалось нажать кнопку "Показать"'

                #ждем, когда значение в блоке с результатом обновится (совпадения знаков до запятой)
                try:
                    WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//span[@data-reactid='.0.$1.$1.1.0']"), output[:-3]))
                    text = self.find("//span[@data-reactid='.0.$1.$1.1.0']").text
                    
                    #заменяем запятую на точку для сравнения результата
                    text = text[:-3] + '.' + text[-2:]
                    return text
                except TimeoutException:
                    raise Exception('Значение не получено')

    #проверить список валют "из"
    def from_currency_func(self, data):
        xpath1 = "//div[@data-reactid='.0.$1.$0.0.2.1']"
        xpath2 = "//div[@data-reactid='.0.$1.$0.0.2.1']//div[@class='visible']/*[contains(text()," + " '" + data + "'" + ")]"

        #находим и кликаем список валюты
        currency = self.find(xpath1)
        currency.click()
        
        with pytest.allure.step('Выбор валюты из списка'):
            #находим валюту в списке и выбираем ее
            currency_item = self.find(xpath2)
            currency_item.click()
            return currency.text

    # Проверить список валют "в"
    def to_currency_func(self, data):
        xpath1 = "//div[@data-reactid='.0.$1.$0.0.3.1']"
        xpath2 = "//div[@data-reactid='.0.$1.$0.0.3.1']//div[@class='visible']/*[contains(text()," + " '" + data + "'" + ")]"

        #находим и кликаем список валюты
        currency = self.find(xpath1)
        currency.click()
        
        with pytest.allure.step('Выбор валюты из списка'):
            #находим валюту в списке и выбираем ее
            currency_item = self.find(xpath2)
            currency_item.click()
            return currency.text
