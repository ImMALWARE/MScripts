import json
import socketio
from requests import get
# pip install python-socketio websocket-client requests
da_alert_widget_token = 'da_token'
tg_bot_token = '12345:tg_token'
tg_user_id = 123457899


sio = socketio.Client(reconnection=True, reconnection_delay=5)

@sio.on('connect')
def on_connect():
    sio.emit('add-user', {'token': da_alert_widget_token, "type": "alert_widget"})
    print('Бот запущен')

@sio.on('donation')
def on_message(data):
    event = json.loads(data)
    print(event)
    get(f'https://api.telegram.org/bot{tg_bot_token}/sendMessage?chat_id={tg_user_id}&text=Новый донат:\n{event["username"]} - {event["amount"]} {event["currency"]}\n{event["message"]}')

sio.connect('wss://socket.donationalerts.ru:443', transports='websocket')