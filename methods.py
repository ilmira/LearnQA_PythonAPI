import requests

response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(f'No method: {response.text}')

response = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': 'HEAD'})
print(f'HEAD method: {response.text}')

response = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': 'POST'})
print(f'POST method: {response.text}')

methods = ['GET', 'POST', 'PUT', 'DELETE']
wrong_data = {}


def find_wrong_data(type, method, response_text):
    if response_text == 'Wrong method provided' and method == type.upper():
        wrong_data[type] = f'method: {method}'
    elif response_text == '{"success":"!"}' and method != type.upper():
        wrong_data[type] = f'method: {method}'


for method in methods:
    response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type',
                            params={'method': method})
    find_wrong_data('get', method, response.text)

    response = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type',
                             data={'method': method})
    find_wrong_data('post', method, response.text)

    response = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type',
                            data={'method': method})
    find_wrong_data('put', method, response.text)

    response = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type',
                               data={'method': method})
    find_wrong_data('delete', method, response.text)

print(f'Wrong type found for: {wrong_data}')
