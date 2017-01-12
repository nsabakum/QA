from utils.steps_lib import *
from data.testing_data import get_currencies_data

params_list = get_currencies_data()

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
