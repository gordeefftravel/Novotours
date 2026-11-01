"""Сайт Novo Tours на Flask.

Запуск локально:  python app.py   (откроется http://127.0.0.1:5000)
Продакшен:        gunicorn app:app
"""
import json
import logging
import os
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

try:  # .env необязателен
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from tours import COMPANY, PERKS, TOURS

BASE_DIR = Path(__file__).resolve().parent
LEADS_FILE = BASE_DIR / "leads.jsonl"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("novo")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Не больше 5 заявок за 10 минут с одного адреса
_hits = defaultdict(deque)
LIMIT, WINDOW = 5, 600


def _too_many(ip: str) -> bool:
    now = time.time()
    q = _hits[ip]
    while q and now - q[0] > WINDOW:
        q.popleft()
    if len(q) >= LIMIT:
        return True
    q.append(now)
    return False


def _send_telegram(text: str) -> bool:
    if not (BOT_TOKEN and CHAT_ID):
        log.warning("Telegram не настроен: заявка сохранена только в leads.jsonl")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10) as r:
            return r.status == 200
    except Exception as exc:  # noqa: BLE001
        log.error("Ошибка отправки в Telegram: %s", exc)
        return False


@app.get("/")
def index():
    return render_template("index.html", company=COMPANY, tours=TOURS, perks=PERKS,
                           now_year=datetime.now().year)


@app.post("/api/lead")
def lead():
    d = request.get_json(silent=True) or {}
    if d.get("website"):  # ловушка для ботов
        return jsonify(ok=True)
    name = str(d.get("name", "")).strip()[:100]
    phone = str(d.get("phone", "")).strip()[:30]
    tour = str(d.get("tour", "")).strip()[:150]
    comment = str(d.get("comment", "")).strip()[:500]
    if len(name) < 2:
        return jsonify(ok=False, error="Укажите имя"), 400
    if len(re.sub(r"\D", "", phone)) < 10:
        return jsonify(ok=False, error="Укажите телефон"), 400
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
    if _too_many(ip):
        return jsonify(ok=False, error="Слишком много заявок, попробуйте позже"), 429

    record = {"time": datetime.now().isoformat(timespec="seconds"), "name": name,
              "phone": phone, "tour": tour, "comment": comment}
    with LEADS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    text = ("Новая заявка с сайта Novo Tours\n"
            f"Тур: {tour or 'не указан'}\nИмя: {name}\nТелефон: {phone}"
            + (f"\nКомментарий: {comment}" if comment else ""))
    _send_telegram(text)
    return jsonify(ok=True)


@app.get("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
