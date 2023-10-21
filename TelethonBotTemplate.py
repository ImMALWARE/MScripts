from telethon import TelegramClient, events

telegram = TelegramClient('session', 'api_id', 'api_hash').start()

@telegram.on(events.NewMessage(pattern='(!проверка)'))
async def handler_proverka(message):
    await message.reply('Проверка успешна!')

@telegram.on(events.NewMessage(pattern='(!напиши )'))
async def handler_napishi(message):
    await message.reply(message.text.replace('!напиши ', ''))

@telegram.on(events.NewMessage(pattern='(!параметрысбщ)'))
async def handler_parametri(message):
    await message.reply('У сообщения такие параметры:\n'+'\n'.join([str(value)+': '+str(vars(message)[value]) for value in vars(message) if not value.startswith('_')]))

print('Бот запущен')
telegram.run_until_disconnected()