import vk_api
token = 'token'
api = vk_api.VkApi(token=token).get_api()
mode = input('Какие беседы показать? 1 - все, 2 - только те, в которых ты состоишь, 3 - только те, где ты не состоишь и не очистил историю, 4 - только те, где ты состоишь и очистил историю: ')
if not int(mode) in [1,2,3,4]: exit('Неверное значение')
print('Получаю беседы...')
for i in range(1, 100000001):
    try:
        chat = api.messages.getChat(chat_id=i)
    except Exception as e:
        if str(e) == "[946] Chat not supported": print(str(i)+': Фантом-чат')
        elif str(e) == "[100] One of the parameters specified was missing or invalid: chat_id param is incorrect": break
        else:
            print(e)
            break
    chat_info = str(chat['id'])+': '+str(chat['title'])+'. '
    if 'left' in chat:
        chat_info += 'Вышел, '
        if mode in ['2', '4']: continue
    elif 'kicked' in chat:
        chat_info += 'Исключен, '
        if mode in ['2', '4']: continue
    else:
        chat_info += 'В составе, '
        if mode == '3': continue
    if api.messages.getHistory(peer_id=2000000000+chat['id'])['count'] == 0:
        chat_info += 'история очищена.'
        if mode == '3': continue
    else:
        chat_info += 'история не очищена.'
        if mode == '4': continue
    print(chat_info)
input('Всё!\n')
