#!/usr/bin/env python3
"""Генератор статических страниц Novo Tours (только стандартная библиотека).

Запуск из корня репозитория:  python3 tools/build.py
Читает  data/countries/*.json, data/blog/*.json, data/reviews.json (необязательно)
Пишет   index.html, countries/, blog/, favorites/, 404.html, sitemap.xml, robots.txt, static/data/index.json
Результат коммитится в репозиторий, поэтому GitHub Pages работает без сборки.
Новая страна = новый JSON-файл в data/countries/ (схема: data/README.md). Код менять не нужно.
"""
import json, glob, os, html, datetime, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://novotours.ru"
TODAY = datetime.date(2026, 11, 25).isoformat()
SITE = "Novo Tours"

CONTS = ["Азия", "Европа", "Африка", "Ближний Восток", "Северная Америка", "Южная Америка", "Океания"]
TYPES = {"beach": "Пляжный отдых", "culture": "Культура и история", "city": "Города", "nature": "Природа и активный отдых",
         "family": "Семейный отдых", "gastro": "Гастрономия", "romantic": "Романтика"}
BUD = {1: "Бюджетно", 2: "Средний бюджет", 3: "Выше среднего", 4: "Премиум"}
SEASONS = [("Зима", [12, 1, 2]), ("Весна", [3, 4, 5]), ("Лето", [6, 7, 8]), ("Осень", [9, 10, 11])]

e = lambda s: html.escape(str(s), quote=True)


def load(pattern):
    out = []
    for f in sorted(glob.glob(pattern)):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        d["_file"] = f
        out.append(d)
    return out


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def img_tag(name, alt, cls="", lazy=True, w=None, h=None):
    """<picture> с WebP, если рядом лежит .webp."""
    base = os.path.splitext(name)[0]
    size = f' width="{w}" height="{h}"' if w and h else ""
    ld = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    tag = f'<img src="/static/img/{name}" alt="{e(alt)}"{c}{ld}{size}>'
    if os.path.exists(f"static/img/{base}.webp"):
        return f'<picture><source type="image/webp" srcset="/static/img/{base}.webp">{tag}</picture>'
    return tag


ICONS = {
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 018-2.8A4.5 4.5 0 0120 10c0 5.8-8 11-8 11z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "tg": '<svg viewBox="0 0 24 24"><path d="M21 4L3 11l6 2 2 6 3-4 5 4z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2 1a11 11 0 005 5l1-2 5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "chat": '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>',
    "card": '<svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/></svg>',
    "user": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/></svg>',
    "map": '<svg viewBox="0 0 24 24"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "plane": '<svg viewBox="0 0 24 24"><path d="M2 14l20-8-8 16-2-7z"/></svg>',
}
ic = lambda n, c="nv-ico": ICONS[n].replace("<svg ", f'<svg class="{c}" aria-hidden="true" ', 1)

NAV = [("/countries/", "Страны"), ("/#tours", "Горящие туры"), ("/blog/", "Журнал"), ("/new-year.html", "Новый год"),
       ("/favorites/", "Избранное"), ("/#contacts", "Контакты")]


def header(active=""):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == active else ""}>{t}</a>' for h, t in NAV)
    return (f'<a class="nv-skip" href="#main">К содержанию</a><header class="nv-header"><div class="nv-wrap">'
            f'<a class="nv-brand" href="/" aria-label="Novo Tours — главная"><img src="/static/img/logo-icon.png" alt="" width="62" height="42"><b>Novo<i>Tours</i></b></a>'
            f'<button class="nv-burger" aria-label="Меню" aria-expanded="false">{ic("menu", "")}</button>'
            f'<nav class="nv-nav" aria-label="Основная навигация">{links}<a class="nv-cta" href="#" data-nv-book="Подбор тура">Подобрать тур</a></nav></div></header>')


def footer(countries):
    cl = "".join(f'<li><a href="/countries/{c["slug"]}/">{e(c["name"])}</a></li>' for c in countries[:8])
    cl2 = "".join(f'<li><a href="/countries/{c["slug"]}/">{e(c["name"])}</a></li>' for c in countries[8:])
    return f'''<footer class="nv-footer" id="contacts"><div class="nv-wrap">
<div class="nv-fcols"><div><a class="nv-brand" href="/"><img src="/static/img/logo-icon.png" alt="" width="62" height="42" loading="lazy"><b>Novo<i>Tours</i></b></a>
<p>Туры из Санкт-Петербурга, экскурсии по России и индивидуальные маршруты. Discover the World.</p>
<p>г. Новоселье, ул. Невская, 15к1<br>Ежедневно 9:00–21:00 · <a href="https://yandex.ru/maps/?text=%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B5%D0%BB%D1%8C%D0%B5%2C%20%D0%9D%D0%B5%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%2015%D0%BA1" target="_blank" rel="noopener">на карте</a></p></div>
<div><h4>Страны</h4><ul>{cl}</ul></div><div><h4>&nbsp;</h4><ul>{cl2}<li><a href="/countries/"><b>Все страны →</b></a></li></ul></div>
<div><h4>Разделы</h4><ul><li><a href="/blog/">Nova Travel Journal</a></li><li><a href="/#tours">Горящие туры</a></li><li><a href="/hot-tours.html">Подборка горящих</a></li><li><a href="/new-year.html">Новый год</a></li><li><a href="/favorites/">Избранное</a></li><li><a href="#" onclick="document.getElementById('pol').showModal();return false">Конфиденциальность</a></li></ul></div></div>
<div class="nv-ct"><a href="https://t.me/Novotoursaibot" target="_blank" rel="noopener" data-g="ai">{ic("chat", "")}ИИ-менеджер</a><a href="tel:+79818820888" data-g="call">{ic("phone", "")}+7 981 882-08-88</a><a href="https://max.ru/u/f9LHodD0cOJ_UcgmDh1PoygO82yH6kYgnsktMBOxpq2aJs4omzDmRsvX6pQ" target="_blank" rel="noopener" data-g="max">{ic("chat", "")}Max</a><a href="https://t.me/GordeeffPhoto" target="_blank" rel="noopener" data-g="tg">{ic("tg", "")}Telegram</a><a href="mailto:Nowotours@gmail.com" data-g="mail">{ic("mail", "")}Nowotours@gmail.com</a></div>
<p class="nv-src" style="color:#8fb3bb">© 2026 Novo Tours. Цены и условия туров указаны ориентировочно и подтверждаются менеджером перед оплатой.</p></div></footer>
<div class="nv-mb"><button data-nv-book="Подбор тура">Подобрать тур</button><a href="tel:+79818820888">Позвонить</a><a href="https://t.me/GordeeffPhoto" target="_blank" rel="noopener">Telegram</a></div>'''


