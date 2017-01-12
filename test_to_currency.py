from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pytest, allure, time, csv

driver = webdriver.Firefox()

#Запустить браузер и загрузить страницу
def setup_module(module):
    driver.maximize_window()
    driver.get('http://www.sberbank.ru/ru/quotes/converter') 
    with pytest.allure.step('Загрузка страницы'):
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

#Получить варианты входных параметров и ожид. результатов из файла CSV
def read_csv_data():
    params_list = []
    with open('currencies.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            params_list.append(row)
    return params_list
        
params_list = read_csv_data() #считываем данные из файла CSV

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

@pytest.fixture(scope="function", params = params_list)
def param_test(request):
    return request.param

@allure.feature('Калькулятор иностранных валют. CRUD-тест: выбор валюты')
@allure.story('Выбор валюты, в которую конвертируем, проверка списка')
def test_to_currency(param_test):
    input, expected_output = param_test
    result = to_currency_func(input)
    with pytest.allure.step('Проверка результата'):
        assert result == input, 'Не удалось выбрать нужную валюту'
        print("input: {0}, output: {1}, expected output: {2}".format(input, result, expected_output))
