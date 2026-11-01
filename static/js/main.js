(function () {
  var $ = function (id) { return document.getElementById(id); };
  var cards = [].slice.call(document.querySelectorAll('#grid .card'));
  var filter = '';

  function toast(m) {
    var t = $('toast'); t.textContent = m; t.classList.add('show');
    setTimeout(function () { t.classList.remove('show'); }, 3000);
  }

  function draw() {
    var q = $('q').value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c) {
      var ok = (!filter || c.dataset.type === filter) && (!q || c.dataset.text.indexOf(q) > -1);
      c.hidden = !ok; if (ok) shown++;
    });
    $('empty').hidden = shown > 0;
  }

  function setTab(f) {
    filter = f;
    [].forEach.call(document.querySelectorAll('.tab'), function (x) { x.classList.toggle('on', x.dataset.f === f); });
    draw();
  }

  $('tabs').addEventListener('click', function (e) {
    var b = e.target.closest('.tab'); if (b) setTab(b.dataset.f);
  });
  $('go').addEventListener('click', function () {
    setTab($('t').value); $('grid').scrollIntoView({ behavior: 'smooth' });
  });
  $('q').addEventListener('input', draw);

  // Окно заявки
  function openForm(tour) { $('fT').value = tour || ''; $('md').classList.add('show'); }
  function closeForm() { $('md').classList.remove('show'); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-tour]'); if (b) openForm(b.dataset.tour);
  });
  $('mx').addEventListener('click', closeForm);
  $('md').addEventListener('click', function (e) { if (e.target === this) closeForm(); });

  $('fS').addEventListener('click', function () {
    var n = $('fN').value.trim(), p = $('fP').value.trim(), t = $('fT').value.trim(), c = $('fC').value.trim();
    if (!n || !p) { toast('Укажите имя и телефон'); return; }
    var m = 'Здравствуйте! Хочу забронировать тур' + (t ? ': ' + t : '') + '.\nИмя: ' + n + '\nТелефон: ' + p + (c ? '\nКомментарий: ' + c : '');
    var a = document.createElement('a');
    a.href = 'https://t.me/GordeeffPhoto?text=' + encodeURIComponent(m);
    a.target = '_blank'; a.rel = 'noopener';
    document.body.appendChild(a); a.click(); a.remove();
    closeForm(); toast('Открываем Telegram — нажмите «Отправить»');
  });
})();