def dialogs():
    opts = "".join(f"<option>{o}</option>" for o in ["Не важно", "3–5 ночей", "6–8 ночей", "9–11 ночей", "12–14 ночей", "15+ ночей"])
    return f'''<dialog id="nvbk"><button class="x" onclick="nvbk.close()" aria-label="Закрыть">×</button>
<form autocomplete="on"><h3>Заявка на подбор тура</h3>
<div><label for="nb-t">Страна или тур</label><input id="nb-t" name="tour" placeholder="Например, Турция"></div>
<div class="g2"><div><label for="nb-f">Город вылета</label><input id="nb-f" name="from" value="Санкт-Петербург"></div><div><label for="nb-p">Туристов</label><input id="nb-p" name="pax" value="2"></div></div>
<div class="g2"><div><label for="nb-d">Желаемые даты</label><input id="nb-d" name="dates" placeholder="8–15 марта"></div><div><label for="nb-u">Продолжительность</label><select id="nb-u" name="dur">{opts}</select></div></div>
<div><label for="nb-b">Бюджет, ₽</label><input id="nb-b" name="budget" placeholder="например, до 150 000"></div>
<div><label for="nb-n">Ваше имя *</label><input id="nb-n" name="name" required autocomplete="name"></div>
<div><label for="nb-ph">Телефон *</label><input id="nb-ph" name="phone" type="tel" required autocomplete="tel" inputmode="tel" placeholder="+7"></div>
<div><label for="nb-c">Комментарий</label><textarea id="nb-c" name="comment" rows="2"></textarea></div>
<input class="hp" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="ck"><input type="checkbox" name="agree" required><span>Согласен на обработку персональных данных и с <a href="#" onclick="pol.showModal();return false">политикой конфиденциальности</a></span></label>
<button class="btn" type="submit">Отправить заявку</button></form>
<div class="ok"><h3>Спасибо!</h3><p class="okt">Заявка принята. Мы свяжемся с вами с 9:00 до 21:00.</p><button class="btn s" onclick="nvbk.close()">Закрыть</button></div></dialog>'''


POLICY = '''<dialog id="pol"><button class="x" onclick="pol.close()" aria-label="Закрыть">×</button><h3>Политика конфиденциальности</h3>
<p class="d">Мы собираем имя, телефон и данные о желаемой поездке только для подбора тура и связи с вами. Данные не передаются третьим лицам, кроме случаев, необходимых для оформления вашей поездки.</p>
<p class="d">Оператор данных: Novo Tours, г. Новоселье, ул. Невская, 15к1, Nowotours@gmail.com. <!-- TODO владельцу: добавить наименование юрлица/ИП, ИНН/ОГРН и согласовать текст с юристом --></p></dialog>'''

METRIKA = open("templates/_metrika.html", encoding="utf-8").read()


