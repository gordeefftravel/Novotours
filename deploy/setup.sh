#!/usr/bin/env bash
# Установка сайта Novo Tours на чистый сервер Ubuntu 22.04/24.04.
# Запуск (от root, из папки проекта):  bash deploy/setup.sh novo.tours you@mail.ru
set -euo pipefail

DOMAIN="${1:?Укажите домен: bash deploy/setup.sh novo.tours you@mail.ru}"
EMAIL="${2:-Nowotours@gmail.com}"
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo ">> Устанавливаю пакеты"
apt-get update -y
apt-get install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx

echo ">> Окружение Python"
python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

if [ ! -f "$APP_DIR/.env" ]; then
  cp "$APP_DIR/.env.example" "$APP_DIR/.env"
  echo "!! Создан $APP_DIR/.env. Впишите в него токен бота и chat id, затем: systemctl restart novo-site novo-bot"
fi
chown -R www-data:www-data "$APP_DIR"
chmod 600 "$APP_DIR/.env"

echo ">> Службы"
cat > /etc/systemd/system/novo-site.service <<UNIT
[Unit]
Description=Novo Tours site
After=network.target

[Service]
User=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
UNIT

cat > /etc/systemd/system/novo-bot.service <<UNIT
[Unit]
Description=Novo Tours Telegram bot
After=network.target

[Service]
User=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now novo-site novo-bot

echo ">> Nginx для $DOMAIN"
cat > /etc/nginx/sites-available/novo-tours <<NGINX
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    client_max_body_size 5m;

    location /static/ {
        alias $APP_DIR/static/;
        expires 7d;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX
ln -sf /etc/nginx/sites-available/novo-tours /etc/nginx/sites-enabled/novo-tours
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo ">> HTTPS (Let's Encrypt)"
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" --redirect || \
  echo "!! HTTPS не выпустился. Проверьте, что домен указывает на этот сервер, и повторите: certbot --nginx -d $DOMAIN -d www.$DOMAIN"

echo ">> Готово: https://$DOMAIN"
