from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
import json
from os.path import isfile
from random import choice
from re import sub
bot = Bot(token='token')
dp = Dispatcher(bot)
channels = [-1001682799926]
admins = [657195904]

if not isfile('participants.malw'):
    with open('participants.malw', 'w') as file:
        file.write('[]')
with open('participants.malw', 'r') as file:
    participants = json.loads(file.read())

@dp.message_handler(commands='start')
async def start(message: types.Message):
    global participants, channels
    if str(message['from']['id']) in participants:
        await message.reply('Ты уже участвуешь в розыгрыше', disable_web_page_preview=True)
        return
    for channel in channels:
        try:
            user_info = await bot.get_chat_member(channel, message['from']['id'])
            if user_info['status'] not in ['member', 'creator', 'administrator']:
                raise
        except Exception as e:
            channel_info = await bot.get_chat(channel)
            await message.reply('Ты не подписан на '+link(channel_info['title'], 'https://t.me/'+channel_info['username']), parse_mode='markdown', disable_web_page_preview=True)
            return
    participants.append(str(message['from']['id']))
    with open('participants.malw', 'w') as file:
        file.write(json.dumps(participants))
    await message.reply('Ты принял участие в розыгрыше', disable_web_page_preview=True)

@dp.message_handler(commands='check')
async def check(message: types.Message):
    global participants, channels
    if message['from']['id'] in admins:
        for participant in participants:
            for channel in channels:
                try:
                    user_info = await bot.get_chat_member(channel, participant)
                    if user_info['status'] not in ['member', 'creator', 'administrator']:
                        raise
                except Exception as e:
                    channel_info = await bot.get_chat(channel)
                    try:
                        await bot.send_message(participant, 'Ты вышел из канала '+link(channel_info['title'], 'https://t.me/'+channel_info['username'])+', поэтому больше не участвуешь в розыгрыше', parse_mode='markdown', disable_web_page_preview=True)
                    except: pass
                    participants.remove(participant)
                    break
        with open('participants.malw', 'w') as file:
            file.write(json.dumps(participants))
        await message.reply('Проверка завершена', disable_web_page_preview=True)

@dp.message_handler(commands='end')
async def end(message: types.Message):
    global participants
    if message['from']['id'] in admins:
        if participants == []:
            await message.reply('В розыгрыше никто не участвует', disable_web_page_preview=True)
            return
        winner = choice(participants)
        winner_name = await bot.get_chat(winner)
        for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', winner_name['first_name']):
            winner_name['first_name'] = winner_name['first_name'].replace(ts, '')
        if winner_name['first_name'].replace(' ', '') == '':
            winner_name['first_name'] = 'Пустой или засранный ник'
        if 'username' in winner_name:
            name = link(winner_name['first_name'], 'https://t.me/'+winner_name['username'])+'\n'
        elif not "has_private_forwards" in winner_name:
            name = link(winner_name['first_name'], 'tg://user?id='+winner)+'\n'
        else:
            name = winner_name['first_name']+' (невозможно упомянуть)'+'\n'
        for participant in participants:
            try:
                await bot.send_message(int(participant), 'Честная система рандома определила победителя этого розыгрыша. Им становится '+name, parse_mode='markdown', disable_web_page_preview=True)
            except:
                pass
        await message.reply('Честная система рандома определила победителя этого розыгрыша. Им становится '+link(winner_name['first_name'], 'tg://user?id='+winner), parse_mode='markdown', disable_web_page_preview=True)
        with open('participants_old.malw', 'w') as file:
            file.write(json.dumps(participants))
        participants = []
        with open('participants.malw', 'w') as file:
            file.write(json.dumps(participants))

@dp.message_handler(commands='testend')
async def end(message: types.Message):
    global participants
    if message['from']['id'] in admins:
        if participants == []:
            await message.reply('В розыгрыше никто не участвует', disable_web_page_preview=True)
            return
        winner = choice(participants)
        winner_name = await bot.get_chat(winner)
        for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', winner_name['first_name']):
            winner_name['first_name'] = winner_name['first_name'].replace(ts, '')
        if winner_name['first_name'].replace(' ', '') == '':
            winner_name['first_name'] = 'Пустой или засранный ник'
        if 'username' in winner_name:
            name = link(winner_name['first_name'], 'https://t.me/'+winner_name['username'])+'\n'
        elif not "has_private_forwards" in winner_name:
            name = link(winner_name['first_name'], 'tg://user?id='+winner)+'\n'
        else:
            name = winner_name['first_name']+' (невозможно упомянуть)'+'\n'
        await message.reply('Тестовое завершение. Список участников не очищается и сообщения не рассылаются. Честная система рандома определила победителя этого розыгрыша. Им становится '+name, parse_mode='markdown', disable_web_page_preview=True)


@dp.message_handler(commands='list')
async def list(message: types.Message):
    global participants
    if message['from']['id'] in admins:
        if participants == []:
            await message.reply('В розыгрыше никто не участвует', disable_web_page_preview=True)
            return
        list = ''
        for participant in participants:
            participant_info = await bot.get_chat(participant)
            for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', participant_info['first_name']):
                participant_info['first_name'] = participant_info['first_name'].replace(ts, '')
            if participant_info['first_name'].replace(' ', '') == '':
                participant_info['first_name'] = 'Пустой или засранный ник'
            if 'username' in participant_info:
                list += link(participant_info['first_name'], 'https://t.me/'+participant_info['username'])+'\n'
            elif not "has_private_forwards" in participant_info:
                list += link(participant_info['first_name'], 'tg://user?id='+participant)+'\n'
            else:
                list += participant_info['first_name']+' (невозможно упомянуть)'+'\n'
        await message.reply('Список участников розыгрыша:\n'+list, parse_mode='markdown', disable_web_page_preview=True)

executor.start_polling(dp, skip_updates=True)