def page(title, desc, path, body, countries, *, og="/static/img/og-banner.jpg", jsonld=None, active="", head="", extra_dialogs=True, noindex=False):
    url = BASE + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in (jsonld or []))
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{SITE}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#00293b"><link rel="icon" href="/static/img/logo-icon.png">
<link rel="stylesheet" href="/static/css/nova.css">{head}{ld}{METRIKA}</head>
<body>{header(active)}<main id="main">{body}</main>{footer(countries)}{dialogs() if extra_dialogs else ""}{POLICY}
<script src="/static/js/nova.js" defer></script></body></html>'''


def fav_btn(key):
    return f'<button class="nv-fav" data-fav="{e(key)}" aria-pressed="false" aria-label="В избранное">{ICONS["heart"]}</button>'


def country_card(c):
    cover = c.get("img")
    ph = (img_tag(cover, f'{c["name"]} — {c["tagline"]}', w=640, h=480) if cover else "")
    noimg = "" if cover else " noimg"
    types = ",".join(c["types"])
    text = " ".join([c["name"], c["tagline"], " ".join(TYPES[t] for t in c["types"]), c.get("search", "")]).lower()
    return f'''<article class="nv-card nv-reveal" data-slug="{c["slug"]}" data-cont="{e(c["continent"])}" data-types="{types}" data-bud="{c["budget"]}" data-name="{e(c["name"])}" data-text="{e(text)}">
{fav_btn("c:" + c["slug"])}<a href="/countries/{c["slug"]}/" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;flex:1">
<div class="nv-ph{noimg}" style="--c1:{c.get("c1", "#0e9aa7")};--c2:{c.get("c2", "#f28c28")}">{ph}<span class="ttl">{e(c["name"])}</span></div>
<div class="nv-cb"><p>{e(c["tagline"])}</p><div class="nv-meta"><span>{e(c["best"])}</span>{"".join(f"<span>{TYPES[t]}</span>" for t in c["types"][:2])}<span>{BUD[c["budget"]]}</span></div></div></a></article>'''


def slug_sight(i):
    return f"s-{i + 1}"


def build_country(c, countries, posts):
    nm, sl = c["name"], c["slug"]
    p = c["practical"]
    # похожие
    rel = sorted([x for x in countries if x["slug"] != sl], key=lambda x: -(len(set(x["types"]) & set(c["types"])) * 2 + (x["continent"] == c["continent"])))[:3]
    idx = [x["slug"] for x in countries].index(sl)
    prev_c, next_c = countries[idx - 1], countries[(idx + 1) % len(countries)]
    rposts = [pp for pp in posts if sl in pp.get("countries", [])][:3]

    sights = ""
    for i, s in enumerate(c["sights"]):
        rows = "".join(f"<dt>{k}</dt><dd>{e(s[v])}</dd>" for k, v in
                       [("Где", "where"), ("Как добраться", "how"), ("Стоимость", "cost"), ("Когда лучше", "when")] if s.get(v))
        sights += (f'<article class="nv-sight nv-reveal" id="{slug_sight(i)}">{fav_btn(f"s:{sl}:{s["n"]}")}<span class="nv-pill" style="align-self:flex-start">{e(s["type"])}</span>'
                   f'<h3>{e(s["n"])}</h3><p>{e(s["d"])}</p><dl>{rows}</dl>'
                   f'<a href="{e(s["map"])}" target="_blank" rel="noopener" class="nv-src"><b>Показать на карте →</b></a></article>')

    names = [s["n"] for s in c["sights"]]
    colmap = [("top", "Топ мест", None), ("free", "Бесплатно", "free"), ("unusual", "Необычные места", "unusual"), ("photo", "Для фото", "photo"),
              ("family", "С детьми", "family"), ("romantic", "Романтика", "romantic"), ("fun", "Развлечения", "fun")]
    tabs, panels, first = "", "", True
    for key, label, ck in colmap:
        lst = [(n, "") for n in names[:10]] if key == "top" else [(x, "") if isinstance(x, str) else (x[0], x[1]) for x in c["collections"].get(ck, [])]
        if not lst:
            continue
        li = ""
        for n, note in lst:
            i = names.index(n) if n in names else None
            lab = f'<a href="#{slug_sight(i)}"><b>{e(n)}</b></a>' if i is not None else f"<b>{e(n)}</b>"
            li += f"<li>{lab}{(' — ' + e(note)) if note else ''}</li>"
        tabs += f'<button role="tab" class="{"on" if first else ""}" aria-selected="{str(first).lower()}">{label}</button>'
        panels += f'<div class="nv-panel{" on" if first else ""}"><ol class="nv-list">{li}</ol></div>' if key == "top" else f'<div class="nv-panel"><ul class="nv-list">{li}</ul></div>'
        first = False

    f = c["food"]
    dishes = "".join(f"<li><b>{e(a)}</b> — {e(b)}</li>" for a, b in f["dishes"])
    markets = "".join(f"<li><b>{e(a)}</b> — {e(b)}</li>" for a, b in f["markets"])
    places = ""
    if f.get("places"):
        places = "<h3 style='margin-top:14px'>Проверенные заведения</h3><ul class='nv-list'>" + "".join(
            f'<li><b>{e(x["n"])}</b>, {e(x["addr"])} — <a href="{e(x["map"])}" target="_blank" rel="noopener">карта</a></li>' for x in f["places"]) + "</ul>"
    else:
        places = '<div class="nv-warn">Конкретные рестораны, адреса и рейтинги мы публикуем только после ручной проверки по актуальным картам — «по памяти» их не указываем. Подборку заведений добавим в ближайшем обновлении.</div>'

    t = c["transport"]
    tr = "".join(f"<li><b>{lab}:</b> {e(t[k])}</li>" for lab, k in
                 [("Из аэропорта", "airport"), ("Общественный транспорт", "public"), ("Такси", "taxi"), ("Аренда авто", "car"), ("Поезда", "trains"), ("Автобусы", "buses")] if t.get(k))
    apps = "".join(f"<span class='nv-pill'>{e(a)}</span> " for a in t.get("apps", []))

    hacks = "".join(f"<li>{e(h)}</li>" for h in c["hacks"])

    vis_ok = p.get("visa_checked")
    vis_note = (f'<p class="nv-src">Проверено: {e(vis_ok)}.</p>' if vis_ok else
                '<div class="nv-warn">Правила въезда для граждан России меняются. Эти сведения общего характера и <b>не проверялись на дату публикации</b> — перед покупкой тура уточните условия на официальных сайтах или у менеджера.</div>')
    prow = [("Виза для граждан России", p["visa"]), ("Правила въезда и документы", p["entry"]), ("Валюта", p["currency"]), ("Язык", p["language"]),
            ("Часовой пояс", p["tz"]), ("Розетки", p["plugs"]), ("Связь и интернет", p["sim"]), ("Законы", p["laws"]), ("Традиции", p["traditions"]), ("Безопасность", p["safety"])]
    ptab = "".join(f"<tr><th scope='row' style='width:34%'>{a}</th><td>{e(b)}</td></tr>" for a, b in prow)
    srcs = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(tt)}</a>' for tt, u in p["sources"])

    w = c["weather"]
    wtab = "".join(f"<tr><td><b>{e(r[0])}</b></td><td>{e(r[1])}</td><td>{e(r[2])}</td><td>{e(r[3])}</td></tr>" for r in w["rows"])

    rt = ""
    rtabs = ""
    for j, d in enumerate(["3", "5", "7", "10", "14"]):
        r = c["routes"][d]
        steps = "".join(f"<li>{e(x)}</li>" for x in r["steps"])
        rtabs += f'<button role="tab" class="{"on" if j == 0 else ""}" aria-selected="{str(j == 0).lower()}">{d} дней</button>'
        rt += f'<div class="nv-panel nv-route{" on" if j == 0 else ""}"><ol>{steps}</ol><p class="nv-src"><b>Транспорт:</b> {e(r["transport"])}<br><b>Бюджет:</b> {e(r["budget"])}</p></div>'

    relcards = "".join(f'<a class="nv-tile" href="/countries/{x["slug"]}/" style="text-decoration:none"><h3>{e(x["name"])}</h3><p>{e(x["tagline"])}</p></a>' for x in rel)
    relposts = ""
    if rposts:
        relposts = (f'<section class="nv-sec"><div class="nv-wrap"><h2 class="nv-h2">Статьи по теме</h2><div class="nv-tiles">' +
                    "".join(f'<a class="nv-tile" href="/blog/{pp["slug"]}/" style="text-decoration:none"><h3>{e(pp["title"])}</h3><p>{e(pp["desc"])}</p></a>' for pp in rposts) + '</div></div></section>')
    jump = "".join(f'<option value="{x["slug"]}"{" selected" if x["slug"] == sl else ""}>{e(x["name"])}</option>' for x in countries)
    hero_bg = f"--hero:url(/static/img/{os.path.splitext(c['img'])[0]}.webp);" if c.get("img") and os.path.exists(f"static/img/{os.path.splitext(c['img'])[0]}.webp") else f"--hero:linear-gradient(135deg,{c.get('c1', '#0e9aa7')},{c.get('c2', '#f28c28')});"
    toc = "".join(f'<a href="#{i}">{l}</a>' for i, l in [("sights", "Что посмотреть"), ("where", "Куда сходить"), ("food", "Еда"), ("transport", "Транспорт"), ("hacks", "Лайфхаки"),
                                                       ("practical", "Практика"), ("weather", "Погода"), ("routes", "Маршруты"), ("tours", "Тур")])
    body = f'''<section class="nv-hero" style="{hero_bg}"><div class="nv-wrap"><div class="nv-bc"><a href="/">Главная</a> / <a href="/countries/">Страны</a> / {e(nm)}</div>
