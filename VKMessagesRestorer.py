from requests import get # pip install requests
from time import sleep

token = 'token'

last = get(f'https://api.vk.com/method/messages.send?peer_id={get(f'https://api.vk.com/method/account.getProfileInfo?access_token={token}&v=5.131').json()['response']['id']}&message=Test&random_id=0&access_token={token}&v=5.131').json()['response']
msgs = get(f'https://api.vk.com/method/messages.getById?message_ids={','.join([str(last-i) for i in range(100)])}&access_token={token}&v=5.131').json()['response']['items']
for msg in msgs:
    if msg['out'] == 1 and 'deleted' in msg and msg['deleted'] == 1:
        print(f'Восстанавливаю сообщение {msg["id"]}:', get(f'https://api.vk.com/method/messages.restore?message_id={msg["id"]}&access_token={token}&v=5.131').json())
        sleep(0.5)