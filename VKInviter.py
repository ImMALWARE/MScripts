import vk_api
from time import sleep
from random import uniform
chat_id = 123
user_id = 204923959
token = 'token'

api = vk_api.VkApi(token=token).get_api()
while True:
    try:
        chat = api.messages.getChat(chat_id=chat_id)
        print(len(chat['users']))
        if len(chat['users']) < 1000:
            try:
                api.messages.addChatUser(chat_id=chat_id, user_id=chat_id)
                exit()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    sleep(uniform(3.0, 5.0))
