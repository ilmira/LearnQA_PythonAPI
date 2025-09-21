from requests import Response
import json
import allure


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        with allure.step('Check JSON format:'):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        with allure.step(f'Check to have key and that value for key {name} is expected: {expected_value}:'):
            assert name in response_as_dict, f'Response JSON does not have key "{name}"'
            assert response_as_dict[name] == expected_value, (error_message +
                                                        f'ID is {response_as_dict[name]}, expected: {expected_value}')

    @staticmethod
    def assert_json_has_key(response: Response, name):
        with allure.step('Check JSON format:'):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        with allure.step(f'Check to have key {name}:'):
            assert name in response_as_dict, f'Response JSON does not have key "{name}"'

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        with allure.step('Check JSON format:'):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f'Response is not in JSON format. Response text is "{response.text}"'

        with allure.step(f'Check to have keys {names}:'):
            for name in names:
                assert name in response_as_dict, f'Response JSON does not have key "{name}"'

    @staticmethod
    def assert_json_not_has_key(response: Response, name):
        with allure.step('Check JSON format:'):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        with allure.step(f'Check to have not key {name}:'):
            assert name not in response_as_dict, f'Response JSON should not have key "{name}", but it is present'

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        with allure.step(f'Check status code is {expected_status_code}:'):
            assert response.status_code == expected_status_code, \
                f'Unexpected status code! Expected: {expected_status_code}, actual: {response.status_code}'
