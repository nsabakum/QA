from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pytest, allure, time, csv

driver = webdriver.Firefox()

#Открыть браузер, загрузить страницу
def setup_module(module):
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

#Получить варианты входных данных и ожид. результатов из файла CSV
def read_csv_data():
    params_list = []
    with open('converter.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            params_list.append(row)
    return params_list

params_list = read_csv_data() #считываем данные из файла CSV

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
        assert driver.find_element_by_xpath("//div[@class='converter-result' and @data-reactid='.0.$1.$1']"), 'Блок с результатом не появился'
        time.sleep(1)
        text = find_and_get_text("//span[@data-reactid='.0.$1.$1.1.0']") #считываем сумму из результата
        result_text = text[:-3] + '.' + text[-2:] #заменяем запятую на точку в результате для сравнения с введенным значением
        return result_text

@pytest.fixture(scope="function", params = params_list)
def param_test(request):
    return request.param

@allure.feature('Калькулятор иностранных валют. CRUD-тест: поле ввода суммы')
@allure.story('Ввод различных параметров и проверка результата')
def test_converter(param_test):
    input, expected_output = param_test
    result = converter_func(input)
    with pytest.allure.step('Проверка результата'):
        assert result == expected_output, 'Результат не совпадает с ожидаемым'
        print("input: {0}, output: {1}, expected: {2}".format(input, result, expected_output))
