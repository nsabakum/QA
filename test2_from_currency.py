from steps_lib import *
#import os

#file_dir = os.path.dirname(os.path.realpath(__file__))
#params_list = read_csv_data(file_dir + os.sep + 'converter.csv')
params_list = read_csv_data('currencies.csv') #считываем данные из файла CSV

@pytest.fixture(scope="function", params = params_list)
def param_test(request):
    return request.param

@pytest.allure.feature('CRUD-тест: выбор валюты')
@pytest.allure.story('Выбор валюты, из которой конвертируем, проверка списка')
def test_from_currency(param_test):
    input, expected_output = param_test
    result = from_currency_func(input)
    with pytest.allure.step('Проверка результата'):
        assert result == input, 'Не удалось выбрать нужную валюту'
        print("input: {0}, output: {1}, expected output: {2}".format(input, result, expected_output))

