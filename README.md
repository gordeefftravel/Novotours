# Сайт Novo Tours (Python + Flask)

## Что внутри
- `app.py` — сервер: главная страница и приём заявок (`/api/lead`)
- `tours.py` — **все туры, цены, контакты, адрес и график**. Меняете здесь
- `templates/index.html` — страница, `static/` — стили, скрипт и картинки
- `leads.jsonl` — сюда пишутся все заявки (создаётся сам)

## Запуск у себя
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # откройте http://127.0.0.1:5000
```

## Заявки в Telegram
1. В Telegram напишите @BotFather → `/newbot` → получите токен.
2. Напишите своему боту любое сообщение.
3. Откройте в браузере `https://api.telegram.org/bot<ТОКЕН>/getUpdates` и найдите `"chat":{"id":...}` — это ваш chat id.
4. Скопируйте `.env.example` в `.env` и впишите `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`.

Без этого сайт работает, заявки просто сохраняются в `leads.jsonl`.

## Бот Novo Tours
`bot.py` — отдельный бот: `/tours` показывает туры и цены из `tours.py`, `/contacts` — адрес и контакты, `/id` — ваш chat id.
Запуск (в отдельном окне, рядом с сайтом): `python bot.py`. На сервере его запускают как отдельную службу (systemd) или процесс.
Порядок: создайте бота в @BotFather, впишите токен в `.env`, запустите `python bot.py`, напишите боту `/id`, впишите ответ в `TELEGRAM_CHAT_ID`, перезапустите сайт.

## Как добавить или изменить тур
Откройте `tours.py`, скопируйте любой блок в списке `TOURS`, поменяйте текст и положите афишу в `static/img/`. Перезапустите сервер.

## Публикация в интернете
На сервере (VPS) или хостинге с Python:
```bash
pip install -r requirements.txt
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```
Перед gunicorn обычно ставят nginx с HTTPS (Let's Encrypt) и подключают домен. Подойдут также PythonAnywhere, Render, Railway: команда запуска `gunicorn app:app`.
Токен бота храните только в переменных окружения или `.env`, не публикуйте его.
