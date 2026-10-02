import {adminViews} from './admin.js';
// Frontend UAO · Reservas de salas. Sin build: se sirve como archivos estáticos.
const API=(localStorage.uao_api||'http://127.0.0.1:8000/api/v1').replace(/\/$/,'');
const $=(s,e=document)=>e.querySelector(s),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ICONS={users:'<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6M16 4.5a3.5 3.5 0 0 1 0 7M22 20c0-3-1.5-5-4-5.8"/>',home:'<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',cal:'<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',plus:'<path d="M12 5v14M5 12h14"/>',list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',bld:'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 21v-4h6v4M9 7h.01M15 7h.01M9 11h.01M15 11h.01"/>',out:'<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',menu:'<path d="M3 6h18M3 12h18M3 18h18"/>',chev:'<path d="M15 18l-6-6 6-6"/>',ok:'<path d="M20 6L9 17l-5-5"/>',x:'<path d="M18 6L6 18M6 6l12 12"/>',clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',shield:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'};
const I=n=>`<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICONS[n]}</svg>`;
const hhmm=t=>String(t).slice(0,5),today=()=>new Date().toLocaleDateString('sv-SE'),longDate=d=>new Date(d+'T00:00').toLocaleDateString('es-CO',{day:'numeric',month:'long',year:'numeric'});
const T=[];for(let m=420;m<=1260;m+=30)T.push(String(m/60|0).padStart(2,'0')+':'+(m%60?'30':'00'));
const E=T.map((_,i)=>T[i+1]||'21:30');
const S={u:JSON.parse(localStorage.uao_user||'null'),d:null,ref:null},app=$('#app');
window.logoFail=i=>{const s=document.createElement('span');s.className='wm';s.textContent='Universidad Autónoma de Occidente';i.replaceWith(s)};
const logo=()=>`<img class="logo" src="assets/logo-uao.png" alt="Universidad Autónoma de Occidente" onerror="logoFail(this)">`;
async function api(path,o={}){let r;try{r=await fetch(API+path,{...o,headers:{'Content-Type':'application/json'},body:o.body&&JSON.stringify(o.body)})}catch{throw new Error('No se pudo conectar con el servidor. Verifica que la API esté en ejecución.')}
 if(!r.ok){let d;try{d=(await r.json()).detail}catch{}throw new Error(typeof d==='string'?d:'No se pudo completar la acción. Revisa los datos e inténtalo de nuevo.')}return r.json()}
const ref=()=>S.ref||(S.ref=Promise.all([api('/facultades'),api('/salas')]).then(([f,s])=>({f,s})));
function toast(m,t='ok'){const e=document.createElement('div');e.className='toast '+t;e.innerHTML=I(t==='ok'?'ok':'x')+`<span>${esc(m)}</span>`;$('#ts').append(e);setTimeout(()=>e.remove(),3800)}
function modal(h){const m=document.createElement('div');m.className='md';m.innerHTML=`<div class="box">${h}</div>`;m.onclick=e=>{if(e.target===m||e.target.closest('[data-x]'))m.remove()};document.body.append(m);return m}
document.addEventListener('keydown',e=>e.key==='Escape'&&$('.md')?.remove());
async function busy(b,txt,fn){const o=b.innerHTML;b.disabled=true;b.innerHTML='<span class="sp"></span>'+txt;try{await fn()}catch(e){toast(e.message,'err')}finally{b.disabled=false;b.innerHTML=o}}
const empty=(i,t,p,b='')=>`<div class="empty">${I(i)}<h3>${t}</h3><p>${esc(p||'')}</p>${b}</div>`;
const SK='<div class="sk" style="height:110px"></div><div class="sk" style="height:110px"></div><div class="sk" style="height:110px"></div>';
const NAV=[['','home','Inicio'],['disponibilidad','cal','Disponibilidad'],['reservar','plus','Nueva reserva'],['reservas','list','Mis reservas'],['salas','bld','Salas'],['admin','shield','Reservas',1],['usuarios','users','Usuarios',1],['admsalas','bld','Gestión de salas',1],['facultades','bld','Facultades',1],['auditoria','list','Auditoría',1]];

function login(){app.innerHTML=`<div class="lg2"><section class="hero"><div class="plate">${logo()}</div><h1>Sistema de Reservas de Salas</h1><p>Encuentra y reserva el espacio que necesitas para tus reuniones y actividades de coordinación.</p></section><section class="fp"><form id="lf"><h2>Iniciar sesión</h2><label>Correo institucional<input type="email" id="e" required autofocus placeholder="Tu correo institucional"></label><button class="btn big">Iniciar sesión</button></form></section></div>`;
 $('#lf').onsubmit=ev=>{ev.preventDefault();busy($('.btn',ev.target),'Verificando…',async()=>{const u=(await api('/usuarios')).find(x=>x.correo_institucional.toLowerCase()===$('#e').value.trim().toLowerCase());
  if(!u)throw new Error('No encontramos ese correo institucional.');if(u.estado!=='Activo')throw new Error('Tu cuenta está inactiva. Contacta a la secretaría de tu facultad.');
  S.u=u;localStorage.uao_user=JSON.stringify(u);location.hash='#/';render()})}}

function shell(r){const sec=S.u.rol==='Secretaria',cur=NAV.find(n=>n[0]===r)||NAV[0],link=n=>`<a href="#/${n[0]}" class="${n[0]===r?'on':''}">${I(n[1])}<span>${n[2]}</span></a>`;
 app.innerHTML=`<div class="app ${localStorage.uao_c?'c':''}"><aside class="sb"><div class="brand">${logo()}<small>Sistema de Reservas</small></div><nav>${NAV.filter(n=>!n[3]).map(link).join('')}${sec?'<p class="gh">Administración</p>'+NAV.filter(n=>n[3]).map(link).join(''):''}</nav><button class="lk" id="col">${I('chev')}<span>Contraer</span></button></aside><div class="mn"><header><button class="ib" id="mb" aria-label="Menú">${I('menu')}</button><div class="bc">Inicio${cur[0]?` / <b>${cur[2]}</b>`:''}</div><div class="me"><div><b>${esc(S.u.nombre_completo)}</b><small>${S.u.rol}</small></div><span class="av">${esc(S.u.nombre_completo[0])}</span><button class="ib" id="out" title="Cerrar sesión">${I('out')}</button></div></header><main id="v" class="in"></main></div></div>`;
 const a=$('.app');$('#col').onclick=()=>{a.classList.toggle('c');localStorage.uao_c=a.classList.contains('c')?1:''};
 $('#mb').onclick=()=>a.classList.toggle('open');a.onclick=e=>{if(e.target===a||e.target.closest('.sb a'))a.classList.remove('open')};
 $('#out').onclick=()=>{S.u=null;S.d=null;localStorage.removeItem('uao_user');location.hash='#/';render()}}

async function dash(v){const [mine,dp,{s}]=await Promise.all([api('/reservas/mias?usuarioId='+S.u.id_usuario),api(`/reservas/disponibilidad?facultadId=${S.u.id_facultad}&fecha=${today()}`).catch(()=>null),ref()]);
 const vig=mine.filter(r=>r.estado!=='Cancelada'),now=new Date().toLocaleString('sv-SE').slice(0,16).replace(' ','T');
 const nx=vig.filter(r=>r.fecha+'T'+hhmm(r.hora_inicio)>=now).sort((a,b)=>(a.fecha+a.hora_inicio).localeCompare(b.fecha+b.hora_inicio))[0],sa=nx&&s.find(x=>x.id_sala===nx.id_sala);
 const libres=dp?dp.salas.filter(x=>x.disponibles.length).length:0;
 v.innerHTML=`<h1>¡Hola, ${esc(S.u.nombre_completo.split(' ')[0])}!</h1><p class="sub">Gestiona tus reservas de salas de manera sencilla.</p><div class="hd"><a class="btn" href="#/disponibilidad">Consultar disponibilidad</a><a class="btn acc" href="#/reservar">Nueva reserva</a></div>
 <div class="stats"><a class="card" href="#/reservas"><small>Mis reservas</small><b>${vig.length}</b><em>Ver reservas</em></a>
 <a class="card" href="#/reservas"><small>Próxima reserva</small><b style="font-size:1.25rem">${nx?(nx.fecha===today()?'Hoy':longDate(nx.fecha))+' · '+hhmm(nx.hora_inicio):'Sin reservas próximas'}</b><em>${nx?esc(sa?.nombre||''):'Ver reservas'}</em></a>
 <a class="card" href="#/disponibilidad"><small>Salas con horario libre hoy</small><b>${libres}</b><em>Consultar</em></a></div>`}

function grid(el,salas,fecha,cb){let sel=null;const n=new Date().toTimeString().slice(0,5),td=fecha===today(),st=(s,t)=>td&&t<n?'past':s.disponibles.some(d=>hhmm(d.hora_inicio)===t)?'free':'busy';
 el.innerHTML=`<div class="gw"><table class="g"><thead><tr><th></th>${T.map(t=>`<th>${t.endsWith(':00')?+t.slice(0,2):''}</th>`).join('')}</tr></thead><tbody>${salas.map((s,r)=>`<tr><th>${esc(s.nombre)}</th>${T.map((t,i)=>{const c=st(s,t);return `<td><button class="c ${c}" data-r="${r}" data-i="${i}" ${c==='free'?'':'disabled'} title="${t} – ${E[i]}"></button></td>`}).join('')}</tr>`).join('')}</tbody></table></div>`;
 const q=(r,i)=>el.querySelector(`[data-r="${r}"][data-i="${i}"]`);
 el.onclick=e=>{const b=e.target.closest('.c.free');if(!b)return;const r=+b.dataset.r,i=+b.dataset.i;
  if(sel&&sel.r===r&&sel.a===sel.b&&i>sel.a&&T.slice(sel.a,i+1).every((_,k)=>q(r,sel.a+k).classList.contains('free')))sel.b=i;else sel={r,a:i,b:i};
  el.querySelectorAll('.c.on').forEach(x=>x.classList.remove('on'));for(let k=sel.a;k<=sel.b;k++)q(r,k).classList.add('on');
  cb({sala:salas[r],ini:T[sel.a],fin:E[sel.b]})}}
const legend='<div class="lgd"><i class="free"></i>Disponible<i class="busy"></i>Ocupado<i class="past"></i>No disponible · Toca una franja y otra más para elegir un rango</div>';

async function disp(v){const {f}=await ref();v.innerHTML=`<h1>Disponibilidad</h1><p class="sub">Elige facultad y fecha; luego marca el horario que necesitas.</p><div class="bar"><label>Facultad<select id="f">${f.map(x=>`<option value="${x.id_facultad}" ${x.id_facultad===S.u.id_facultad?'selected':''}>${esc(x.nombre)}</option>`).join('')}</select></label><label>Fecha<input type="date" id="d" value="${today()}" min="${today()}"></label></div>${legend}<div id="g"></div><div id="pick" class="pick"></div>`;
 const load=async()=>{const g=$('#g');g.innerHTML='<div class="sk" style="height:200px"></div>';$('#pick').innerHTML='';
  try{const d=await api(`/reservas/disponibilidad?facultadId=${$('#f').value}&fecha=${$('#d').value}`);grid(g,d.salas,d.fecha,x=>{const own=+$('#f').value===S.u.id_facultad;
   $('#pick').innerHTML=`<div class="card"><div><b>${esc(x.sala.nombre)}</b> · ${longDate(d.fecha)} · ${x.ini} – ${x.fin}</div>${own?'<button class="btn acc" id="go">Reservar este horario</button>':'<small>Solo puedes reservar en tu propia facultad.</small>'}</div>`;
   if(own)$('#go').onclick=()=>{S.d={step:5,f:S.u.id_facultad,fecha:d.fecha,sala:x.sala,ini:x.ini,fin:x.fin,disp:d};location.hash='#/reservar'}})}
  catch(e){g.innerHTML=empty('bld','No hay salas disponibles para esta fecha.',e.message)}};
 $('#f').onchange=$('#d').onchange=load;load()}

async function book(v){const {f}=await ref(),D=S.d||(S.d={step:1,f:S.u.id_facultad,fecha:today()}),names=['Facultad','Fecha','Sala','Horario','Confirmar'];
 const draw=async()=>{v.innerHTML=`<h1>Nueva reserva</h1><p class="sub">Sigue los pasos; siempre puedes volver atrás.</p><ol class="st">${names.map((n,i)=>`<li class="${i+1<D.step?'done':i+1===D.step?'on':''}"><span>${i+1<D.step?I('ok'):i+1}</span>${n}</li>`).join('')}</ol><section class="card" id="p"></section>`;
  const p=$('#p'),nav=(ok,t='Continuar')=>`<div class="act">${D.step>1?'<button class="btn ghost" id="bk">Volver</button>':''}<button class="btn ${D.step===5?'acc':''}" id="nx" ${ok?'':'disabled'}>${t}</button></div>`,go=n=>{D.step=n;draw()};
  const wire=fn=>{const b=$('#bk');if(b)b.onclick=()=>go(D.step-1);$('#nx').onclick=fn||(()=>go(D.step+1))};
  if(D.step===1){const sec=S.u.rol==='Secretaria';if(sec&&!D.doc)D.doc=await api(`/usuarios?facultadId=${S.u.id_facultad}&rol=Docente&estado=Activo`).catch(()=>[]);p.innerHTML=`<h2>Selecciona tu facultad</h2><div class="opts">${f.map(x=>{const own=x.id_facultad===S.u.id_facultad;return `<button class="opt ${x.id_facultad===D.f?'on':''}" ${own?'':'disabled'}>${I('bld')}<b>${esc(x.nombre)}</b><small>${own?'Tu facultad':'Solo puedes reservar en tu facultad'}</small></button>`}).join('')}</div>${sec?`<label style="max-width:360px;margin-top:16px">Reservar a nombre de<select id="ow"><option value="${S.u.id_usuario}">Mí (${esc(S.u.nombre_completo)})</option>${D.doc.map(u=>`<option value="${u.id_usuario}" ${D.owner==u.id_usuario?'selected':''}>${esc(u.nombre_completo)} (Docente)</option>`).join('')}</select></label>`:''}${nav(1)}`;wire(()=>{if(sec)D.owner=+$('#ow').value;go(2)})}
  if(D.step===2){p.innerHTML=`<h2>Selecciona la fecha</h2><label style="max-width:240px"><input type="date" id="d" value="${D.fecha}" min="${today()}"></label>${nav(1)}`;
   wire(()=>{const d=$('#d').value;if(!d||d<today())return toast('Elige una fecha válida.','err');if(d!==D.fecha){D.fecha=d;D.sala=D.ini=D.fin=D.disp=null}go(3)})}
  if(D.step===3){p.innerHTML=SK;try{D.disp=await api(`/reservas/disponibilidad?facultadId=${D.f}&fecha=${D.fecha}`)}catch(e){p.innerHTML=empty('bld','No hay salas disponibles para esta fecha.',e.message)+nav(0);return wire()}
   p.innerHTML=`<h2>Selecciona una sala</h2><div class="opts">${D.disp.salas.map(s=>`<button class="opt ${D.sala?.id_sala===s.id_sala?'on':''}" data-id="${s.id_sala}">${I('bld')}<b>${esc(s.nombre)}</b><small>${s.disponibles.length} franjas libres</small></button>`).join('')}</div>${nav(D.sala)}`;
   p.onclick=e=>{const b=e.target.closest('.opt');if(!b)return;D.sala=D.disp.salas.find(s=>s.id_sala==b.dataset.id);D.ini=D.fin=null;draw()};wire()}
  if(D.step===4){p.innerHTML=`<h2>Selecciona el horario</h2>${legend}<div id="g"></div><p id="h" style="color:var(--mut)">${D.ini?`${D.ini} – ${D.fin}`:'Aún no has elegido horario.'}</p>${nav(D.ini)}`;
   grid($('#g'),D.disp.salas.filter(s=>s.id_sala===D.sala.id_sala),D.fecha,x=>{D.ini=x.ini;D.fin=x.fin;$('#h').textContent=`${x.ini} – ${x.fin}`;$('#nx').disabled=false});wire()}
  if(D.step===5){p.innerHTML=`<h2>Resumen de reserva</h2><dl><dt>Facultad</dt><dd>${esc(f.find(x=>x.id_facultad===D.f)?.nombre)}</dd><dt>Sala</dt><dd>${esc(D.sala.nombre)}</dd><dt>Fecha</dt><dd>${longDate(D.fecha)}</dd><dt>Horario</dt><dd>${D.ini} – ${D.fin}</dd>${D.owner&&D.owner!==S.u.id_usuario?`<dt>A nombre de</dt><dd>${esc(D.doc.find(u=>u.id_usuario===D.owner)?.nombre_completo)}</dd>`:''}<dt>Estado</dt><dd><span class="tag Habilitada">Disponible</span></dd></dl>${nav(1,'Confirmar reserva')}`;
   wire(()=>busy($('#nx'),'Creando reserva…',async()=>{await api(`/reservas?usuarioId=${D.owner||S.u.id_usuario}&facultadId=${D.f}&salaId=${D.sala.id_sala}`,{method:'POST',body:{fecha:D.fecha,hora_inicio:D.ini,hora_fin:D.fin}});S.d=null;toast('Reserva creada correctamente.');location.hash='#/reservas'}))}};
 draw()}

async function cards(v,list,title,sub,em){const {f,s}=await ref(),SA=Object.fromEntries(s.map(x=>[x.id_sala,x])),FA=Object.fromEntries(f.map(x=>[x.id_facultad,x.nombre])),sec=S.u.rol==='Secretaria';
 v.innerHTML=`<h1>${title}</h1><p class="sub">${sub}</p>`+(list.length?`<div class="cg">${list.map(r=>{const sa=SA[r.id_sala]||{};return `<article class="card rc"><div class="top"><h3>${esc(sa.nombre||'Sala '+r.id_sala)}</h3><span class="tag ${r.estado}">${r.estado}</span></div><p>${I('bld')}${esc(FA[sa.id_facultad]||'')}</p><p>${I('cal')}${longDate(r.fecha)}</p><p>${I('clock')}${hhmm(r.hora_inicio)} – ${hhmm(r.hora_fin)}</p>${r.estado!=='Cancelada'?`<div class="act">${sec?`<button class="btn ghost" data-a="e" data-id="${r.id_reserva}">Modificar</button>`:''}<button class="btn warn" data-a="c" data-id="${r.id_reserva}">Cancelar</button></div>`:''}</article>`}).join('')}</div>`:empty('list',em,'',em.startsWith('No tienes')?'<a class="btn" href="#/reservar">Crear una reserva</a>':''));
 v.onclick=e=>{const b=e.target.closest('[data-a]');if(!b)return;const r=list.find(x=>x.id_reserva==b.dataset.id);b.dataset.a==='c'?cancel(r,SA,FA):edit(r,SA,s)}}
const mine=async v=>cards(v,await api('/reservas/mias?usuarioId='+S.u.id_usuario),'Mis reservas','Consulta, cancela o revisa el estado de tus reservas.','No tienes reservas todavía.');
const adminRes=async v=>cards(v,await api(`/reservas?facultadId=${S.u.id_facultad}&limit=100`),'Reservas de la facultad','Todas las reservas de las salas de tu facultad.','No hay reservas registradas.');

function cancel(r,SA){const m=modal(`<h2>¿Cancelar reserva?</h2><p>Estás a punto de cancelar esta reserva.</p><dl><dt>Sala</dt><dd>${esc(SA[r.id_sala]?.nombre)}</dd><dt>Fecha</dt><dd>${longDate(r.fecha)}</dd><dt>Hora</dt><dd>${hhmm(r.hora_inicio)} – ${hhmm(r.hora_fin)}</dd></dl><div class="act"><button class="btn ghost" data-x>Volver</button><button class="btn warn solid" id="ok">Cancelar reserva</button></div>`);
 $('#ok',m).onclick=e=>busy(e.currentTarget,'Cancelando…',async()=>{await api(`/reservas/${r.id_reserva}/cancelar?usuarioId=${S.u.id_usuario}`,{method:'PUT'});m.remove();toast('Reserva cancelada correctamente.');render()})}
function edit(r,SA,s){const sa=SA[r.id_sala],op=(a,v)=>a.map(x=>`<option ${x===v?'selected':''}>${x}</option>`).join('');
 const m=modal(`<h2>Modificar reserva</h2><div class="fm"><label>Sala<select id="s">${s.filter(x=>x.id_facultad===sa.id_facultad&&x.estado==='Habilitada').map(x=>`<option value="${x.id_sala}" ${x.id_sala===r.id_sala?'selected':''}>${esc(x.nombre)}</option>`).join('')}</select></label><label>Fecha<input type="date" id="d" value="${r.fecha}"></label><label>Hora inicio<select id="a">${op(T,hhmm(r.hora_inicio))}</select></label><label>Hora final<select id="b">${op(E,hhmm(r.hora_fin))}</select></label><label class="w">Motivo<textarea id="m" maxlength="300" placeholder="Explica por qué ajustas la reserva"></textarea></label></div><div class="act"><button class="btn ghost" data-x>Volver</button><button class="btn" id="ok">Guardar cambios</button></div>`);
 $('#ok',m).onclick=e=>{const mo=$('#m',m).value.trim();if(mo.length<5)return toast('El motivo debe tener al menos 5 caracteres.','err');
  busy(e.currentTarget,'Guardando…',async()=>{const x=await api(`/reservas/${r.id_reserva}/ajustar?usuarioId=${S.u.id_usuario}`,{method:'PUT',body:{salaId:+$('#s',m).value,fecha:$('#d',m).value,hora_inicio:$('#a',m).value,hora_fin:$('#b',m).value,motivo:mo}});
   m.remove();toast(`Reserva ajustada: ${SA[x.id_sala]?.nombre}, ${longDate(x.fecha)}, ${hhmm(x.hora_inicio)} – ${hhmm(x.hora_fin)}.`);render()})}}

async function rooms(v){const {f,s}=await ref(),sec=S.u.rol==='Secretaria';v.innerHTML=`<h1>Salas</h1><p class="sub">Espacios de cada facultad y los recursos con los que cuentan.</p><div class="bar"><label>Facultad<select id="f">${f.map(x=>`<option value="${x.id_facultad}" ${x.id_facultad===S.u.id_facultad?'selected':''}>${esc(x.nombre)}</option>`).join('')}</select></label></div><div id="l"></div>`;
 const show=async()=>{const l=$('#l'),id=+$('#f').value,list=s.filter(x=>x.id_facultad===id);if(!list.length)return l.innerHTML=empty('bld','No hay salas registradas en esta facultad.');
  l.innerHTML=SK;const rec=await Promise.all(list.map(x=>api(`/salas/${x.id_sala}/recursos`).catch(()=>[])));
  l.innerHTML=`<div class="cg">${list.map((x,i)=>`<article class="card rm"><div class="ic">${I('bld')}</div><h3>${esc(x.nombre)}</h3><p>Código: ${x.codigo}</p><span class="tag ${x.estado}">${x.estado}</span>${x.observaciones?`<p>${esc(x.observaciones)}</p>`:''}<ul>${rec[i].length?rec[i].map(r=>`<li>${I('ok')}${esc(r.nombre_recurso)}</li>`).join(''):'<li><small>Sin recursos registrados</small></li>'}</ul>${sec&&id===S.u.id_facultad?`<button class="btn ghost" data-id="${x.id_sala}" data-e="${x.estado==='Habilitada'?'Deshabilitada':'Habilitada'}">${x.estado==='Habilitada'?'Deshabilitar':'Habilitar'}</button>`:''}</article>`).join('')}</div>`;
  l.onclick=e=>{const b=e.target.closest('[data-e]');if(b)busy(b,'Guardando…',async()=>{await api(`/salas/${b.dataset.id}/estado?usuarioId=${S.u.id_usuario}`,{method:'PATCH',body:{estado:b.dataset.e}});S.ref=null;toast('Estado de la sala actualizado.');render()})}};
 $('#f').onchange=show;show()}

const V={...adminViews,'':dash,disponibilidad:disp,reservar:book,reservas:mine,salas:rooms,admin:adminRes};
async function render(){if(!S.u)return login();const r=location.hash.slice(2);shell(r);const v=$('#v');v.innerHTML=SK;
 try{await(V[r]||dash)(v)}catch(e){v.innerHTML=empty('x','No pudimos cargar la información',e.message,'<button class="btn" onclick="location.reload()">Reintentar</button>')}}
addEventListener('hashchange',render);render();

export{S,$,esc,I,api,ref,toast,modal,busy,empty,SK,render};
