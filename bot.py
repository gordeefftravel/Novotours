"""Telegram-бот Novo Tours (без сторонних библиотек).

Команды: /start, /tours, /contacts, /id
/id показывает chat id, его нужно вписать в .env как TELEGRAM_CHAT_ID,
чтобы заявки с сайта приходили именно вам.

Запуск: python bot.py   (работает отдельно от сайта)
"""
import json
import logging
import os
import time
import urllib.parse
import urllib.request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from tours import COMPANY, TOURS

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}/"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("novo-bot")


def call(method, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(urllib.request.Request(API + method, data=data), timeout=60) as r:
        return json.loads(r.read().decode())


def send(chat_id, text):
    call("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview="true")


def tours_text():
    lines = ["Актуальные туры Novo Tours:\n"]
    for t in TOURS:
        unit = f" ({t['unit']})" if t["unit"] else ""
        lines.append(f"• {t['title']} — {t['price']}{unit}\n  {t['when']}")
    lines.append("\nДля бронирования напишите менеджеру: " + COMPANY["telegram"])
    return "\n".join(lines)


def contacts_text():
    c = COMPANY
    return (f"{c['name']}\n{c['address']}\n{c['hours']}\n"
            f"Телефон: {c['phone_pretty']}\nTelegram: {c['telegram']}\nПочта: {c['email']}")


def handle(msg):
    chat_id = msg["chat"]["id"]
    cmd = (msg.get("text") or "").split()[0].split("@")[0].lower() if msg.get("text") else ""
    if cmd == "/id":
        send(chat_id, f"Ваш chat id: {chat_id}")
    elif cmd == "/tours":
        send(chat_id, tours_text())
    elif cmd == "/contacts":
        send(chat_id, contacts_text())
    else:
        send(chat_id, "Здравствуйте! Это бот Novo Tours.\n\n"
                      "/tours — актуальные туры и цены\n/contacts — адрес и контакты\n"
                      "/id — узнать chat id (для настройки заявок)")


def main():
    if not TOKEN:
        raise SystemExit("Укажите TELEGRAM_BOT_TOKEN в .env")
    offset = None
    log.info("Бот запущен")
    while True:
        try:
            params = {"timeout": 50}
            if offset:
                params["offset"] = offset
            for upd in call("getUpdates", **params).get("result", []):
                offset = upd["update_id"] + 1
                if "message" in upd:
                    handle(upd["message"])
        except Exception as exc:  # noqa: BLE001
            log.error("Ошибка: %s", exc)
            time.sleep(5)


if __name__ == "__main__":
    main()
