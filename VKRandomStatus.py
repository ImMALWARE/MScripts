import vk_api
from random import choice
from time import sleep
token = 'token'
statuses = ['Статус', 'Автостатус', 'Рандомный статус', 'Мяу']

api = vk_api.VkApi(token=token).get_api()
while True:
    status = choice(statuses)
    api.status.set(text=status)
    print('Статус изменен на '+status)
    sleep(90)