<h1>{e(nm)}</h1><p class="sub">{e(c["intro"])}</p>
<div class="facts"><span>Лучший сезон: {e(c["best"])}</span><span>{e(c["continent"])}</span><span>{BUD[c["budget"]]}</span></div>
<div class="acts"><button class="nv-btn" data-nv-book="{e(nm)}">Подобрать тур</button><button class="nv-btn ghost" data-share="{e(nm)} — путеводитель Novo Tours">Поделиться</button></div></div></section>
<nav class="nv-toc" aria-label="Разделы страницы"><div class="nv-wrap">{toc}</div></nav>

<section class="nv-sec" id="sights"><div class="nv-wrap"><div class="nv-eyebrow">Что посмотреть</div><h2 class="nv-h2">{e(nm)}: главные места</h2><p class="nv-lead">{e(c["sights_lead"])}</p><div class="nv-grid" style="grid-template-columns:repeat(auto-fill,minmax(310px,1fr))">{sights}</div>
<p class="nv-src" style="margin-top:14px">Стоимость входа и часы работы меняются — проверяйте на официальных сайтах объектов. Фотографии мест будут добавлены после загрузки собственных снимков.</p></div></section>

<section class="nv-sec alt" id="where"><div class="nv-wrap"><div class="nv-eyebrow">Куда сходить</div><h2 class="nv-h2">Подборки по настроению</h2><div class="nv-tabs" role="tablist" data-tabs="wp">{tabs}</div><div id="wp">{panels}</div></div></section>

<section class="nv-sec" id="food"><div class="nv-wrap"><div class="nv-eyebrow">Где вкусно поесть</div><h2 class="nv-h2">Гастрономический путеводитель</h2><p class="nv-lead">{e(f["cuisine"])}</p>
<div class="nv-cols"><div class="nv-box"><h3>Что попробовать</h3><ul class="nv-list">{dishes}</ul></div><div class="nv-box"><h3>Рынки и фуд-споты</h3><ul class="nv-list">{markets}</ul></div>
<div class="nv-box"><h3>Уличная еда и бюджет</h3><p>{e(f["street"])}</p><p><b>Районы:</b> {e(f["areas"])}</p><p><b>Средний чек:</b> {e(f["avg"])}</p></div></div>{places}</div></section>

<section class="nv-sec alt" id="transport"><div class="nv-wrap"><div class="nv-eyebrow">Как добраться и передвигаться</div><h2 class="nv-h2">Транспорт</h2>
<div class="nv-box"><ul class="nv-list">{tr}</ul><p><b>Полезные приложения:</b> {apps}</p><p class="nv-src">{e(t["cost"])}</p></div></div></section>

<section class="nv-sec" id="hacks"><div class="nv-wrap"><div class="nv-eyebrow">Лайфхаки</div><h2 class="nv-h2">Советы путешественнику</h2><div class="nv-box"><ul class="nv-list">{hacks}</ul></div></div></section>

<section class="nv-sec alt" id="practical"><div class="nv-wrap"><div class="nv-eyebrow">Практическая информация</div><h2 class="nv-h2">Перед поездкой</h2>{vis_note}
<div class="nv-scroll"><table class="nv-table"><tbody>{ptab}</tbody></table></div><p class="nv-src" style="margin-top:10px"><b>Официальные источники:</b> {srcs}. Дата редакции раздела: {TODAY}.</p></div></section>

<section class="nv-sec" id="weather"><div class="nv-wrap"><div class="nv-eyebrow">Погода и сезоны</div><h2 class="nv-h2">Когда ехать в {e(c.get("name_in", nm))}</h2><p class="nv-lead">{e(w["summary"])}</p>
<div class="nv-scroll"><table class="nv-table"><thead><tr><th>Период</th><th>Воздух, °C</th><th>Вода, °C</th><th>Что ожидать</th></tr></thead><tbody>{wtab}</tbody></table></div>
<p class="nv-src" style="margin-top:10px">Значения ориентировочные (климатические нормы), реальная погода может отличаться. <b>Когда выгоднее:</b> {e(w["cheap"])}</p></div></section>

<section class="nv-sec alt" id="routes"><div class="nv-wrap"><div class="nv-eyebrow">Готовые маршруты</div><h2 class="nv-h2">Маршруты на 3–14 дней</h2><div class="nv-tabs" role="tablist" data-tabs="rp">{rtabs}</div><div id="rp">{rt}</div></div></section>

<section class="nv-sec" id="tours"><div class="nv-wrap"><div class="nv-band"><h2>Готовы открыть эту страну?</h2><p>Расскажем про актуальные туры и реальные цены — без выдуманных предложений. Страна подставится в заявку автоматически.</p>
<button class="nv-btn" data-nv-book="{e(nm)}">Подобрать тур</button> <a class="nv-btn ghost" href="https://t.me/Novotoursaibot" target="_blank" rel="noopener">Спросить ИИ-менеджера</a></div></div></section>

