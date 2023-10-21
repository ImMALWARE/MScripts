import json
from os.path import isfile
from time import sleep

from telethon.sync import TelegramClient

config = {
    'tg_api_id': '12345',
    'tg_api_hash': '3f46s5c7z65875084f39z8d8v89174',
    'channel_id': '-1001853994420',
    'notifications_chat_id': 657195904,
    'bot_token': '12345678:AdfwtKwyBycRyj97JPfd9I',
    'refresh_rate': '5'
}

if not isfile('session.session'): print('Войдите от имени администратора канала, у которого есть доступ к журналу событий')
telegram = TelegramClient('session', config['tg_api_id'], config['tg_api_hash']).start()
bot = TelegramClient('bot', config['tg_api_id'], config['tg_api_hash']).start(bot_token=config['bot_token'])
if not isfile('aln_data.malw'):
    with open('aln_data.malw', 'w') as file:
        file.write('[]')
        data = []
else:
    with open('aln_data.malw', 'r') as file:
        data = json.loads(file.read())

while True:
    events = reversed(list(telegram.get_admin_log(entity=int(config['channel_id']), info=False, settings=False, pinned=False, edit=False, delete=False, group_call=False)))
    for event in events:
        if event.id in data: continue
        event2 = event.action.to_dict()
        try:
            if event2['_'] == 'ChannelAdminLogEventActionParticipantJoinByInvite':
                bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') вступил в канал по ссылке '+event2['invite']['link'], parse_mode='markdown')
            elif event2['_'] == 'ChannelAdminLogEventActionParticipantInvite':
                bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') пригласил ['+telegram.get_entity(event2['participant']['user_id']).first_name+'](tg://user?id='+str(event2['participant']['user_id'])+') в канал', parse_mode='markdown')
            elif event2['_'] == 'ChannelAdminLogEventActionParticipantJoin':
                bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') подписался на канал!', parse_mode='markdown')
            elif event2['_'] == 'ChannelAdminLogEventActionParticipantLeave':
                bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') покинул канал', parse_mode='markdown')
            elif event2['_'] == 'ChannelAdminLogEventActionParticipantToggleAdmin':
                if event2['prev_participant']['_'] == 'ChannelParticipant' and event2['new_participant']['_'] == 'ChannelParticipantAdmin':
                    bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event2['new_participant']['promoted_by']).first_name+'](tg://user?id='+str(event2['new_participant']['promoted_by'])+') назначил пользователя ['+telegram.get_entity(event2['new_participant']['user_id']).first_name+'](tg://user?id='+str(event2['new_participant']['user_id'])+') администратором')
                elif event2['prev_participant']['_'] == 'ChannelParticipantAdmin' and event2['new_participant']['_'] == 'ChannelParticipant':
                    bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') разжаловал пользователя ['+telegram.get_entity(event2['new_participant']['user_id']).first_name+'](tg://user?id='+str(event2['new_participant']['user_id'])+'), он больше не администратор')
                elif event2['prev_participant']['_'] == 'ChannelParticipantAdmin' and event2['new_participant']['_'] == 'ChannelParticipantAdmin':
                    bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') отредактировал права администратора ['+telegram.get_entity(event2['new_participant']['user_id']).first_name+'](tg://user?id='+str(event2['new_participant']['user_id'])+')')
            elif event2['_'] == 'ChannelAdminLogEventActionParticipantToggleBan':
                if event2['prev_participant']['_'] == 'ChannelParticipantBanned' and event2['new_participant']['_'] == 'ChannelParticipantLeft':
                    bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') разблокировал пользователя ['+telegram.get_entity(event2['new_participant']['peer']['user_id']).first_name+'](tg://user?id='+str(event2['new_participant']['peer']['user_id'])+')')
                elif event2['prev_participant']['_'] == 'ChannelParticipant' and event2['new_participant']['_'] == 'ChannelParticipantBanned':
                    bot.send_message(config['notifications_chat_id'], ''+'['+telegram.get_entity(event.user_id).first_name+'](tg://user?id='+str(event.user_id)+') заблокировал пользователя ['+telegram.get_entity(event2['new_participant']['peer']['user_id']).first_name+'](tg://user?id='+str(event2['new_participant']['peer']['user_id'])+')')
            data.append(event.id)
        except Exception as e:
            print(e)
            bot.send_message(config['notifications_chat_id'], 'Произошла ошибка :(\nСобытие: '+json.dumps(event2)+'\nОшибка: '+str(e))
    with open('aln_data.malw', 'w') as file:
        file.write(json.dumps(data))
    sleep(int(config['refresh_rate']))