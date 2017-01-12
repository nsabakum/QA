from steps_lib import *
#import os

#file_dir = os.path.dirname(os.path.realpath(__file__))
#params_list = read_csv_data(file_dir + os.sep + 'converter.csv')
params_list = read_csv_data('converter.csv')

@pytest.fixture(scope="function", params = params_list)

def param_test(request):
    return request.param

@pytest.allure.feature('CRUD-тест: поле ввода суммы')
@pytest.allure.story('Ввод различных параметров и проверка результата')
def test_converter(param_test):
    input, expected_output = param_test
    result = converter_func(input)
    with pytest.allure.step('Проверка результата'):
        assert result == expected_output, 'Результат не совпадает с ожидаемым'
        print("input: {0}, output: {1}, expected: {2}".format(input, result, expected_output))
        
