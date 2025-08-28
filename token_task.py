import requests
import time

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')

token = response.json()['token']
seconds = response.json()['seconds']

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})

def check_messages(message, check_message):
    if message == check_message:
        print('Message is correct')
        return True
    else:
        print('Message is not correct!')
        return False

if check_messages(response.json()['status'], 'Job is NOT ready'):
    print(f'Task will be ready from {seconds} seconds')
    time.sleep(seconds)
    response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
    if check_messages(response.json()['status'], 'Job is ready'):
        try:
            if response.json()['result']:
                print('Task is ready!')
        except Exception:
            print('There is not "result" field!')
