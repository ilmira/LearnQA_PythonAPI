import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response1, 'id')

    def login_current_user(self):
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        self.auth_sid = self.get_cookie(response2, 'auth_sid')
        self.token = self.get_header(response2, 'x-csrf-token')

    def teardown_method(self):
        self.login_current_user()
        MyRequests.delete(f'/user/{self.user_id}', headers={'x-csrf-token': self.token},
                          cookies={'auth_sid': self.auth_sid})

    def test_edit_just_created_user(self):
        # LOGIN

        self.login_current_user()

        # EDIT

        new_name = 'Changed name'

        response3 = MyRequests.put(
            f'/user/{self.user_id}',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(
            f'/user/{self.user_id}',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    def test_edit_just_created_user_without_auth(self):
        # EDIT

        new_name = 'Changed name'

        response3 = MyRequests.put(
            f'/user/{self.user_id}',
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 400)

    def test_edit_just_created_user_another_user_auth(self):
        # LOGIN

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT

        new_name = 'Changed name'

        response3 = MyRequests.put(
            f'/user/{self.user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 400)

    def test_edit_just_created_user_to_wrong_email(self):
        # LOGIN

        self.login_current_user()

        # EDIT

        new_email = 'testemail.com'

        response3 = MyRequests.put(
            f'/user/{self.user_id}',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid},
            data={'email': new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()['error'] == 'Invalid email format'

    def test_edit_just_created_user_to_short_name(self):
        # LOGIN

        self.login_current_user()

        # EDIT

        new_name = 'I'

        response3 = MyRequests.put(
            f'/user/{self.user_id}',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()['error'] == "The value for field `firstName` is too short"
