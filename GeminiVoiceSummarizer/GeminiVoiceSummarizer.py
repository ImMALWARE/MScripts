gemini_token = 'https://lolz.live/threads/6818835/'
bot_token = 'https://t.me/botfather'
allowed_users = [657195904, -1001537487920]

# Больше ничего редактировать не нужно

import asyncio
from aiogram import Router, Bot, Dispatcher, F, types
import logging
from io import BytesIO
from pydub import AudioSegment
import google.generativeai as gemini
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import ResourceExhausted
from ssl import SSLError
from os import remove
from asyncio import sleep

bot = None
router = Router(name=__name__)
lock = asyncio.Lock()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

gemini.configure(api_key=gemini_token)

async def telegram_voice_gemini_tts(file_id: str, format: str, message_id: int) -> str:
    wav_io = BytesIO()
    AudioSegment.from_file((await bot.download_file((await bot.get_file(file_id)).file_path)), format=format).export(wav_io, format="wav")
    wav_io.seek(0)
    with open(f'vm{message_id}.wav', 'wb') as f: f.write(wav_io.getvalue())
    audio_file = gemini.upload_file(f'vm{message_id}.wav', mime_type='audio/wav')
    try:
        return gemini.GenerativeModel(model_name="gemini-1.5-flash").generate_content([f'Перескажи голосовое сообщение на русском языке. Сообщи об эмоциях автора. В случае, если ты услышал речь, начни свой ответ со слов "В {"голосовом сообщении" if format == "ogg" else "видеосообщении"} говорится". В случае, если ты не услышал в записи речь, сообщи о том, что в {"голосовом сообщении" if format == "ogg" else "видеосообщении"} нет речи.', audio_file], safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},{"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},]).text
    finally:
        remove(f'vm{message_id}.wav')

@router.business_message(F.voice | F.video_note)
async def handle_message(message: types.Message):
    async with lock:
        if not (await bot.get_business_connection(message.business_connection_id)).user.id in allowed_users: return
        logger.info(f"Received voice message from {message.from_user.id}")
        recognition_message = await bot.send_message(message.chat.id, '<tg-emoji emoji-id="5296262629558340179">🖥</tg-emoji>Gemini распознаёт голосовое сообщение<tg-emoji emoji-id="5220046725493828505">✍️</tg-emoji>' if message.voice else '<tg-emoji emoji-id="5296262629558340179">🖥</tg-emoji>Gemini распознаёт видеосообщение<tg-emoji emoji-id="5220070652756635426">👀</tg-emoji>', business_connection_id=message.business_connection_id, reply_to_message_id=message.message_id, parse_mode='HTML')
        await bot.send_chat_action(message.chat.id, 'upload_voice' if message.voice else 'upload_video_note', business_connection_id=message.business_connection_id)
        while True:
            try:
                tts_result = await telegram_voice_gemini_tts(message.voice.file_id if message.voice else message.video_note.file_id, 'ogg' if message.voice else 'mp4', message.message_id)
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='<tg-emoji emoji-id="5296262629558340179">🖥</tg-emoji><b>Gemini</b>: ' + tts_result, business_connection_id=message.business_connection_id, parse_mode='HTML')
            except ValueError:
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='<tg-emoji emoji-id="5807626765874499116">🚫</tg-emoji><tg-emoji emoji-id="5296262629558340179">🖥</tg-emoji>Gemini посчитал этот запрос небезопасным.', business_connection_id=message.business_connection_id, parse_mode='HTML')
            except (InternalServerError, SSLError):
                sleep(3)
            except ResourceExhausted:
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='<tg-emoji emoji-id="5456670136121434320">😔</tg-emoji><tg-emoji emoji-id="5296262629558340179">🖥</tg-emoji>Достигнут лимит запросов к Gemini :(', business_connection_id=message.business_connection_id, parse_mode='HTML')
            except Exception as e:
                logger.error(e)
                await bot.send_message(allowed_users[0], str(e))

# @router.message()
# async def echo(message: types.Message):
#     print(message.html_text)

@router.message(F.chat.type == 'private', F.text)
async def handle_message(message: types.Message):
    async with lock:
        if not message.from_user.id in allowed_users: return
        await bot.send_chat_action(message.chat.id, 'typing')
        response = gemini.GenerativeModel(model_name="gemini-1.5-pro").generate_content(message.text)
        await message.reply(response.text)

@router.message(F.voice | F.video_note)
async def handle_message(message: types.Message):
    async with lock:
        if not message.chat.id in allowed_users: return
        logger.info(f"Received voice message from {message.from_user.id}")
        recognition_message = await message.reply('Gemini распознаёт голосовое сообщение...' if message.voice else 'Gemini распознаёт видеосообщение...')
        await bot.send_chat_action(message.chat.id, 'upload_voice' if message.voice else 'upload_video_note')
        while True:
            try:
                tts_result = await telegram_voice_gemini_tts(message.voice.file_id if message.voice else message.video_note.file_id, 'ogg' if message.voice else 'mp4', message.message_id)
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='<b>Gemini</b>: ' + tts_result, parse_mode='HTML')
            except ValueError:
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='🚫Gemini посчитал этот запрос небезопасным.', parse_mode='HTML')
            except (InternalServerError, SSLError):
                sleep(3)
            except ResourceExhausted:
                return await bot.edit_message_text(chat_id=recognition_message.chat.id, message_id=recognition_message.message_id, text='😔Достигнут лимит запросов к Gemini :(')
            except Exception as e:
                logger.error(e)
                await bot.send_message(allowed_users[0], str(e))
                sleep(10)

async def main():
    global bot
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main()) 