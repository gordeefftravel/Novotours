/* Novo Tours — общий JS: меню, избранное, шаринг, вкладки, каталог, заявка. Без зависимостей. */
(function(){
"use strict";
var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return[].slice.call((r||document).querySelectorAll(s))};
var WORKER_URL="https://novotours-bb57.nowotours.workers.dev",TG="GordeeffPhoto",YM_ID="114045220";
function goal(n){try{if(window.ym)ym(YM_ID,"reachGoal",n)}catch(e){}}
function toast(m){var t=$("#nvToast");if(!t){t=document.createElement("div");t.id="nvToast";t.className="nv-toast";t.setAttribute("role","status");document.body.appendChild(t)}
 t.textContent=m;t.classList.add("show");clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove("show")},2800)}
/* хранилище: безопасно, если localStorage недоступен */
var store={get:function(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
/* меню */
var bg=$(".nv-burger"),nav=$(".nv-nav");
if(bg&&nav){bg.addEventListener("click",function(){var o=nav.classList.toggle("open");bg.setAttribute("aria-expanded",o)});
 nav.addEventListener("click",function(e){if(e.target.closest("a"))nav.classList.remove("open")})}
/* появление при прокрутке */
if("IntersectionObserver"in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});
 $$(".nv-reveal").forEach(function(el){io.observe(el)})}else $$(".nv-reveal").forEach(function(el){el.classList.add("in")});
/* избранное */
function favs(){return store.get("nt_favs",[])}
function paintFavs(){var f=favs();$$("[data-fav]").forEach(function(b){var on=f.indexOf(b.dataset.fav)>-1;b.setAttribute("aria-pressed",on);b.setAttribute("aria-label",on?"Убрать из избранного":"В избранное")})}
document.addEventListener("click",function(e){var b=e.target.closest("[data-fav]");if(!b)return;e.preventDefault();e.stopPropagation();
 var f=favs(),k=b.dataset.fav,i=f.indexOf(k);if(i>-1)f.splice(i,1);else{f.push(k);goal("fav_add")}store.set("nt_favs",f);paintFavs();
 toast(i>-1?"Убрано из избранного":"Добавлено в избранное");document.dispatchEvent(new Event("nv-favs"))});
paintFavs();
/* шаринг */
document.addEventListener("click",function(e){var b=e.target.closest("[data-share]");if(!b)return;
 var d={title:document.title,text:b.dataset.share||document.title,url:location.href.split("#")[0]};
 if(navigator.share){navigator.share(d).catch(function(){})}
 else if(navigator.clipboard){navigator.clipboard.writeText(d.url).then(function(){toast("Ссылка скопирована")},function(){toast(d.url)})}else toast(d.url);goal("share")});
/* вкладки */
$$("[data-tabs]").forEach(function(g){var bs=$$("button",g),ps=$$(".nv-panel",document.getElementById(g.dataset.tabs));
 bs.forEach(function(b,i){b.addEventListener("click",function(){bs.forEach(function(x,j){x.classList.toggle("on",i===j);x.setAttribute("aria-selected",i===j)});ps.forEach(function(p,j){p.classList.toggle("on",i===j)})})})});
/* подсветка пункта оглавления */
var toc=$$(".nv-toc a");if(toc.length&&"IntersectionObserver"in window){var map={};toc.forEach(function(a){map[a.getAttribute("href").slice(1)]=a});
 var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){toc.forEach(function(a){a.classList.remove("on")});var a=map[e.target.id];if(a)a.classList.add("on")}})},{rootMargin:"-30% 0px -60% 0px"});
 Object.keys(map).forEach(function(id){var s=document.getElementById(id);if(s)io2.observe(s)})}
/* ===== заявка ===== */
var legacy=document.getElementById("bk")&&document.getElementById("bf")&&!document.getElementById("nvbk");
function openBooking(o){o=o||{};
 if(legacy){var set=function(id,v){var el=document.getElementById(id);if(el&&v!=null&&v!=="")el.value=v};
  set("bt",o.tour);set("bc",o.from);set("bd",o.dates);set("bp",o.pax);set("bdu",o.dur);set("bb",o.budget);
  document.getElementById("bf").style.display="";document.getElementById("ok").style.display="none";document.getElementById("bk").showModal();goal("book_click");return}
 var d=document.getElementById("nvbk");if(!d)return;
 var f=d.querySelector("form");f.style.display="";d.querySelector(".ok").style.display="none";
 ["tour","from","dates","pax","dur","budget"].forEach(function(k){var el=f.elements[k];if(el&&o[k]!=null&&o[k]!=="")el.value=o[k]});
 d.showModal();goal("book_click")}
window.NV={openBooking:openBooking,toast:toast};
document.addEventListener("click",function(e){var b=e.target.closest("[data-nv-book]");if(!b)return;e.preventDefault();
 openBooking({tour:b.dataset.nvBook,dates:b.dataset.dates});});
/* виджет «Подобрать тур»: страна и параметры передаются в заявку */
$$(".nv-pick").forEach(function(f){
 var qs=new URLSearchParams(location.search),c=qs.get("country");if(c&&f.elements.country){[].forEach.call(f.elements.country.options,function(o){if(o.dataset.slug===c||o.value===c)f.elements.country.value=o.value})}
 f.addEventListener("submit",function(e){e.preventDefault();var g=function(n){return f.elements[n]?f.elements[n].value:""};
  openBooking({tour:g("country"),from:g("from"),dates:g("date"),pax:g("pax"),dur:g("dur"),budget:g("budget")});goal("pick_submit")})});
