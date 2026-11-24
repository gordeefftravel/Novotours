(function () {
  var slug = location.pathname.replace(/\/+$/, "").split("/").pop();
  var country = (window.COUNTRIES || []).find(function (item) { return item.slug === slug; });
  if (!country) {
    document.getElementById("country-content").innerHTML = '<section class="content wrap"><h1>Страна не найдена</h1><p><a class="button" href="../">Вернуться к каталогу стран</a></p></section>';
    return;
  }
  document.title = country.name + " — путеводитель и туры | Novo Tours";
  var description = document.querySelector('meta[name="description"]');
  if (description) description.content = country.description + " Практическая информация, маршруты и подбор туров от Novo Tours.";
  var canonical = document.querySelector('link[rel="canonical"]');
  if (canonical) canonical.href = "https://novotours.ru/countries/" + country.slug + "/";
  var ogTitle = document.querySelector('meta[property="og:title"]');
  var ogUrl = document.querySelector('meta[property="og:url"]');
  var ogImage = document.querySelector('meta[property="og:image"]');
  if (ogTitle) ogTitle.content = country.name + " — путеводитель Novo Tours";
  if (ogUrl) ogUrl.content = "https://novotours.ru/countries/" + country.slug + "/";
  if (ogImage) ogImage.content = "https://novotours.ru/static/img/" + country.image;
  var esc = function (value) {
    return String(value).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; });
  };
  var related = (window.COUNTRIES || []).filter(function (item) { return item.region === country.region && item.slug !== country.slug; }).slice(0, 3);
  document.getElementById("country-content").innerHTML =
    '<section class="country-hero" style="background-image:linear-gradient(90deg,#00293bf2,#00293b80),url(../../static/img/' + esc(country.image) + ')">' +
      '<div class="wrap"><p class="eyebrow">' + esc(country.region) + ' · ' + esc(country.rest) + '</p><h1>' + esc(country.name) + '</h1><p>' + esc(country.description) + '</p>' +
      '<div class="hero-actions"><a class="button" href="../../hot-tours.html">Посмотреть туры</a><button class="button button-light" type="button" onclick="document.getElementById(\'country-request\').scrollIntoView({behavior:\'smooth\'})">Подобрать тур</button></div></div></section>' +
    '<main class="wrap country-page"><section><div class="bar"><h2>Почему стоит посетить</h2></div><div class="info-grid"><article><h3>Особенности</h3><p>' + esc(country.description) + ' Формат поездки лучше выбирать с учётом сезона и вашего типа отдыха.</p></article><article><h3>Лучший сезон</h3><p>' + esc(country.season) + '</p></article><article><h3>Что посмотреть</h3><p>' + country.highlights.map(esc).join("<br>") + '</p></article></div></section>' +
    '<section><div class="bar"><h2>Маршруты для первого знакомства</h2></div><div class="route-grid"><article><b>3 дня</b><p>Ключевой город, одна обзорная программа и свободный вечер.</p></article><article><b>5 дней</b><p>Основные достопримечательности и один тематический день.</p></article><article><b>7–10 дней</b><p>Город, природа и одна дополнительная локация с переносом багажа.</p></article></div></section>' +
    '<section><div class="bar"><h2>Практическая информация</h2></div><div class="info-grid"><article><h3>Въезд и документы</h3><p>Актуальные визовые правила для граждан России проверяйте перед поездкой на официальном портале консульства или МИД РФ.</p><a href="https://mid.ru/ru/foreign_policy/international_contracts/international_contracts/travel_note/" target="_blank" rel="noopener">Официальная справка МИД РФ</a></article><article><h3>Транспорт</h3><p>Маршрут из аэропорта, местные билеты и стоимость поездок меняются. Сверяйте расписание и тарифы на сайтах перевозчиков.</p></article><article><h3>Советы</h3><p>Бронируйте популярные объекты заранее, используйте официальные карты и сохраняйте копии документов вне смартфона.</p></article></div></section>' +
    '<section><div class="bar"><h2>Лайфхаки путешественника</h2></div><div class="info-grid"><article><h3>Бюджет</h3><p>Сравните проживание, перелёт и обязательные экскурсии; цены на рейс и тур меняются.</p></article><article><h3>Еда</h3><p>Ищите районы и рынки с местными заведениями. Конкретные рестораны и адреса проверяйте перед визитом.</p></article><article><h3>Безопасность</h3><p>Пользуйтесь официальными такси или проверенными приложениями, избегайте нелицензионных обменников.</p></article></div></section>' +
    '<section id="country-request" class="request"><div><h2>Подобрать тур в ' + esc(country.name) + '</h2><p>Менеджер уточнит даты вылета, бюджет и актуальные предложения.</p></div><div class="request-actions"><a class="button" href="../../hot-tours.html">Смотреть актуальные туры</a><a class="button button-light" href="tel:+79818820888">Позвонить</a></div></section>' +
    '<section><div class="bar"><h2>Похожие направления</h2></div><div class="route-grid">' + related.map(function (item) { return '<a class="text-card" href="../' + item.slug + '/"><b>' + esc(item.name) + '</b><span>' + esc(item.rest) + '</span></a>'; }).join("") + '</div></section></main>';
  var schema = document.getElementById("country-schema");
  if (schema) schema.text = JSON.stringify({"@context":"https://schema.org","@type":"TouristDestination","name":country.name,"description":country.description,"url":"https://novotours.ru/countries/" + country.slug + "/"});
}());
