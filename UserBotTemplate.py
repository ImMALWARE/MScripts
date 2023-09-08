import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

vk_session = vk_api.VkApi(token='token', api_version=5.131)
api = vk_session.get_api()
longpoll = VkLongPoll(vk_session, preload_messages=True)
    
print("Бот запущен")
while True:
    try:
        for event in longpoll.listen():
            if event.type != VkEventType.MESSAGE_NEW and event.type != VkEventType.MESSAGE_EDIT: continue
            message = event.message_data
            # if not message['out']: continue
            # Если нужно, чтобы бот реагировал только на сообщения от хозяина страницы, нужно убрать комментирование на строке выше
            args = message['text'].split(" ")
            cmd = args[0].lower()

            if cmd == '!проверка':
                # Если нужно, чтобы бот редактировал отправленное сообщение: (я буду использовать именно этот способ)
                api.messages.edit(peer_id=message['peer_id'], message_id=message['id'], message='Проверка успешна!', keep_forward_messages=1)
                # Если нужно, чтобы бот отвечал новым сообщением:
                # api.messages.send(peer_id=message['peer_id'], message='Проверка успешна!', random_id=0, forward=json.dumps({'peer_id': message['peer_id'], 'conversation_message_ids': message['conversation_message_id'], 'is_reply': 1}))

            elif cmd == '!напиши':
                api.messages.edit(peer_id=message['peer_id'], message_id=message['id'], message=message['text'].replace(cmd+' ', ''), keep_forward_messages=1)
            
            elif cmd == '!параметрысбщ':
                api.messages.edit(peer_id=message['peer_id'], message_id=message['id'], message='У сообщения такие параметры:\n'+'\n'.join([str(value)+': '+str(message[value]) for value in message]), keep_forward_messages=1)
    
    except Exception as e:
        print(e)