<section class="nv-sec alt"><div class="nv-wrap"><h2 class="nv-h2">Похожие направления</h2><div class="nv-tiles">{relcards}</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:24px"><a class="nv-btn line" href="/countries/{prev_c["slug"]}/">← {e(prev_c["name"])}</a><a class="nv-btn line" href="/countries/{next_c["slug"]}/">{e(next_c["name"])} →</a>
<label style="margin:0;flex:1;min-width:200px">Быстрый переход<select onchange="location.href='/countries/'+this.value+'/'">{jump}</select></label></div></div></section>{relposts}'''
    ld = [{"@context": "https://schema.org", "@type": "TouristDestination", "name": nm, "description": c["meta"], "url": f"{BASE}/countries/{sl}/",
           "touristType": [TYPES[x] for x in c["types"]], "image": f"{BASE}/static/img/{c['img']}" if c.get("img") else f"{BASE}/static/img/og-banner.jpg"},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Страны", "item": BASE + "/countries/"},
              {"@type": "ListItem", "position": 3, "name": nm, "item": f"{BASE}/countries/{sl}/"}]}]
    og = f"/static/img/{c['img']}" if c.get("img") else "/static/img/og-banner.jpg"
    return page(c["title"], c["meta"], f"/countries/{sl}/", body, countries, og=og, jsonld=ld, active="/countries/")


def build_catalog(countries):
    cards = "".join(country_card(c) for c in countries)
    conts = "".join(f'<option value="{e(x)}">{x}</option>' for x in CONTS)
    types = "".join(f'<option value="{k}">{v}</option>' for k, v in TYPES.items())
    body = f'''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap"><div class="nv-bc"><a href="/">Главная</a> / Страны</div><h1>Каталог стран</h1>
