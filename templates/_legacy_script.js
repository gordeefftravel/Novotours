/* НАСТРОЙКИ: WORKER_URL — адрес бесплатного Cloudflare Worker, который шлёт заявку в Telegram (токен хранится в Worker). Если пусто — заявка отправляется через открытие Telegram. YM_ID — номер счётчика Яндекс Метрики. */
var WORKER_URL="https://novotours-bb57.nowotours.workers.dev",YM_ID="114045220",TG="GordeeffPhoto";
var T=[
{id:"villa-sonata",n:"Villa Sonata",t:"abroad",c:"Турция",dt:"1–8 декабря 2026 · 7 ночей",k:"2026-12-01",m:[12],img:"alanya.jpg",b:"3★ · без питания",p:65724,u:"за 2 взрослых",d:"Аланья · номер Standard Room.",src:"https://sletat.ru/hot-tour/saint_petersburg/turkey/"},
{id:"kleopatra-bavyera",n:"Kleopatra Bavyera",t:"abroad",c:"Турция",dt:"27 ноября – 4 декабря 2026 · 7 ночей",k:"2026-11-27",m:[11],img:"alanya.jpg",b:"Завтрак",p:68569,u:"за 2 взрослых",d:"Аланья · Eco Room без кондиционера · 2-я линия, песок.",src:"https://sletat.ru/hot-tour/saint_petersburg/turkey/"},
{id:"lola-hotel",n:"The Lola Hotel",t:"abroad",c:"Турция",dt:"20–26 ноября 2026 · 6 ночей",k:"2026-11-20",m:[11],img:"istanbul.jpg",b:"Без питания",p:71225,u:"за 2 взрослых",d:"Стамбул, Фатих · номер Economy Double.",src:"https://sletat.ru/hot-tour/saint_petersburg/turkey/"},
{id:"may-hotel",n:"May",t:"abroad",c:"Турция",dt:"30 ноября – 4 декабря 2026 · 4 ночи",k:"2026-11-30",m:[11],img:"istanbul.jpg",b:"4 ночи",p:71293,u:"за 2 взрослых",d:"Стамбул · номер Standard · без питания.",src:"https://sletat.ru/hot-tour/saint_petersburg/turkey/"},
{id:"new-badawia",n:"New Badawia Sharm Resort",t:"abroad",c:"Египет",dt:"29 ноября – 8 декабря 2026 · 9 ночей",k:"2026-11-29",m:[11],img:"egypt.jpg",b:"Всё включено",p:80784,u:"за 2 взрослых",d:"Хадаба · Standard Garden View Room · 3-я линия.",src:"https://sletat.ru/hot-tour/saint_petersburg/egypt/"},
{id:"dahab-plaza",n:"Dahab Plaza Hotel",t:"abroad",c:"Египет",dt:"29 ноября – 7 декабря 2026 · 8 ночей",k:"2026-11-29",m:[11],img:"egypt.jpg",b:"Без питания",p:84223,u:"за 2 взрослых",d:"Дахаб · номер Deluxe Room · 2-я линия.",src:"https://sletat.ru/hot-tour/saint_petersburg/egypt/"},
{id:"sharm-hills",n:"Sharm Hills Resort",t:"abroad",c:"Египет",dt:"30 ноября – 7 декабря 2026 · 7 ночей",k:"2026-11-30",m:[11],img:"egypt.jpg",b:"Без питания",p:86154,u:"за 2 взрослых",d:"Шарм-эль-Шейх · номер Deluxe Twin Room.",src:"https://sletat.ru/hot-tour/saint_petersburg/egypt/"},
{id:"uni-sharm",n:"Uni Sharm Aqua Park",t:"abroad",c:"Египет",dt:"30 ноября – 7 декабря 2026 · 7 ночей",k:"2026-11-30",m:[11],img:"egypt.jpg",b:"Завтрак и ужин",p:86817,u:"за 2 взрослых",d:"Хадаба · Standard Room · 3-я линия.",src:"https://sletat.ru/hot-tour/saint_petersburg/egypt/"},
{id:"sand-beach",n:"The Sand Beach",t:"abroad",c:"Таиланд",dt:"21–27 ноября 2026 · 6 ночей",k:"2026-11-21",m:[11],img:"thailand.jpg",b:"Завтрак · первая линия",p:127756,u:"за 2 взрослых",d:"Пляж Джомтьен · номер Deluxe · 3★.",src:"https://sletat.ru/hot-tour/saint_petersburg/thailand/"},
{id:"mariek",n:"Мариэк",t:"abroad",c:"Абхазия",dt:"25 ноября – 2 декабря 2026 · 7 ночей",k:"2026-11-25",m:[11],img:"abhazia.jpg",imgMode:"country",b:"8,9 · 2-я линия",p:28164,u:"за 2 взрослых",d:"Сухум · без питания · 2-местный номер с отдельным входом.",src:"https://sletat.ru/hot-tour/saint_petersburg/abkhazia/"},
{id:"arda",n:"Arda",t:"abroad",c:"Абхазия",dt:"28 ноября – 2 декабря 2026 · 4 ночи",k:"2026-11-28",m:[11],img:"abhazia.jpg",imgMode:"country",b:"Завтрак",p:29160,u:"за 2 взрослых",d:"Гагра · стандартный 2-местный номер без балкона · 2-я линия.",src:"https://sletat.ru/hot-tour/saint_petersburg/abkhazia/"},
{id:"grace-black-sea",n:"Grace Black Sea",t:"abroad",c:"Абхазия",dt:"25 ноября – 2 декабря 2026 · 7 ночей",k:"2026-11-25",m:[11],img:"abhazia.jpg",imgMode:"country",b:"Рейтинг 9 · первая линия",p:33222,u:"за 2 взрослых",d:"Сухум · без питания · стандартный номер с балконом.",src:"https://sletat.ru/hot-tour/saint_petersburg/abkhazia/"},
{id:"crystal-plaza",n:"Crystal Plaza Hotel",t:"abroad",c:"ОАЭ",dt:"22–28 ноября 2026 · 6 ночей",k:"2026-11-22",m:[11],img:"dubai.jpg",imgMode:"country",b:"Завтрак",p:85392,u:"за 2 взрослых",d:"Шарджа · номер Standard.",src:"https://sletat.ru/hot-tour/saint_petersburg/uae/"},
{id:"red-castle",n:"Red Castle Hotel",t:"abroad",c:"ОАЭ",dt:"24 ноября – 1 декабря 2026 · 7 ночей",k:"2026-11-24",m:[11],img:"dubai.jpg",imgMode:"country",b:"4★ · без питания",p:88384,u:"за 2 взрослых",d:"Шарджа · номер Deluxe Suite · 2-я линия, песок.",src:"https://sletat.ru/hot-tour/saint_petersburg/uae/"},
{id:"custom",n:"Индивидуальный подбор",t:"custom",c:"Свой маршрут",dt:"Ваш маршрут · ваши даты",k:"2027-01-01",m:[],img:"custom.jpg",b:"Эксклюзив",p:0,u:"по запросу",d:"Подберём маршрут под ваши даты, бюджет и состав группы: от выходных в области до дальних стран."}];
var $=function(i){return document.getElementById(i)},type="",E=function(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
function imgFb(i){var f=i.dataset.fb;if(f){i.onerror=null;i.src="static/img/"+f}else i.remove()}
function goal(n){try{if(window.ym&&YM_ID)ym(YM_ID,"reachGoal",n)}catch(e){}}
var cs=[];T.forEach(function(x){if(cs.indexOf(x.c)<0)cs.push(x.c)});
cs.forEach(function(c){var o=document.createElement("option");o.textContent=c;o.value=c;$("fc").appendChild(o)});
[["","Все"],["abroad","Зарубежные туры"],["russia","По России"],["custom","Индивидуальные"]].forEach(function(a){var b=document.createElement("button");b.textContent=a[1];b.onclick=function(){type=a[0];$("ft").value=a[0];render()};b.dataset.v=a[0];$("chips").appendChild(b)});
function render(){
 var c=$("fc").value,m=+$("fm").value,bd=+$("fb").value,ty=$("ft").value;type=ty;
 var L=T.filter(function(x){return(!c||x.c===c)&&(!ty||x.t===ty)&&(!m||x.m.indexOf(m)>-1)&&(!bd||!x.p||x.p<=bd)});
 if(!c&&!m&&!bd&&!ty)L=T.slice();
 L.sort($("fs").value==="price"?function(a,b){return(a.p||9e9)-(b.p||9e9)}:function(a,b){return a.k<b.k?-1:1});
 $("grid").innerHTML=L.map(function(x){return'<article class="card" id="tour-'+x.id+'"><div class="ph'+(x.imgMode==='country'?' ph-country':'')+'">'+(x.img?'<img class="'+(x.imgMode==='banner'?'tour-banner':x.imgMode==='country'?'country-photo':x.src?'tour-photo':'')+'" src="static/img/'+x.img+'" alt="'+E(x.n)+'" loading="lazy" data-fb="'+(x.fb||'')+'" onerror="imgFb(this)">':'<span class="ph-place">'+E(x.c)+'</span>')+(x.b?'<span class="tag">'+E(x.b)+'</span>':'')+'</div><div class="cb"><h3>'+E(x.n)+'</h3><div class="meta">'+E(x.dt)+' · из Санкт-Петербурга</div><div class="d">'+E(x.d)+'</div><div class="pr">'+(x.p?'<small>'+E(x.u)+'</small><b>от '+x.p.toLocaleString("ru-RU")+' ₽</b>':'<b>по запросу</b>')+'</div><div class="row"><button class="btn" data-book="'+E(x.n)+'" data-dates="'+E(x.dt)+'">Забронировать</button></div>'+(x.src?'<a class="source-link" href="'+E(x.src)+'" target="_blank" rel="noopener">Сверить цену на Sletat.ru</a>':'')+'</div></article>'}).join("");
 $("empty").style.display=L.length?"none":"block";
 [].forEach.call($("chips").children,function(b){b.className=b.dataset.v===ty?"on":""});
}
["fc","ft","fm","fs"].forEach(function(i){$(i).onchange=render});$("fb").oninput=render;
$("go").onclick=function(){render();goal("search");$("tours").scrollIntoView()};
document.addEventListener("click",function(e){var b=e.target.closest("[data-book]");if(b){e.preventDefault();$("bt").value=b.dataset.book;$("bd").value=b.dataset.dates||"";$("bp").value=$("fp").value;$("bf").style.display="";$("ok").style.display="none";bk.showModal();goal("book_click");return}
 var g=e.target.closest("[data-g]");if(g)goal("contact_"+g.dataset.g)});
var u=new URLSearchParams(location.search),src=[u.get("utm_source"),u.get("utm_campaign")].filter(Boolean).join("/")||document.referrer||"прямой заход";
$("bf").onsubmit=function(e){e.preventDefault();if($("hp").value)return;
 var tour=$("bt").value,ph=$("bph").value.replace(/[^\d+]/g,""),key=tour+ph,last=localStorage.getItem("nt_last");
 var msg="Новая заявка Novo Tours\nТур: "+(tour||"—")+"\nВылет: "+$("bc").value+"\nДаты: "+($("bd").value||"—")+"\nТуристов: "+$("bp").value+"\nПродолжительность: "+($("bdu").value||"—")+"\nБюджет: "+($("bb").value||"—")+"\nИмя: "+$("bn").value+"\nТелефон: "+$("bph").value+"\nКомментарий: "+($("bm").value||"—")+"\nИсточник: "+src;
 function done(t){$("bf").style.display="none";if(t)$("okt").textContent=t;$("ok").style.display="block";goal("lead")}
 if(last&&last.split("|")[0]===key&&Date.now()-last.split("|")[1]<6e5){done("Эту заявку мы уже получили. Свяжемся с вами в ближайшее время.");return}
 try{localStorage.setItem("nt_last",key+"|"+Date.now())}catch(x){}
 if(WORKER_URL){fetch(WORKER_URL,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:msg})}).then(function(r){if(!r.ok)throw 0;done()}).catch(function(){location.href="https://t.me/"+TG+"?text="+encodeURIComponent(msg);done("Не удалось отправить автоматически. Откройте Telegram и отправьте сообщение — или позвоните: +7 981 882-08-88.")})}
 else{window.open("https://t.me/"+TG+"?text="+encodeURIComponent(msg),"_blank");done("Откроется Telegram с готовым сообщением — нажмите «Отправить». Или позвоните: +7 981 882-08-88.")}};
render();
