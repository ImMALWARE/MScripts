from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='token')
dp = Dispatcher(bot)

@dp.message_handler(regexp='(!проверка)')
async def handler_proverka(message: types.Message):
    await message.reply('Проверка успешна!')

@dp.message_handler(regexp='(!напиши )')
async def handler_napishi(message: types.Message):
    await message.reply(message.text.replace('!напиши ', ''))

@dp.message_handler(regexp='(!параметрысбщ)')
async def handler_parametri(message: types.Message):    
    await message.reply('У сообщения такие параметры:\n'+'\n'.join([str(value)+': '+str(message[value]) for value in dict(message)]))

print('Бот запущен')
executor.start_polling(dp, skip_updates=True)