<p class="sub">Путеводители по направлениям: что посмотреть, где поесть, как добраться и когда ехать. Выберите страну — и подберём тур из Санкт-Петербурга.</p></div></section>
<section class="nv-sec"><div class="nv-wrap">
<div class="nv-filters"><div><label for="catQ">Поиск по названию</label><input id="catQ" type="search" placeholder="Например, Таиланд" autocomplete="off"></div>
<div><label for="catCont">Регион</label><select id="catCont"><option value="">Все регионы</option>{conts}</select></div>
<div><label for="catType">Тип отдыха</label><select id="catType"><option value="">Любой</option>{types}</select></div>
<div><label for="catSort">Сортировка</label><select id="catSort"><option value="name">По алфавиту</option><option value="budget">Сначала бюджетнее</option><option value="budget-desc">Сначала дороже</option></select></div></div>
<div class="nv-chips"><button id="catFav" aria-label="Показать избранные страны">♥ Только избранное</button><span class="nv-src" style="align-self:center">Найдено стран: <b id="catCount">{len(countries)}</b></span></div>
<div class="nv-grid" id="catGrid">{cards}</div>
<div class="nv-empty" id="catEmpty"><p><b>По вашим условиям стран пока нет.</b></p><p>Каталог растёт — а пока подберём поездку индивидуально.</p><button class="nv-btn" data-nv-book="Подбор тура">Оставить заявку</button></div>
<p class="nv-src" style="margin-top:18px">Уровень бюджета — сравнительная оценка направления, а не цена тура. Актуальную стоимость рассчитает менеджер под ваши даты.</p></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Каталог стран — Novo Tours", "url": BASE + "/countries/"},
          {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/countries/{c['slug']}/", "name": c["name"]} for i, c in enumerate(countries)]}]
    return page("Каталог стран — путеводители и туры из Санкт-Петербурга | Novo Tours", "Каталог стран Novo Tours: Турция, Египет, Таиланд, ОАЭ, Вьетнам и другие. Что посмотреть, где поесть, когда ехать, как добраться.", "/countries/", body, countries, jsonld=ld, active="/countries/")


def fmt_date(s):
    y, m, d = map(int, s.split("-"))
    return f"{d} {['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'][m]} {y}"


BLOG_CATS = ["Советы путешественникам", "Необычные места", "Гастрономические путешествия", "Маршруты", "Бюджетные путешествия", "Пляжный отдых", "Самостоятельные путешествия", "Путешествия с детьми"]


BLOGJS = '''<script>(function(){var b=document.getElementById("blogCats"),g=[].slice.call(document.querySelectorAll("#blogGrid .nv-card"));b.addEventListener("click",function(ev){var t=ev.target.closest("button");if(!t)return;
[].forEach.call(b.children,function(x){x.classList.toggle("on",x===t)});var n=0;g.forEach(function(c){var ok=!t.dataset.cat||c.dataset.cat===t.dataset.cat;c.hidden=!ok;if(ok)n++});document.getElementById("blogEmpty").style.display=n?"none":"block"})})();</script>'''


def build_blog(posts, countries):
    cname = {c["slug"]: c["name"] for c in countries}
    cats = "".join(f'<button data-cat="{e(x)}">{x}</button>' for x in BLOG_CATS)
    cards = ""
    for p in posts:
        cards += (f'<a class="nv-card nv-reveal" href="/blog/{p["slug"]}/" data-cat="{e(p["category"])}"><div class="nv-ph" style="--c1:{p.get("c1", "#0e9aa7")};--c2:{p.get("c2", "#f28c28")};aspect-ratio:16/9">'
                  f'{img_tag(p["cover"], p["title"], w=640, h=360) if p.get("cover") else ""}<span class="ttl" style="font-size:22px">{e(p["category"])}</span></div>'
                  f'<div class="nv-cb"><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><div class="nv-meta"><span>{fmt_date(p["published"])}</span></div></div></a>')
    body = f'''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap"><div class="nv-bc"><a href="/">Главная</a> / Журнал</div><h1>Nova Travel Journal</h1><p class="sub">Советы, маршруты и идеи для путешествий — без воды и выдуманных цен.</p></div></section>
<section class="nv-sec"><div class="nv-wrap"><div class="nv-chips" id="blogCats"><button class="on" data-cat="">Все</button>{cats}</div>
<div class="nv-grid" id="blogGrid">{cards}</div><div class="nv-empty" id="blogEmpty">В этой рубрике пока нет статей — скоро появятся.</div></div></section>
{BLOGJS}'''
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Nova Travel Journal", "url": BASE + "/blog/"}]
    return page("Nova Travel Journal — журнал путешествий | Novo Tours", "Журнал Novo Tours: советы путешественникам, маршруты, бюджетные и самостоятельные поездки, путешествия с детьми.", "/blog/", body, countries, jsonld=ld, active="/blog/")


def build_post(p, posts, countries):
    cname = {c["slug"]: c["name"] for c in countries}
    body_html = "".join(f"<h2>{e(s['h'])}</h2>" + "".join(f"<p>{e(x)}</p>" for x in s["p"]) for s in p["sections"])
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in p.get("links", []))
    rc = "".join(f'<a class="nv-pill" href="/countries/{s}/" style="text-decoration:none">{e(cname[s])}</a> ' for s in p.get("countries", []) if s in cname)
    first = (p.get("countries") or [""])[0]
    cta_name = cname.get(first, "Подбор тура")
    others = [x for x in posts if x["slug"] != p["slug"]][:3]
    more = "".join(f'<a class="nv-tile" href="/blog/{x["slug"]}/" style="text-decoration:none"><h3>{e(x["title"])}</h3><p>{e(x["desc"])}</p></a>' for x in others)
    body = f'''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap"><div class="nv-bc"><a href="/">Главная</a> / <a href="/blog/">Журнал</a></div><div class="nv-eyebrow" style="color:#ffb454">{e(p["category"])}</div><h1 style="font-size:clamp(30px,5vw,52px)">{e(p["title"])}</h1>
<p class="sub">{e(p["desc"])}</p><div class="facts"><span>Опубликовано: {fmt_date(p["published"])}</span><span>Обновлено: {fmt_date(p["updated"])}</span></div></div></section>
<section class="nv-sec"><div class="nv-wrap"><article class="nv-post">{body_html}
{('<h2>Полезные ссылки</h2><ul class="nv-list">' + links + '</ul>') if links else ''}
{('<h2>Связанные страны</h2><p>' + rc + '</p>') if rc else ''}
<div class="nv-band" style="margin-top:32px"><h2>Хотите так же?</h2><p>Подберём тур под ваши даты и бюджет.</p><button class="nv-btn" data-nv-book="{e(cta_name)}">Подобрать тур</button></div>
<div class="nv-share" style="margin-top:18px"><button class="nv-btn line" data-share="{e(p["title"])}">Поделиться статьёй</button></div></article></div></section>
<section class="nv-sec alt"><div class="nv-wrap"><h2 class="nv-h2">Читайте также</h2><div class="nv-tiles">{more}</div></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "datePublished": p["published"], "dateModified": p["updated"],
           "author": {"@type": "Organization", "name": SITE}, "publisher": {"@type": "Organization", "name": SITE, "logo": {"@type": "ImageObject", "url": BASE + "/static/img/logo-icon.png"}},
           "mainEntityOfPage": f"{BASE}/blog/{p['slug']}/", "image": BASE + "/static/img/og-banner.jpg"}]
    return page(p["title"] + " | Novo Tours", p["desc"], f"/blog/{p['slug']}/", body, countries, jsonld=ld, active="/blog/")


def build_home(countries, posts, reviews):
    pop = [c for c in countries if c.get("popular")][:6]
    rest = [c for c in countries if c not in pop]
    pcards = "".join(country_card(c) for c in pop)
    more = "".join(f'<a class="nv-tile" href="/countries/{c["slug"]}/" style="text-decoration:none"><h3>{e(c["name"])}</h3><p>{e(c["tagline"])}</p></a>' for c in rest)
    seas = ""
    for name, months in SEASONS:
        pick = [c for c in countries if any(m in c["months"] for m in months)]
        pick.sort(key=lambda c: -len(set(months) & set(c["months"])))
        seas += (f'<div class="nv-tile"><h3>{name}</h3><p>' + ", ".join(f'<a href="/countries/{c["slug"]}/" style="color:var(--td);font-weight:700;text-decoration:none">{e(c["name"])}</a>' for c in pick[:4]) + '</p></div>')
    exp = "".join(f'<div class="nv-tile"><h3>{e(c["sights"][0]["n"])}</h3><p>{e(c["name"])} · {e(c["sights"][0]["d"])}</p><a href="/countries/{c["slug"]}/#sights">Подробнее →</a></div>' for c in rest[:6])
    unu = ""
    for c in countries:
        u = c["collections"].get("unusual", [])
        if u and len(unu.split("nv-tile")) <= 6:
            n = u[0] if isinstance(u[0], str) else u[0][0]
            unu += f'<div class="nv-tile"><h3>{e(n)}</h3><p>{e(c["name"])}</p><a href="/countries/{c["slug"]}/#where">Все необычные места →</a></div>'
    tips = "".join(f'<a class="nv-tile" href="/blog/{p["slug"]}/" style="text-decoration:none"><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p></a>' for p in posts[:3])
    pick_opts = "".join(f'<option value="{e(c["name"])}" data-slug="{c["slug"]}">{e(c["name"])}</option>' for c in countries)
    dur = "".join(f"<option>{o}</option>" for o in ["Не важно", "3–5 ночей", "6–8 ночей", "9–11 ночей", "12–14 ночей", "15+ ночей"])
    if reviews:
        rv = "".join(f'<figure class="nv-tile" style="margin:0"><blockquote style="margin:0 0 10px">{e(r["text"])}</blockquote><figcaption class="nv-src"><b>{e(r["name"])}</b>{(" · " + e(r["trip"])) if r.get("trip") else ""}</figcaption></figure>' for r in reviews)
        reviews_html = f'<section class="nv-sec alt"><div class="nv-wrap"><h2 class="nv-h2">Отзывы клиентов</h2><div class="nv-tiles">{rv}</div></div></section>'
    else:
        reviews_html = ""
    ben = [("check", "Условия отмены", "Для ряда туров есть бесплатная отмена. Условия зависят от тура — расскажем до оплаты."), ("card", "Оплата картой", "Оплатите тур банковской картой."),
           ("user", "Помощь менеджера", "Подберём тур, ответим на вопросы и поможем с бронированием."), ("map", "Свой маршрут", "Соберём индивидуальный тур под ваши даты и бюджет."),
           ("clock", "Каждый день 9–21", "Офис в Новоселье работает ежедневно; быстрее всего отвечаем в Telegram и Max."), ("plane", "Вылет из Санкт-Петербурга", "Все туры на сайте — из Санкт-Петербурга; другой город укажите в заявке.")]
    bt = "".join(f'<div class="nv-tile nv-reveal">{ic(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in ben)
    tours = open("templates/_tours.html", encoding="utf-8").read()
    filters = '''<form class="nv-filters" id="sf" onsubmit="return false" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
