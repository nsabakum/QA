import time

from selenium import webdriver
import pytest
import allure

#Открыть браузер, загрузить страницу
def setup_module(module):
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('http://www.sberbank.ru/ru/quotes/converter')
    with allure.step('Загрузка страницы'):
        assert 'Калькулятор иностранных валют' in driver.title, 'Страница не загрузилась'
        driver.implicitly_wait(15)

#Закрыть браузер
def teardown_module(module):
    driver.quit()

#Считать текст элемента
def find_and_get_text(xpath):
    return driver.find_element_by_xpath(xpath).text

#Найти элемент и кликнуть по нему
def find_and_click(xpath):
    var_click = driver.find_element_by_xpath(xpath)
    var_click.click()

#Найти элемент и очистить поле от текста
def find_and_clear(xpath):
    var_field = driver.find_element_by_xpath(xpath)
    var_field.clear()

#Найти элемент и ввести данные
def find_and_input(xpath, keys):
    var_input = driver.find_element_by_xpath(xpath)
    var_input.send_keys(keys)

#Ввод суммы и конвертация
def converter_func(data):
    with pytest.allure.step('Ввод новых данных в поле "Сумма"'):
        find_and_click("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']") #находим и кликаем поле для ввода суммы
        assert 'Не удалось выделить поле для ввода суммы'
        find_and_clear("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']") #очищаем поле для ввода суммы
        assert 'Не удалось очистить поле для ввода суммы'
        find_and_input("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']", data) #вводим данные
        assert 'Не удалось ввести данные'
        
        with pytest.allure.step('Вывод результата'):
            find_and_click("//button[@data-reactid='.0.$1.$0.6.0']") #кликаем по кнопке "Показать"
            assert 'Не удалось нажать кнопку "Показать"'
            assert driver.find_element_by_xpath("//div[@class='converter-result']"), 'Блок с результатом не найден'
            time.sleep(1)
            text = find_and_get_text("//span[@data-reactid='.0.$1.$1.1.0']") #считываем сумму из результата
            result_text = text[:-3] + '.' + text[-2:] #заменяем запятую на точку в результате для сравнения с введенным значением
            return result_text

#Проверить список валют "из"
def from_currency_func(data):
    xpath1 = "//div[@data-reactid='.0.$1.$0.0.2.1']"
    xpath2 = "//div[@data-reactid='.0.$1.$0.0.2.1']//div[@class='visible']"
    xpath3 = "//div[@data-reactid='.0.$1.$0.0.2.1']//div[@class='visible']/*[contains(text()," + " '" + data + "'" + ")]"
    find_and_click(xpath1) #находим и кликаем список валюты
    with pytest.allure.step('Выбор валюты из списка'):
        driver.find_element_by_xpath(xpath2) #находим список валют
        find_and_click(xpath3) #находим валюту в списке и выбираем ее
        return find_and_get_text(xpath1) 

#Проверить список валют "в"
def to_currency_func(data):
    xpath1 = "//div[@data-reactid='.0.$1.$0.0.3.1']"
    xpath2 = "//div[@data-reactid='.0.$1.$0.0.3.1']//div[@class='visible']"
    xpath3 = "//div[@data-reactid='.0.$1.$0.0.3.1']//div[@class='visible']/*[contains(text()," + " '" + data + "'" + ")]"
    find_and_click(xpath1) #находим и кликаем список валюты
    with pytest.allure.step('Выбор валюты из списка'):
        driver.find_element_by_xpath(xpath2) #находим список валют
        find_and_click(xpath3) #находим валюту в списке и выбираем ее
        return find_and_get_text(xpath1) 
