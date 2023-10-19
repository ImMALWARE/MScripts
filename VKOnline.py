from urllib.request import urlopen
from time import sleep
tokens = ['token1', 'token2']
while True:
    for token in tokens: print(urlopen(f'https://api.vk.com/method/account.setOnline?voip=1&access_token={token}&v=5.131').read().decode())
    sleep(120)
