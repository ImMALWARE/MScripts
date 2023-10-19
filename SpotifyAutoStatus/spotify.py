from spotipy.oauth2 import SpotifyOAuth
import spotipy
import vk_api
from time import sleep

config = {
    'vk-default-status': "Статус в ВК, когда в Spotify ничего не играет",
    'telegram-default-status': 'О себе в Telegram, когда в Spotify ничего не играет',
    'status-update-timeout': 60,
    'spotify-client-id': "",
    'spotify-client-secret': "",
    'spotify-redirect-uri': "",
    'spotify-username': "as67lwic16uszxqpd6rbfimol",
    'vk-token': "token",
    'vk-online-when-listen-spotify': True,
    'use-telegram': True,
    'telegram-api-id': 1,
    'telegram-api-hash': ''
    }

if config['use-telegram']:
    from telethon.tl.functions.account import UpdateProfileRequest
    from telethon.sync import TelegramClient
    telegram = TelegramClient('telegram', config['telegram-api-id'], config['telegram-api-hash']).start()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state user-library-read", client_id=config['spotify-client-id'], client_secret=config['spotify-client-secret'], redirect_uri=config['spotify-redirect-uri'], username=config['spotify-username']))
api = vk_api.VkApi(token=config['vk-token']).get_api()
current_status = api.status.get()['text']

def change_status(status):
    if not status == current_status:
        api.status.set(text=status[:140])
        if config['vk-online-when-listen-spotify']: api.account.setOnline(voip=1)
        print('Статус в VK обновлен')
    if config['use-telegram']:
        telegram(UpdateProfileRequest(about=status[:70]))
        print('Статус в Telegram обновлен')
    print(status)
def default_status():
    api.status.set(text=config['vk-default-status'][:140])
    print('Статус в VK обновлен')
    if config['use-telegram']:
        telegram(UpdateProfileRequest(about=config['telegram-default-status'][:70]))
        print('Статус в Telegram обновлен')
    print('Установлен обычный статус')
def calculate_minutes(ms): return str(int(((ms / (1000*60)) % 60)))
def calculate_seconds(ms): return str(int((ms / 1000) % 60)) if len(str(int((ms / 1000) % 60))) > 1 else '0'+str(int((ms / 1000) % 60))
while True:
    current_playing = spotify.current_user_playing_track()
    if current_playing is None or current_playing["currently_playing_type"] == "ad":
        default_status()
        sleep(int(config['status-update-timeout'])*2)
        continue
    play_emoji = '' if current_playing['is_playing'] == True else ''
    change_status(play_emoji+'Слушаю Spotify: '+current_playing["item"]["artists"][0]["name"]+' — '+current_playing["item"]["name"]+' ('+calculate_minutes(current_playing['progress_ms'])+':'+calculate_seconds(current_playing['progress_ms'])+'/'+calculate_minutes(current_playing['item']['duration_ms'])+':'+calculate_seconds(current_playing['item']['duration_ms'])+')')
    sleep(int(config['status-update-timeout']))
