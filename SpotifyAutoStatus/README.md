<h2>Использование</h2>
<p>Нужно заполнить конфиг, затем, после запуска, войти в Spotify в браузере и войти в Telegram в консоли</p>
<h2>Конфиг</h2>
<ul class="normal">
    <li><b>vk-default-status</b> - Статус в ВК, когда в Spotify ничего не играет</li>
    <li><b>telegram-default-status</b> - О себе в Telegram, когда в Spotify ничего не играет</li>
    <li><b>status-update-timeout</b> - Количество секунд, спустя которое нужно обновить статус</li>
    <li><b>spotify-client-id</b> - Client ID приложения Spotify</li>
    <li><b>spotify-client-secret</b> - Client secret приложения Spotify</li>
    <li><b>spotify-redirect-uri</b> - redirect uri приложения Spotify</li>
    <li><b>spotify-username</b> - Часть ссылки на ваш профиль Spotify</li>
    <li><b>vk-token</b> - Токен ВК</li>
    <li><b>vk-online-when-listen-spotify</b> - Нужно ли делать вас онлайн в ВК, когда включен Spotify (True/False)</li>
    <li><b>use-telegram</b> - Нужно ли обновлять био в телеграм (поставьте False, если хотите автостатус только в ВК)</li>
    <li><b>telegram-api-id</b> - API ID приложения Telegram</li>
    <li><b>telegram-api-hash</b> - API hash приложения Telegram</li>
</ul>
<details>
    <summary>Где взять параметры, связанные с Spotify (тык)</summary>
    <ol>
        <li>Заходим на <a href="https://developer.spotify.com/dashboard/" target="_blank">https://developer.spotify.com/dashboard/"</a>, авторизуемся. Для российских пользователей понадобится VPN.</li>
        <li>Создаем приложение <img src="https://i.imgur.com/DGTUoJf.png" referrerpolicy="no-referrer" style="display: inline;">, вводим любое имя и описание, ставим галочку
            <img src="https://i.imgur.com/KhbkhG7.png" referrerpolicy="no-referrer" width="300px"></li>
        <li>Нажимаем на show client secret<img src="https://i.imgur.com/KsHOA2G.png" referrerpolicy="no-referrer" width="300px"></li>
        <li>Два значения уже получили. Теперь нажимаем edit settings<img src="https://i.imgur.com/Ku1lzHg.png" referrerpolicy="no-referrer" style="display: inline;"></li>
        <li>Вводим http://localhost:8888/callback в redirect url. (в конфиге тоже)
            <img src="https://i.imgur.com/Hv8aYGM.png" referrerpolicy="no-referrer"></li>
        <li>Для получения ссылки на свой профиль заходим на <a href="https://open.spotify.com/" target="_blank">https://open.spotify.com/</a>, для пользователей из России понадобится VPN.</li>
        <li><img src="https://i.ibb.co/74JZn9y/image.png" style="display: math;"></li>
        <li>Копируем значение после user/<img src="https://i.ibb.co/j8MdV24/image.png">Это <b>spotify-username</b></li>
    </ol>
</details>
<details>
    <summary>Где взять значения, связанные с Telegram (тык)</summary>
    <ol>
        <li>Заходим на <a href="https://my.telegram.org/" target="_blank">https://my.telegram.org/</a>, авторизуемся</li>
        <li><img src="https://i.ibb.co/7bk1xtj/image.png" style="display: math;"></li>
        <li>Создаем приложение</li>
        <li>Вот и данные</li>
    </ol>
</details>
