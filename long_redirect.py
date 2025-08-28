import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')

print(f'There is {len(response.history)} redirects.\nFinally URL is: "{response.url}"')
