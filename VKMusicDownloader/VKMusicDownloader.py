from os import getcwd, name, system, remove
from os.path import isfile
from io import BytesIO
from re import sub
from subprocess import call

if name != 'nt': exit('Скрипт работает неправильно на Linux! Пожалуйста, используйте Windows!')
system('title VKMusic Downloader')
system('cls')
print('Внимание! ВК не позволяет загружать некоторые треки с нероссийским айпи! В то же время, MusixMatch заблокирован РКНом. Используйте zapret или WARP.')
system('pause')


config = {
    "vk_user_agent": "KateMobileAndroid/92.2 v1-524 (Android 11; SDK 30; x86; Pixel sdk_gphone_x86_arm; ru)",
    "vk_katemobile_token": "",
    "genius_token": "",
    "owner_id": 1234567
}

try:
    from requests import Session, get
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TT2, TPE1, APIC, USLT
    from bs4 import BeautifulSoup
    from PIL import Image
except:
    system('pip install requests mutagen bs4 pillow')
    system('python "'+__file__+'"')
    exit()

s, mm = Session(), Session()
s.headers.update({'User-Agent': config['vk_user_agent']})
mm.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
response = s.get(f'https://api.vk.com/method/audio.get?owner_id={config["owner_id"]}&count=6000&access_token={config["vk_katemobile_token"]}&v=5.131').json()['response']
print(f'Будет загружено {response["count"]} треков в папку {getcwd()}')
for song in response['items']:
    if isfile(f'{song["artist"]} — {song["title"]}.mp3'):
        print(f'Трек {song["artist"]} — {song["title"]}.mp3 уже загружен, пропускаю')
        continue
    if song['url'] == '':
        print(f'Внимание! Нельзя скачать трек {song["artist"]} — {song["title"]}! Скачайте вручную!')
        system('pause')
        continue
    print(f'Скачиваю трек {song["artist"]} — {song["title"]}')
    with open(f'{song["artist"]} — {song["title"]}.mp3', 'wb') as file:
        file.write(s.get(song["url"]).content)
    track = MP3(f'{song["artist"]} — {song["title"]}.mp3', ID3=ID3)
    track.delete()
    track.tags.add(TT2(encoding=3, text=song['title']))
    track.tags.add(TPE1(encoding=3, text=song['artist']))
    track.save()

    # Получаю текст песни с MusixMatch
    lyrics = False
    cover_set = False
    musixmatch = BeautifulSoup(mm.get(f'https://www.musixmatch.com/search/{song["artist"]} - {song["title"]}/tracks'.replace(' ', '%20')).text, "html.parser")
    try:
        musixmatch = musixmatch.find_all('ul', {'class': "tracks list thumb-list"})[0]
        musixmatch = BeautifulSoup(mm.get("https://www.musixmatch.com"+musixmatch.find_all('a', {'class': 'title'})[0]['href']).text, "html.parser")
        if cols := musixmatch.find_all('span', {'class': "lyrics__content__ok"}, string=True):
            lyrics = "\n".join(x.text for x in cols)
        elif data := musixmatch.find_all('span', {'class': "lyrics__content__warning"}, string=True):
            lyrics = "\n".join(x.text for x in data)
        elif musixmatch.find_all('h2', {'class': 'mxm-empty__title'})[0].text == 'Instrumental':
            print('Инструментальная песня, нет текста')
        else:
            raise Exception('Трек не найден на MusixMatch')
        if lyrics:
            track.tags.add(USLT(encoding=3, lang=u'eng', desc='', text=lyrics))
            track.save()
        else:
            lyrics = True
    except (IndexError, Exception):
        track.save()
        print(f'Не удалось найти текст песни {song["artist"]} — {song["title"]}! Ищу на Genius!')
    
    # Получаю обложку трека с MusixMatch
    if lyrics:
        try:
            if musixmatch.find_all('div', {'class': "banner-album-image-desktop"})[0].find_all('img')[0]['src'] == '//s.mxmcdn.net/site/images/albums/nocover_new-350x350.png':
                raise Exception('Стандартная обложка не подойдёт')
            Image.open(BytesIO(get("https:"+musixmatch.find_all('div', {'class': "banner-album-image-desktop"})[0].find_all('img')[0]['src']).content)).convert('RGB').save('temp_cover.jpg')
            track.tags.add(APIC(encoding=0, mime='image/jpg', type=3, desc='', data=open('temp_cover.jpg', 'rb').read()))
            track.save()
            cover_set = True
            continue
        except:
            print(f'Не удалось найти обложку {song["artist"]} — {song["title"]} на MusixMatch. Ищу на Genius!')
    
    search = get(f'https://api.genius.com/search/?q={song["artist"]} - {song["title"]}&access_token={config["genius_token"]}').json()
    try:
        if not lyrics:
            if not search['response']['hits'][0]['type'] == 'song':
                raise Exception('Не удалось найти песню на Genius')
            lyrics = sub(r'\[[^\]]*\]', '', "\n".join(x.get_text(separator='\n') for x in BeautifulSoup(get('https://genius.com' + search['response']['hits'][0]['result']['path']).text, "html.parser").find_all('div', {'data-lyrics-container': "true"}))).lstrip('\n')
            temp_file = f'Верный ли это текст песни для {song["artist"]} - {song["title"]}？Смотрите в консоль.txt'
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(lyrics)
            print(f'Верный ли это текст песни для {song["artist"]} - {song["title"]}? Если да - закройте блокнот. Если нет, измените и сохраните, затем закройте блокнот.')
            call(['notepad.exe', temp_file])
            system('pause')
            with open(temp_file, 'r', encoding='utf-8') as file:
                track.tags.add(USLT(encoding=3, lang=u'eng', desc='', text=file.read()))
                track.save()
            remove(temp_file)
        if not cover_set:
            if 'default_cover_image.png' in search['response']['hits'][0]['result']['song_art_image_url']:
                raise Exception('Стандартная обложка не подойдёт')
            Image.open(BytesIO(get(search['response']['hits'][0]['result']['song_art_image_url']).content)).convert('RGB').save('temp_cover.jpg')
            track.tags.add(APIC(encoding=0, mime='image/jpg', type=3, desc='', data=open('temp_cover.jpg', 'rb').read()))
            track.save()
    except Exception as e:
        if not lyrics:
            print(f'Не удалось найти текст песни {song["artist"]} — {song["title"]}! Установите текст вручную!')
            system('pause')
        if not cover_set:
            print(f'Не удалось найти обложку {song["artist"]} — {song["title"]}! Установите обложку вручную!')
            system('pause')

remove('temp_cover.jpg')
