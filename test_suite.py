from steps_lib import *
from test0_converter import *
from test1_end_to_end import *
from test2_from_currency import *
from test3_to_currency import *

@pytest.allure.feature('Калькулятор иностранных валют')
@pytest.allure.story('CRUD, end-to-end функциональные тесты')
class TestSuite:
    #Тестируем поле для ввода суммы
    def test0_converter(self, data):
        pass

    #Тестируем end-to-end сценарий
    def test1_end_to_end(self):
        pass

    #Тестируем выпадающий список валют (из)
    def test2_from_currency(self):
        pass

    #Тестируем выпадающий список валют (в)
    def test3_to_currency(self):
        pass
