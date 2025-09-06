import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        print(f'\nText is: {response.cookies}')

        assert response.cookies
        assert response.cookies.get('HomeWork')
        assert response.cookies.get('HomeWork') == 'hw_value'
