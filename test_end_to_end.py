from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pytest, allure, time, csv

driver = webdriver.Firefox()

#Запуск браузера и загрузка страницы
def setup_module(module):
    driver.maximize_window()
    driver.get('http://www.sberbank.ru/ru/quotes/converter') 
    with pytest.allure.step('Загрузка страницы'):
        assert 'Калькулятор иностранных валют' in driver.title, 'Страница не открылась.'
        driver.implicitly_wait(15)

#'Закрыть браузер
def teardown_module(module):
    driver.quit()

#'Считать текст элемента
def find_and_get_text(xpath):
    return driver.find_element_by_xpath(xpath).text

#'Найти элемент и кликнуть по нему    
def find_and_click(xpath):
    var_click = driver.find_element_by_xpath(xpath)
    var_click.click()

#'Найти элемент и очистить поле от текста
def find_and_clear(xpath):
    var_field = driver.find_element_by_xpath(xpath)
    var_field.clear()

#'Найти элемент и ввести данные
def find_and_input(xpath, keys):
    var_input = driver.find_element_by_xpath(xpath)
    var_input.send_keys(keys)

@allure.feature('End-to-end сценарий')
@allure.story('Ввод суммы, выбор некоторых опций, конвертация валюты')
def test_end_to_end():
    with pytest.allure.step('Ввод суммы'):
        find_and_click("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']") #кликаем поле для ввода суммы
        assert 'Не удалось найти и кликнуть в поле ввода суммы'
        find_and_clear("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']") #очищаем поле для ввода суммы
        assert 'Не удалось очистить поле ввода суммы'
        find_and_input("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']", '2450') #вводим сумму
        assert 'Не удалось ввести сумму'
        
    with pytest.allure.step('Выбор опций'):
        find_and_click("//div[@data-reactid='.0.$1.$0.0.2.1']") #выбираем валюту, из которой конвертируем
        assert 'Список валют "из" не открывается'
        find_and_click("//div[@data-reactid='.0.$1.$0.0.2.1']//span[contains(text(), 'EUR')]") #выбираем евро
        assert 'Не удалось выбрать валюту (EUR)'
        find_and_click("//div[@data-reactid='.0.$1.$0.0.3.1']") #выбираем валюту, в которую конвертируем
        assert 'Список валют "в" не открывается'
        find_and_click("//div[@data-reactid='.0.$1.$0.0.3.1']//span[contains(text(), 'GBP')]") #выбираем фунты
        assert 'Не удалось выбрать валюту (GBP)'
        find_and_click("//input[@name='sourceCode']/following-sibling::p[contains(text(), 'Наличные')]") #в блоке "Источник" выбираем "Наличные"
        assert 'Не удалось выбрать "Источник" - "Наличные"'
        find_and_click("//input[@name='destinationCode']/following-sibling::p[contains(text(), 'Выдать наличные')]") #в блоке "Получение" выбираем "Выбрать наличные"
        assert 'Не удалось выбрать "Получение" - "Выбрать наличные"'

    with pytest.allure.step('Вывод результата с помощью кнопки "Показать"'):
        find_and_click("//div[@data-reactid='.0.$1.$0.6']/button[contains(text(), 'Показать')]") #нажимаем "Показать"
        time.sleep(1)
        a = find_and_get_text("//div[@class='converter-result']/h5/span[1]")
        b = find_and_get_text("//div[@class='converter-result']/h5/span[2]")
        c = find_and_get_text("//div[@class='converter-result']/h4/span[2]")
        with pytest.allure.step('Проверка результата'):
            assert a == '2 450,00', 'Неверная сумма'
            assert b == 'EUR', 'Неверная валюта "из"'
            assert c == 'GBP', 'Неверная валюта "в"'
