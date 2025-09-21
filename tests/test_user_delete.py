import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Check delete cases')
class TestUserDelete(BaseCase):
    @allure.description('This test for check that first users cant delete accounts')
    def test_delete_user_negative_first_users(self):
        with allure.step('Login user for delete:'):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response1 = MyRequests.post('/user/login', data=data)

            auth_sid = self.get_cookie(response1, 'auth_sid')
            token = self.get_header(response1, 'x-csrf-token')

        response2 = MyRequests.delete('/user/2', headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.json()['error'] == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'

    @allure.description('This test successfully delete just created user from his auth')
    def test_delete_user_just_created(self):
        # REGISTER
        with allure.step('Register new user:'):

            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        # LOGIN
        with allure.step('Login new user with auth:'):

            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        with allure.step('Delete user with auth:'):

            response3 = MyRequests.delete(
                f'/user/{user_id}',
                headers={'x-csrf-token': token},
                cookies={'auth_sid': auth_sid},
            )

            Assertions.assert_code_status(response3, 200)

        # GET

        with allure.step('Check that user deleted:'):

            response4 = MyRequests.get(
                f'/user/{user_id}',
                headers={'x-csrf-token': token},
                cookies={'auth_sid': auth_sid},
            )

            Assertions.assert_code_status(response4, 404)

    @allure.description('This test check undelete just created user from another user')
    def test_delete_user_just_created_from_another_user(self):
        # REGISTER
        with allure.step('Register new user:'):

            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            user_id = self.get_json_value(response1, 'id')

        # LOGIN
        with allure.step('Login from another user:'):

            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response2 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        # DELETE

        with allure.step('Check undelete new user from another user account:'):

            response3 = MyRequests.delete(
                f'/user/{user_id}',
                headers={'x-csrf-token': token},
                cookies={'auth_sid': auth_sid},
            )

            Assertions.assert_code_status(response3, 400)
