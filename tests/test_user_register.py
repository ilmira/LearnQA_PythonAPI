import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('Registration cases')
class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f'Unexpected content: {response.content}'

    def test_create_user_with_wrong_email(self):
        data = self.prepare_registration_data()
        data['email'] = 'vinkotovexample.com'

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == 'Invalid email format'

    data_for_test_without_one_field = (({'password': '123',
                                         'username': 'learnqa',
                                         'firstName': 'learnqa',
                                         'lastName': 'learnqa'}, 'email'), ({'password': '123',
                                                                             'username': 'learnqa',
                                                                             'firstName': 'learnqa',
                                                                             'email': 'test@email.com'}, 'lastName'),
                                       ({'password': '123',
                                         'username': 'learnqa',
                                         'lastName': 'learnqa',
                                         'email': 'test@email.com'}, 'firstName'), ({'password': '123',
                                                                                     'firstName': 'learnqa',
                                                                                     'lastName': 'learnqa',
                                                                                     'email': 'test@email.com'},
                                                                                    'username'),
                                       ({'username': 'learnqa',
                                         'firstName': 'learnqa',
                                         'lastName': 'learnqa',
                                         'email': 'test@email.com'}, 'password')
                                       )

    @pytest.mark.parametrize('data, field_name', data_for_test_without_one_field)
    def test_create_user_without_one_field(self, data, field_name):
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'The following required params are missed: {field_name}'

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'I'

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == "The value of 'firstName' field is too short"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 252 * 'i'

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == "The value of 'firstName' field is too long"
