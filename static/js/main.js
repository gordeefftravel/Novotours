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
    var btn = this;
    var body = { tour: $('fT').value, name: $('fN').value, phone: $('fP').value,
                 comment: $('fC').value, website: $('fW').value };
    if (!body.name.trim() || !body.phone.trim()) { toast('Укажите имя и телефон'); return; }
    btn.disabled = true;
    fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok && res.j.ok) {
          closeForm(); toast('Заявка отправлена! Мы скоро свяжемся с вами.');
          ['fN', 'fP', 'fC'].forEach(function (i) { $(i).value = ''; });
        } else { toast(res.j.error || 'Не удалось отправить заявку'); }
      })
      .catch(function () { toast('Нет связи. Позвоните нам или напишите в Telegram.'); })
      .then(function () { btn.disabled = false; });
  });
})();
