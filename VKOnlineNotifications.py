from requests import get
from time import strftime, localtime, sleep
token = 'token'
group_token = 'token'
user_id = 1
sleep_time = 60
# Больше ничего редактировать не нужно

owner_id = get(f'https://api.vk.com/method/account.getProfileInfo?v=5.131&access_token={token}').json()['response']['id']
last_online_time = get(f'https://api.vk.com/method/users.get?fields=online,last_seen&v=5.131&user_ids={user_id}&access_token={token}').json()['response'][0]['last_seen']['time']
last_online = False

while True:
    online_info = get(f'https://api.vk.com/method/users.get?fields=online,last_seen&v=5.131&user_ids={user_id}&access_token={token}').json()['response'][0]
    if online_info['online'] == 1 and not last_online:
        get(f'https://api.vk.com/method/messages.send?peer_id={owner_id}&message=[id{user_id}|{online_info["first_name"]} {online_info["last_name"]}] в сети!&random_id=0&v=5.131&access_token={group_token}')
        last_online = True
    elif online_info['online'] == 0:
        if last_online:
            get(f'https://api.vk.com/method/messages.send?peer_id={owner_id}&message=[id{user_id}|{online_info["first_name"]} {online_info["last_name"]}] больше не в сети.&random_id=0&v=5.131&access_token={group_token}')
            last_online = False
        if online_info['last_seen']['time'] != last_online_time:
            get(f'https://api.vk.com/method/messages.send?peer_id={owner_id}&message=[id{user_id}|{online_info["first_name"]} {online_info["last_name"]}] был в сети в {strftime("%H:%M", localtime(online_info["last_seen"]["time"]))}&random_id=0&v=5.131&access_token={group_token}')
            last_online_time = online_info['last_seen']['time']
    sleep(sleep_time)
