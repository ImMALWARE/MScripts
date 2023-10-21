import vk_api

from random import shuffle
from time import sleep
token = 'token' # Токен от приложения VK Admin
api = vk_api.VkApi(token=token, api_version=5.131).get_api()
audios = []
while True:
    try:
        audio = api.audio.get(offset=len(audios))
    except: break
    if audio['items'] == []: break
    else: audios += audio['items']
while True:
    shuffle(audios)
    for audio in audios:
        api.audio.setBroadcast(audio=str(audio['owner_id'])+'_'+str(audio['id']))
        sleep(audio['duration'])