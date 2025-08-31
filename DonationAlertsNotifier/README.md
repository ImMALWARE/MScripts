# Использование

1. Получаем токен оповещений DonationAlerts.  
   Для этого заходим сюда: [https://www.donationalerts.com/dashboard/alert-widget](https://www.donationalerts.com/dashboard/alert-widget),  
   возле "Группа 1" нажимаем "Показать ссылку для встраивания" и копируем её.  
   ![](https://i.imgur.com/Siak4NQ.png)  

   В конце этой ссылки будет токен. Подставляем его в переменную `da_alert_widget_token`.

2. Создаем бота в Telegram и получаем токен.  
   Для этого используем команду `/newbot` в боте [t.me/BotFather](https://t.me/BotFather), выбираем имя и адрес бота.  
   ![](https://i.imgur.com/LXibpYB.png)  

   Подставляем токен в переменную `tg_bot_token`.

3. Узнаем ID пользователя или канала, куда вы хотите отправлять сообщения.  
   Для этого ПЕРЕД добавлением бота в канал открываем ссылку: `https://api.telegram.org/bot{token}/getUpdates`
   и подставляем туда токен бота вместо `{token}`, затем переходим по ней.

4. Добавляем бота в канал или пишем ему любое сообщение, обновляем страницу и видим ID:  

    - ID пользователя:  
    ![](https://i.imgur.com/9PNt5ZU.png)  

    - ID канала:  
    ![](https://i.imgur.com/HpZKGtI.png)  

    Подставляем ID в переменную `tg_user_id`.

5. Устанавливаем зависимости:  
    ```bash
    pip install python-socketio websocket-client requests
    ```
6. Запускаем скрипт и ждем донатов 🙂