var nvf=document.querySelector("#nvbk form");
if(nvf){var u=new URLSearchParams(location.search),src=[u.get("utm_source"),u.get("utm_campaign")].filter(Boolean).join("/")||document.referrer||"прямой заход";
 nvf.addEventListener("submit",function(e){e.preventDefault();var F=nvf.elements;if(F.hp.value)return;
  var tour=F.tour.value,ph=F.phone.value.replace(/[^\d+]/g,""),key=tour+ph,last=store.get("nt_last",null);
  var msg="Новая заявка Novo Tours\nТур/страна: "+(tour||"—")+"\nВылет: "+F.from.value+"\nДаты: "+(F.dates.value||"—")+"\nТуристов: "+F.pax.value+"\nПродолжительность: "+(F.dur.value||"—")+"\nБюджет: "+(F.budget.value||"—")+"\nИмя: "+F.name.value+"\nТелефон: "+F.phone.value+"\nКомментарий: "+(F.comment.value||"—")+"\nСтраница: "+location.pathname+"\nИсточник: "+src;
  var d=document.getElementById("nvbk");function done(t){nvf.style.display="none";if(t)d.querySelector(".okt").textContent=t;d.querySelector(".ok").style.display="block";goal("lead")}
  if(last&&last.k===key&&Date.now()-last.t<6e5){done("Эту заявку мы уже получили. Свяжемся с вами в ближайшее время.");return}
  store.set("nt_last",{k:key,t:Date.now()});
  fetch(WORKER_URL,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:msg})}).then(function(r){if(!r.ok)throw 0;done()}).catch(function(){location.href="https://t.me/"+TG+"?text="+encodeURIComponent(msg);done("Не удалось отправить автоматически. Откройте Telegram и отправьте сообщение — или позвоните: +7 981 882-08-88.")})})}
/* ===== каталог стран ===== */
var cat=$("#catGrid");
if(cat){var cards=$$(".nv-card",cat),st={q:"",cont:"",type:"",sort:"name",fav:false},F=function(i){return document.getElementById(i)};
 var apply=function(){var q=st.q.trim().toLowerCase(),f=favs(),n=0;
  cards.forEach(function(c){var ok=(!q||c.dataset.text.indexOf(q)>-1)&&(!st.cont||c.dataset.cont===st.cont)&&(!st.type||c.dataset.types.split(",").indexOf(st.type)>-1)&&(!st.fav||f.indexOf("c:"+c.dataset.slug)>-1);c.hidden=!ok;if(ok)n++});
  var s=st.sort,arr=cards.slice().sort(function(a,b){return s==="budget"?(+a.dataset.bud)-(+b.dataset.bud):s==="budget-desc"?(+b.dataset.bud)-(+a.dataset.bud):a.dataset.name.localeCompare(b.dataset.name,"ru")});
  arr.forEach(function(c){cat.appendChild(c)});F("catEmpty").style.display=n?"none":"block";F("catCount").textContent=n};
 F("catQ").addEventListener("input",function(){st.q=this.value;apply()});
 ["catCont","catType","catSort"].forEach(function(id){F(id).addEventListener("change",function(){st[id==="catCont"?"cont":id==="catType"?"type":"sort"]=this.value;apply()})});
 F("catFav").addEventListener("click",function(){st.fav=!st.fav;this.classList.toggle("on",st.fav);apply()});
 document.addEventListener("nv-favs",function(){if(st.fav)apply()});
 var h=location.hash.match(/^#cont=(.+)$/);if(h){F("catCont").value=decodeURIComponent(h[1]);st.cont=F("catCont").value}
 apply()}
/* ===== страница избранного ===== */
var fl=$("#favList");
if(fl){var render=function(){var f=favs();fetch("/static/data/index.json").then(function(r){return r.json()}).then(function(db){
  var out="",cs=db.countries.filter(function(c){return f.indexOf("c:"+c.slug)>-1}),ss=[];
  db.countries.forEach(function(c){c.sights.forEach(function(s){if(f.indexOf("s:"+c.slug+":"+s)>-1)ss.push([c,s])})});
  if(cs.length){out+="<h2 class='nv-h2'>Страны</h2><div class='nv-tiles'>"+cs.map(function(c){return"<div class='nv-tile'><h3>"+c.name+"</h3><p>"+c.tagline+"</p><a href='/countries/"+c.slug+"/'>Открыть страницу →</a></div>"}).join("")+"</div>"}
  if(ss.length){out+="<h2 class='nv-h2' style='margin-top:32px'>Места</h2><div class='nv-tiles'>"+ss.map(function(x){return"<div class='nv-tile'><h3>"+x[1]+"</h3><p>"+x[0].name+"</p><a href='/countries/"+x[0].slug+"/#sights'>К месту →</a></div>"}).join("")+"</div>"}
  fl.innerHTML=out||"<div class='nv-box'><p>Пока пусто. Нажмите сердечко на карточке страны или места — и они появятся здесь. Избранное хранится только в вашем браузере.</p><a class='nv-btn' href='/countries/'>Открыть каталог стран</a></div>"})
  .catch(function(){fl.textContent="Не удалось загрузить данные."})};
 render();document.addEventListener("nv-favs",render)}
})();
