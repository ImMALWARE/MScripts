import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json

vk_session = vk_api.VkApi(token='token', api_version=5.131)
api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=12345) # тут айди группы без минуса

    
print("Бот запущен")
while True:
    try:
        for event in longpoll.listen():
            if event.type != VkBotEventType.MESSAGE_NEW: continue
            message = event.object.message
            args = message['text'].split(" ")
            cmd = args[0].lower()

            if cmd == '!проверка':
                api.messages.send(peer_id=message['peer_id'], message='Проверка успешна!', random_id=0, forward=json.dumps({'peer_id': message['peer_id'], 'conversation_message_ids': message['conversation_message_id'], 'is_reply': 1}))

            elif cmd == '!напиши':
                api.messages.send(peer_id=message['peer_id'], message=message['text'].replace(cmd+' ', ''), random_id=0, forward=json.dumps({'peer_id': message['peer_id'], 'conversation_message_ids': message['conversation_message_id'], 'is_reply': 1}))
            
            elif cmd == '!параметрысбщ':
                api.messages.send(peer_id=message['peer_id'], message='У сообщения такие параметры:\n'+'\n'.join([str(value)+': '+str(message[value]) for value in message]), random_id=0, forward=json.dumps({'peer_id': message['peer_id'], 'conversation_message_ids': message['conversation_message_id'], 'is_reply': 1}))

    except Exception as e:
        print(e)
