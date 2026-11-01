# Сайт Novo Tours для GitHub Pages

Обычный статический сайт: `index.html` + папка `static`. Python и бот не нужны.
Форма заявки открывает Telegram (@GordeeffPhoto) с готовым сообщением.

## Как выложить на GitHub Pages
1. Зарегистрируйтесь на github.com и нажмите **New repository**. Назовите, например, `novo-tours`, выберите **Public**.
2. Нажмите **uploading an existing file** и перетащите **содержимое** этой папки (index.html, папку static и файл .nojekyll), затем **Commit changes**.
3. Откройте **Settings → Pages**. В разделе Source выберите **Deploy from a branch**, ветка **main**, папка **/(root)**, нажмите Save.
4. Через 1–2 минуты сайт откроется по адресу `https://ВАШ-ЛОГИН.github.io/novo-tours/`.

## Свой домен
1. В **Settings → Pages → Custom domain** впишите домен (например, `novo.tours`) и сохраните.
2. У регистратора домена создайте записи **A** для `@` на адреса GitHub: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, а для `www` запись **CNAME** на `ВАШ-ЛОГИН.github.io`. Актуальные адреса проверьте в справке GitHub Pages.
3. Когда домен подтвердится, включите **Enforce HTTPS**.

## Как менять туры
Тексты и цены правятся прямо в `index.html` (поиск по названию тура). Афиши лежат в `static/img/`.
