/* Cuentas de Paw Party y Paw Diary (Firebase Auth + Firestore, plan Spark gratis).
   Solo se activa si build.py tiene CONFIG['firebase']. Sin cuenta, todo sigue funcionando con guardado local.
   Qué se sube: mascotas (con foto chica), diario, recordatorios y nombres favoritos. Las fotos del diario quedan en el equipo.
   Documento: users/{uid}/data/main  (las reglas de Firestore dejan leer/escribir solo al dueño). */
(function(){
'use strict';
if(!CFG.firebase)return;
var L=CFG.lang,KEYS=['cozypaws-pets','cozypaws-diary','cozypaws-fun'],AT='cozypaws-sync-at',V='10.12.5',B='https://www.gstatic.com/firebasejs/'+V+'/';
var T={en:{acc:'Account',signH:'Save on all your devices',signB:'Sign in to keep your pets, diary and reminders safe in the cloud and see them on your phone and computer. Free. Diary photos stay on this device.',
google:'Continue with Google',orEmail:'Or get a sign-in link by email',email:'Your email',send:'Email me a link',sent:'Check your email and open the link on this device.',
inAs:'Signed in as {e}',synced:'Synced {t}',never:'Not synced yet',syncNow:'Sync now',out:'Sign out',delAcc:'Delete my account and cloud data',delQ:'This deletes your account and the copy in the cloud. Data on this device stays. Continue?',
deleted:'Account deleted',again:'For safety, sign in again and then delete.',err:'Something went wrong. Try again.',close:'Close',confirmEmail:'Confirm your email to finish signing in',privacy:'We only save your email and your app data. See our'},
es:{acc:'Cuenta',signH:'Guarda en todos tus equipos',signB:'Inicia sesión para guardar tus mascotas, diario y recordatorios en la nube y verlos en tu celular y tu computadora. Gratis. Las fotos del diario quedan en este equipo.',
google:'Continuar con Google',orEmail:'O recibe un enlace por correo',email:'Tu correo',send:'Enviarme el enlace',sent:'Revisa tu correo y abre el enlace en este equipo.',
inAs:'Sesión iniciada como {e}',synced:'Sincronizado {t}',never:'Todavía sin sincronizar',syncNow:'Sincronizar ahora',out:'Cerrar sesión',delAcc:'Borrar mi cuenta y los datos en la nube',delQ:'Esto borra tu cuenta y la copia en la nube. Lo que está en este equipo queda. ¿Seguir?',
deleted:'Cuenta borrada',again:'Por seguridad, inicia sesión de nuevo y después bórrala.',err:'Algo salió mal. Prueba de nuevo.',close:'Cerrar',confirmEmail:'Confirma tu correo para terminar de entrar',privacy:'Solo guardamos tu correo y los datos de la app. Mira nuestra'}}[L];
function t(k,v){var s=T[k];return v?s.replace(/\{(\w+)\}/g,function(_,x){return v[x]}):s}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
var fb=null,user=null,timer=null,pulling=false;
function load(){return fb||(fb=Promise.all([import(B+'firebase-app.js'),import(B+'firebase-auth.js'),import(B+'firebase-firestore.js')]).then(function(m){
 var app=m[0].initializeApp(CFG.firebase),auth=m[1].getAuth(app),db=m[2].getFirestore(app);auth.languageCode=L;return {A:m[1],F:m[2],auth:auth,db:db}}).catch(function(e){fb=null;throw e}))}
function local(){var o={};KEYS.forEach(function(k){try{o[k]=JSON.parse(localStorage.getItem(k))}catch(e){o[k]=null}});return o}
function localAt(){return +localStorage.getItem(AT)||0}
function ref(f){return f.F.doc(f.db,'users',user.uid,'data','main')}
// unión por id: no se pierde nada la primera vez que se juntan un equipo y la nube
function merge(a,b){if(!a)return b;if(!b)return a;var o=JSON.parse(JSON.stringify(b));
 if(a.pets){o.pets=o.pets||[];a.pets.forEach(function(p){if(!o.pets.some(function(x){return x.id===p.id}))o.pets.push(p)});if(!o.cur)o.cur=a.cur}
 ['log','rem'].forEach(function(k){if(a[k]){o[k]=o[k]||[];a[k].forEach(function(p){if(!o[k].some(function(x){return x.id===p.id}))o[k].push(p)})}});
 if(a.favs){o.favs=o.favs||[];a.favs.forEach(function(n){if(o.favs.indexOf(n)<0)o.favs.push(n)})}return o}
var raw=Storage.prototype.setItem;
function writeLocal(data,at){KEYS.forEach(function(k){if(data[k]!=null)raw.call(localStorage,k,JSON.stringify(data[k]))});raw.call(localStorage,AT,String(at))}
function push(){if(!user)return;clearTimeout(timer);timer=setTimeout(function(){load().then(function(f){var at=Date.now(),d=local();
 return f.F.setDoc(ref(f),{data:JSON.stringify(d),at:at,app:'cozypaws'}).then(function(){raw.call(localStorage,AT,String(at));badge()})}).catch(function(e){console.warn(e)})},1500)}
function pull(first){if(!user||pulling)return Promise.resolve();pulling=true;return load().then(function(f){return f.F.getDoc(ref(f)).then(function(s){pulling=false;
 if(!s.exists()){push();return}var r=s.data(),rd=JSON.parse(r.data||'{}'),ld=local();
 if(first){var m={};KEYS.forEach(function(k){m[k]=merge(ld[k],rd[k])});var changed=JSON.stringify(m)!==JSON.stringify(ld);writeLocal(m,r.at);if(JSON.stringify(m)!==JSON.stringify(rd))push();if(changed)location.reload();return}
 if(r.at>localAt()){writeLocal(rd,r.at);location.reload()}})}).catch(function(e){pulling=false;console.warn(e)})}
// cada vez que la app guarda algo, se sube (con una pausa corta para juntar cambios)
Storage.prototype.setItem=function(k,v){raw.call(this,k,v);if(this===localStorage&&KEYS.indexOf(k)>=0)push()};

var btn=document.createElement('button');btn.className='chip';btn.id='acct';btn.type='button';btn.textContent='👤';btn.setAttribute('aria-label',t('acc'));
var top=document.querySelector('.top');top.insertBefore(btn,document.getElementById('lang'));
function badge(){btn.textContent=user?'✅ '+(user.displayName||user.email||'').split(/[ @]/)[0]:'👤 '+t('acc')}
var dlg=document.getElementById('dlg');function open(h){dlg.innerHTML=h;if(dlg.showModal&&!dlg.open)dlg.showModal()}
function close(){if(dlg.close)dlg.close()}
function panel(){if(user){var at=localAt();open('<h2 style="margin-top:0">👤 '+t('acc')+'</h2><p>'+t('inAs',{e:esc(user.email||user.displayName)})+'</p><p class="muted">'+(at?t('synced',{t:new Date(at).toLocaleString()}):t('never'))+'</p>'+
  '<div class="btns"><button class="btn alt" id="aSync">🔄 '+t('syncNow')+'</button><button class="btn ghost" id="aOut">'+t('out')+'</button></div><details class="more" style="margin-top:16px"><summary>'+t('delAcc')+'</summary><p>'+t('delQ')+'</p><button class="btn ghost" id="aDel">🗑 '+t('delAcc')+'</button></details><div class="btns"><button class="btn ghost" id="aX">'+t('close')+'</button></div>');
  document.getElementById('aSync').onclick=function(){pull(true).then(function(){push();close()})};
  document.getElementById('aOut').onclick=function(){load().then(function(f){return f.A.signOut(f.auth)}).then(close)};
  document.getElementById('aDel').onclick=function(){if(!confirm(t('delQ')))return;load().then(function(f){return f.F.deleteDoc(ref(f)).then(function(){return f.A.deleteUser(f.auth.currentUser)})}).then(function(){raw.call(localStorage,AT,'0');alert(t('deleted'));close()}).catch(function(e){alert(e&&e.code==='auth/requires-recent-login'?t('again'):t('err'))})};
 }else{open('<h2 style="margin-top:0">☁️ '+t('signH')+'</h2><p class="muted">'+t('signB')+'</p><button class="btn" id="aG" style="width:100%;justify-content:center">G&nbsp; '+t('google')+'</button>'+
  '<p style="margin:16px 0 6px;font-weight:600">'+t('orEmail')+'</p><form id="aE"><input type="email" required placeholder="'+t('email')+'" autocomplete="email"><div class="btns"><button class="btn alt" type="submit">✉️ '+t('send')+'</button><button class="btn ghost" type="button" id="aX">'+t('close')+'</button></div></form>'+
  '<p class="muted" style="font-size:13px">'+t('privacy')+' <a href="/privacy/">'+(L==='es'?'política de privacidad':'privacy policy')+'</a>.</p>');
  document.getElementById('aG').onclick=function(){load().then(function(f){var p=new f.A.GoogleAuthProvider(),standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
   return standalone?f.A.signInWithRedirect(f.auth,p):f.A.signInWithPopup(f.auth,p).catch(function(e){if(e&&e.code==='auth/popup-blocked')return f.A.signInWithRedirect(f.auth,p);throw e})}).then(close).catch(function(e){if(!e||e.code!=='auth/popup-closed-by-user')alert(t('err'))})};
  document.getElementById('aE').onsubmit=function(e){e.preventDefault();var em=this.querySelector('input').value.trim();load().then(function(f){return f.A.sendSignInLinkToEmail(f.auth,em,{url:location.origin+location.pathname,handleCodeInApp:true})}).then(function(){localStorage.setItem('cozypaws-email',em);alert(t('sent'));close()}).catch(function(){alert(t('err'))})}}
 var x=document.getElementById('aX');if(x)x.onclick=close}
btn.onclick=panel;badge();
// arranca Firebase solo si ya hay sesión o vuelve de un enlace de correo (no carga nada extra a quien no lo usa)
var hadUser=localAt()>0||/apiKey=|oobCode=/.test(location.search);
function start(){load().then(function(f){f.A.getRedirectResult(f.auth).catch(function(){});
 if(f.A.isSignInWithEmailLink(f.auth,location.href)){var em=localStorage.getItem('cozypaws-email')||prompt(t('confirmEmail'));if(em)f.A.signInWithEmailLink(f.auth,em,location.href).then(function(){localStorage.removeItem('cozypaws-email');history.replaceState(null,'',location.pathname+location.hash)}).catch(function(){alert(t('err'))})}
 f.A.onAuthStateChanged(f.auth,function(u){var was=user;user=u;badge();if(u&&!was){try{if(window.gtag)gtag('event','login')}catch(e){}pull(true)}})}).catch(function(e){console.warn('cuenta: sin conexión',e)})}
if(hadUser)start();else btn.addEventListener('click',start,{once:true});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'&&user)pull(false)});
})();
