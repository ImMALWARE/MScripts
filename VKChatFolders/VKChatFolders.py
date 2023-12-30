try:
    from requests import post
except:
    from os import system
    system('pip install requests')
    system('python '+__file__)
    exit()

token = 'token'

personal = []
chats = []
bots = []
offset = 0

while True:
    request = post('https://api.vk.me/method/messages.getConversations', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}, params={'v': '5.131'}, data={'count': 200, 'offset': offset, 'access_token': token}).json()
    try:
        request = request['response']['items']
    except:
        print(request)
        exit()
    if request == []: break
    for item in request:
        if item['conversation']['peer']['type'] == 'user':
            personal.append(item['conversation']['peer']['id'])
        elif item['conversation']['peer']['type'] == 'chat':
            chats.append(item['conversation']['peer']['id'])
        elif item['conversation']['peer']['type'] == 'group':
            bots.append(item['conversation']['peer']['id'])
    offset += 200

print(post('https://api.vk.me/method/messages.createFolder', params={'v': '5.198'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'},
    data={'name': 'Личные', 'included_peer_ids': ','.join(list(map(str, personal[:500]))), 'extended': '1', 'access_token': token}).json())

print(post('https://api.vk.me/method/messages.createFolder', params={'v': '5.198'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'},
    data={'name': 'Беседы', 'included_peer_ids': ','.join(list(map(str, chats[:500]))), 'extended': '1', 'access_token': token}).json())

print(post('https://api.vk.me/method/messages.createFolder', params={'v': '5.198'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'},
    data={'name': 'Боты', 'included_peer_ids': ','.join(list(map(str, bots[:500]))), 'extended': '1', 'access_token': token}).json())