<div><label for="fc">Куда</label><select id="fc"><option value="">Любое направление</option></select></div>
<div><label for="ft">Тип</label><select id="ft"><option value="">Любой</option><option value="abroad">Зарубежные туры</option><option value="russia">Экскурсии по России</option><option value="custom">Индивидуальные</option></select></div>
<div><label for="fm">Когда</label><select id="fm"><option value="">Любой месяц</option><option value="11">Ноябрь</option><option value="12">Декабрь</option></select></div>
<div><label for="fb">Бюджет до, ₽</label><input id="fb" type="number" min="0" step="1000" inputmode="numeric" placeholder="любой"></div>
<div><label for="fp">Туристов</label><select id="fp"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>
<div style="align-self:end"><button class="btn" style="width:100%" id="go">Найти туры</button></div></form>'''
    tours = tours.replace('<div class="chips" id="chips">', filters + '<div class="chips" id="chips">', 1)
    script = open("templates/_legacy_script.js", encoding="utf-8").read()
    dlg = open("templates/_legacy_dialogs.html", encoding="utf-8").read()
    faq = '''<details><summary>Как оплатить тур?</summary><p>Банковской картой. Порядок оплаты менеджер объяснит при оформлении.</p></details>
<details><summary>Можно ли отменить поездку?</summary><p>Условия отмены зависят от конкретного тура. Уточните их у менеджера до оплаты.</p></details>
<details><summary>Можно ли тур не из Санкт-Петербурга?</summary><p>Все туры на сайте — из Санкт-Петербурга. Если нужен другой город вылета, напишите в заявке.</p></details>
<details><summary>Вы собираете индивидуальные туры?</summary><p>Да: подберём маршрут под даты, бюджет и состав группы — от выходных в области до дальних стран.</p></details>
<details><summary>Как быстро с вами свяжутся?</summary><p>Офис работает ежедневно с 9:00 до 21:00. Быстрее всего ответим в Telegram или Max.</p></details>'''
    body = f'''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap">
<div class="nv-eyebrow" style="color:#ffb454">Novo Tours · Discover the World</div><h1>Мир ближе, чем кажется</h1>
<p class="sub">Путешествия и открытия: путеводители по странам, горящие туры из Санкт-Петербурга и маршруты, собранные под вас.</p>
<div class="acts"><a class="nv-btn" href="#tours">Найти путешествие</a><a class="nv-btn ghost" href="/countries/">Исследовать страны</a></div>
<form class="nv-pick" id="pick" autocomplete="off"><div><label for="pk-c">Страна</label><select id="pk-c" name="country"><option value="">Любая</option>{pick_opts}</select></div>
<div><label for="pk-f">Город вылета</label><input id="pk-f" name="from" value="Санкт-Петербург"></div><div><label for="pk-d">Дата</label><input id="pk-d" name="date" placeholder="например, март"></div>
<div><label for="pk-p">Туристов</label><select id="pk-p" name="pax"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>
<div><label for="pk-u">Продолжительность</label><select id="pk-u" name="dur">{dur}</select></div><div><label for="pk-b">Бюджет, ₽</label><input id="pk-b" name="budget" placeholder="до 150 000"></div>
<button class="nv-btn go" type="submit">Подобрать тур</button></form></div></section>

<section class="nv-sec"><div class="nv-wrap"><div class="nv-eyebrow">Популярные направления</div><h2 class="nv-h2">Куда летят чаще всего</h2><p class="nv-lead">Путеводители с маршрутами, сезонами и практической информацией.</p><div class="nv-grid">{pcards}</div></div></section>

<section class="nv-sec alt"><div class="nv-wrap">{tours}</div></section>

<section class="nv-sec"><div class="nv-wrap"><div class="nv-eyebrow">Страны, которые стоит посетить</div><h2 class="nv-h2">Ещё идеи</h2><div class="nv-tiles">{more}</div><p style="margin-top:20px"><a class="nv-btn line" href="/countries/">Весь каталог стран</a></p></div></section>

<section class="nv-sec alt"><div class="nv-wrap"><div class="nv-eyebrow">По сезонам</div><h2 class="nv-h2">Идеи для путешествий по сезонам</h2><p class="nv-lead">Страны сгруппированы по лучшим месяцам для поездки.</p><div class="nv-tiles">{seas}</div></div></section>

<section class="nv-sec"><div class="nv-wrap nv-split"><div><div class="nv-eyebrow">Экскурсии и впечатления</div><h2 class="nv-h2">Что увидеть своими глазами</h2><p class="nv-lead">Главные места направлений — с описанием, дорогой и лучшим временем визита.</p></div><div class="nv-tiles" style="grid-template-columns:1fr 1fr">{exp}</div></div></section>

<section class="nv-sec alt"><div class="nv-wrap"><div class="nv-eyebrow">Необычные места мира</div><h2 class="nv-h2">Там, где нет толп</h2><div class="nv-tiles">{unu}</div></div></section>

<section class="nv-sec"><div class="nv-wrap"><div class="nv-eyebrow">Полезные советы</div><h2 class="nv-h2">Nova Travel Journal</h2><div class="nv-tiles">{tips}</div><p style="margin-top:20px"><a class="nv-btn line" href="/blog/">Все статьи</a></p></div></section>

<section class="nv-sec alt"><div class="nv-wrap"><div class="nv-eyebrow">Преимущества</div><h2 class="nv-h2">Почему Novo Tours</h2><div class="nv-tiles">{bt}</div></div></section>
{reviews_html}
<section class="nv-sec" id="faq"><div class="nv-wrap"><h2 class="nv-h2">Вопросы и ответы</h2><div style="margin-top:14px">{faq}</div></div></section>

<section class="nv-sec"><div class="nv-wrap"><div class="nv-band"><h2>Не нашли подходящий тур?</h2><p>Расскажите, куда хотите, — подберём вариант.</p><button class="nv-btn" data-book="Подбор тура">Оставить заявку</button> <a class="nv-btn ghost" href="https://t.me/Novotoursaibot" target="_blank" rel="noopener" data-g="ai">Спросить ИИ-менеджера</a></div></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "TravelAgency", "name": "Novo Tours", "url": BASE + "/", "email": "Nowotours@gmail.com", "telephone": "+79818820888",
           "address": {"@type": "PostalAddress", "addressLocality": "Новоселье", "streetAddress": "ул. Невская, 15к1", "addressCountry": "RU"}, "openingHours": "Mo-Su 09:00-21:00", "image": BASE + "/static/img/og-banner.jpg"},
          {"@context": "https://schema.org", "@type": "WebSite", "name": "Novo Tours", "url": BASE + "/"}]
    html_out = page("Novo Tours — туры из Санкт-Петербурга, путеводители по странам", "Мир ближе, чем кажется: путеводители по странам, горящие туры из Санкт-Петербурга, экскурсии и индивидуальные маршруты. Новоселье, ул. Невская, 15к1. Ежедневно 9:00–21:00.",
                    "/", body, countries, jsonld=ld, active="/", extra_dialogs=False)
    # на главной остаётся прежняя заявка (id=bk) + её скрипт без изменений; виджет подбора открывает её через NV.openBooking
    html_out = html_out.replace("<script src=\"/static/js/nova.js\" defer></script>", dlg + "\n<script>\n" + script + "\n</script>\n<script src=\"/static/js/nova.js\" defer></script>")
    html_out = html_out.replace(POLICY, "")  # политика уже есть в legacy-диалогах
    return html_out


def build_misc(countries, posts):
    # избранное
    body = '''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap"><h1>Избранное</h1><p class="sub">Страны и места, которые вы сохранили. Хранятся только в вашем браузере — регистрация не нужна.</p></div></section>
<section class="nv-sec"><div class="nv-wrap"><div id="favList"><noscript>Для избранного нужен JavaScript.</noscript></div></div></section>'''
    write("favorites/index.html", page("Избранное — Novo Tours", "Ваши сохранённые страны и места.", "/favorites/", body, countries, active="/favorites/", noindex=True))
    nf = '''<section class="nv-hero fx" style="--hero:url(/static/img/hero-crop.webp)"><div class="nv-wrap"><h1>Страница не найдена</h1><p class="sub">Возможно, ссылка устарела. Загляните в каталог стран или оставьте заявку — подберём поездку.</p>
<div class="acts"><a class="nv-btn" href="/countries/">Каталог стран</a><a class="nv-btn ghost" href="/">На главную</a></div></div></section>'''
    write("404.html", page("Страница не найдена — Novo Tours", "Страница не найдена.", "/404.html", nf, countries, noindex=True))
    urls = [("/", "1.0"), ("/countries/", "0.9"), ("/blog/", "0.7"), ("/hot-tours.html", "0.6"), ("/new-year.html", "0.6")]
    urls += [(f"/countries/{c['slug']}/", "0.8") for c in countries] + [(f"/blog/{p['slug']}/", "0.6") for p in posts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /favorites/\n\nSitemap: {BASE}/sitemap.xml\n")
    write("static/data/index.json", json.dumps({"countries": [{"slug": c["slug"], "name": c["name"], "tagline": c["tagline"], "sights": [s["n"] for s in c["sights"]]} for c in countries]}, ensure_ascii=False))


def main():
    countries = load("data/countries/*.json")
    order = ["turkey", "egypt", "thailand", "uae", "vietnam", "china", "japan", "indonesia", "sri-lanka", "maldives", "india", "italy", "france", "spain", "georgia"]
    countries.sort(key=lambda c: order.index(c["slug"]) if c["slug"] in order else 99)
    posts = load("data/blog/*.json")
    posts.sort(key=lambda p: p["published"], reverse=True)
    reviews = json.load(open("data/reviews.json", encoding="utf-8")) if os.path.exists("data/reviews.json") else []
    errs = []
    for c in countries:
        for k in ("slug", "name", "continent", "types", "budget", "best", "months", "tagline", "intro", "title", "meta", "sights", "collections", "food", "transport", "hacks", "practical", "weather", "routes"):
            if k not in c:
                errs.append(f'{c["_file"]}: нет поля {k}')
        if c.get("continent") not in CONTS:
            errs.append(f'{c["slug"]}: континент {c.get("continent")}')
        for t in c.get("types", []):
            if t not in TYPES:
                errs.append(f'{c["slug"]}: тип {t}')
    if errs:
        print("\n".join(errs)); sys.exit(1)
    for c in countries:
        write(f"countries/{c['slug']}/index.html", build_country(c, countries, posts))
    write("countries/index.html", build_catalog(countries))
    write("blog/index.html", build_blog(posts, countries))
    for p in posts:
        write(f"blog/{p['slug']}/index.html", build_post(p, posts, countries))
    write("index.html", build_home(countries, posts, reviews))
    build_misc(countries, posts)
    print(f"OK: стран {len(countries)}, статей {len(posts)}")


if __name__ == "__main__":
    main()
