// Carrusel de Instagram R004 · El ciclo de vida de la ingeniería de datos (1080x1350, marca v3).
// Ideas de la Presentación de NotebookLM (cuaderno R004), redibujadas en la marca y pasadas por la Voz de Elmer.
// Uso: node carruseles/r004-ciclo-de-vida.mjs <carpeta de salida> <prefijo>
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'node:fs';
const NM = process.env.FONTSOURCE || new URL('../node_modules/@fontsource', import.meta.url).pathname;
import { resolve } from 'node:path';
const OUT = resolve(process.argv[2] || './out');
const PREFIJO = process.argv[3] || 'R004-carrusel';
mkdirSync(OUT, { recursive: true });

const C={marino:"#0B1F3A",oscuro:"#07152A",claro:"#1E3A5F",am:"#F5B800",amC:"#FFD84D",bl:"#FFFFFF",gris:"#A9B4C4",verde:"#3DDC84",rojo:"#FF5A5F"};
const BEBAS="'Bebas Neue',Impact,sans-serif", INTER="Inter,system-ui,sans-serif";
const W=1080, H=1350, N=8;

// ---------- primitivas SVG ----------
const R=(x,y,w,h,o={})=>{const {rx=16,fill='none',stroke='none',sw=0,op=1}=o;return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" opacity="${op}"/>`};
const L=(x1,y1,x2,y2,o={})=>{const {stroke=C.gris,sw=4,op=1,cap='round',dash=''}=o;return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="${cap}" opacity="${op}" ${dash?`stroke-dasharray="${dash}"`:''}/>`};
const P=(d,o={})=>{const {stroke=C.bl,sw=5,fill='none',op=1}=o;return `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" opacity="${op}"/>`};
const Ci=(x,y,r,o={})=>{const {fill='none',stroke='none',sw=0,op=1}=o;return `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" opacity="${op}"/>`};
const G=(inner,{x=0,y=0,s=1,op=1}={})=>`<g transform="translate(${x} ${y}) scale(${s})" opacity="${op}">${inner}</g>`;
const T=(x,y,s,o={})=>{const {size=40,font=BEBAS,fill=C.bl,anchor='start',weight=400,ls=0,op=1}=o;return `<text x="${x}" y="${y}" font-family="${font}" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}" letter-spacing="${ls}" opacity="${op}">${s}</text>`};

// íconos de la marca (los mismos del short R004, 100x100)
const I={
  phone:(c)=>R(22,4,56,92,{rx:12,stroke:c,sw:5})+L(42,14,58,14,{stroke:c,sw:4})+Ci(50,84,4,{fill:c}),
  pipe:(c)=>P('M6 36 L54 36 C70 36 76 44 76 60 L76 94',{stroke:c,sw:14})+P('M6 36 L54 36 C70 36 76 44 76 60 L76 94',{stroke:C.oscuro,sw:5})+R(2,24,12,24,{rx:3,fill:c})+R(64,86,24,12,{rx:3,fill:c}),
  gear:(c)=>{let d='';for(let k=0;k<8;k++){const a=k*Math.PI/4;d+=L(50+30*Math.cos(a),50+30*Math.sin(a),50+44*Math.cos(a),50+44*Math.sin(a),{stroke:c,sw:12,cap:'butt'});}return d+Ci(50,50,30,{stroke:c,sw:6,fill:C.oscuro})+Ci(50,50,10,{fill:c})},
  chart:(c,acc=C.am)=>L(12,88,92,88,{stroke:c,sw:5})+R(20,58,14,30,{rx:3,fill:c})+R(43,40,14,48,{rx:3,fill:c})+R(66,22,14,66,{rx:3,fill:acc}),
  db:(c)=>`<ellipse cx="50" cy="20" rx="36" ry="12" fill="none" stroke="${c}" stroke-width="5"/>`+P('M14 20 L14 80 C14 96 86 96 86 80 L86 20',{stroke:c,sw:5})+P('M14 50 C14 66 86 66 86 50',{stroke:c,sw:4,op:.8}),
  bookmark:(c)=>P('M24 8 L76 8 L76 94 L50 72 L24 94 Z',{stroke:c,sw:6}),
};
const ICONO_MARCA=(w)=>`<svg width="${w}" height="${w*100/120}" viewBox="0 0 120 100" fill="none"><g stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M33 10 C21 10 23 26 23 38 C23 45 19 50 11 50 C19 50 23 55 23 62 C23 74 21 90 33 90"/><path d="M87 10 C99 10 97 26 97 38 C97 45 101 50 109 50 C101 50 97 55 97 62 C97 74 99 90 87 90"/></g><g transform="translate(-7.556 -17.222) scale(0.26389)"><g fill="${C.am}"><path d="M184 185A72 25 0 0 0 328 185V223A72 25 0 0 1 184 223Z"/><path d="M184 237A72 25 0 0 0 328 237V275A72 25 0 0 1 184 275Z"/><path d="M184 289A72 25 0 0 0 328 289V327A72 25 0 0 1 184 327Z"/></g><ellipse cx="256" cy="185" rx="72" ry="25" fill="${C.amC}"/></g></svg>`;

// ---------- el diagrama del ciclo (igual que en el short: 4 etapas sobre la base de almacenamiento) ----------
const ETAPAS=[['GENERACIÓN','phone'],['INGESTA','pipe'],['TRANSFORMACIÓN','gear'],['SERVING','chart']];
function Ciclo({x0=100,y=0,w=880,on=-1,base=false,dim=true}={}){
  const n=4, gap=36, tw=(w-gap*(n-1))/n, th=150;
  let s='';
  ETAPAS.forEach(([lab,ic],k)=>{
    const x=x0+k*(tw+gap), act=(k===on), apag=dim && on!==-1 && !act || (dim && base && !act);
    const st=act?C.am:(apag?C.claro:C.gris), ic_c=act?C.am:(apag?'#5d7392':C.bl);
    s+=R(x,y,tw,th,{rx:22,fill:act?'#16304f':C.oscuro,stroke:st,sw:act?6:3});
    s+=G(I[ic](ic_c,act?C.amC:(apag?'#5d7392':C.am)),{x:x+tw/2-34,y:y+22,s:0.68});
    s+=T(x+tw/2,y+th-20,lab,{size:lab.length>11?25:30,anchor:'middle',fill:act?C.am:(apag?'#6f84a3':C.bl),ls:1.5});
    if(k<n-1){const ax=x+tw+4, ay=y+th/2;s+=L(ax,ay,ax+gap-10,ay,{stroke:apag&&!act?C.claro:C.gris,sw:4})+P(`M${ax+gap-18} ${ay-7} L${ax+gap-9} ${ay} L${ax+gap-18} ${ay+7}`,{stroke:apag&&!act?C.claro:C.gris,sw:4});}
  });
  // base
  const by=y+th+26, bh=96, bon=base, bapag=dim && on!==-1;
  s+=R(x0,by,w,bh,{rx:22,fill:bon?'#16304f':C.oscuro,stroke:bon?C.am:(bapag?C.claro:C.gris),sw:bon?6:3});
  s+=G(I.db(bon?C.am:(bapag?'#5d7392':C.bl)),{x:x0+30,y:by+18,s:0.6});
  s+=T(x0+w/2,by+bh/2+14,'ALMACENAMIENTO · LA BASE DE TODO',{size:38,anchor:'middle',fill:bon?C.am:(bapag?'#6f84a3':C.bl),ls:2});
  // pilares que bajan de cada etapa a la base
  ETAPAS.forEach((_,k)=>{const cx=x0+k*(tw+gap)+tw/2;s+=L(cx,y+th+3,cx,by-3,{stroke:bon?C.am:C.claro,sw:5,op:bon?1:0.9});});
  return s;
}

// ---------- marco de cada lámina ----------
function fondo(){
  const dots=(c,r,p)=>`radial-gradient(circle at ${p/2}px ${p/2}px, ${c} ${r}px, transparent ${r+0.8}px)`;
  return `<div style="position:absolute;inset:0;background:${C.marino}">
   <div style="position:absolute;inset:0;background:radial-gradient(900px 900px at 70% 38%, rgba(169,180,196,0.10), transparent 70%)"></div>
   <div style="position:absolute;inset:0;background-image:${dots('rgba(169,180,196,0.18)',1.6,36)};background-size:36px 36px"></div>
   <div style="position:absolute;inset:0;background:radial-gradient(ellipse 95% 75% at 50% 45%, transparent 50%, rgba(7,21,42,0.8) 100%)"></div>
   <div style="position:absolute;left:0;top:0;bottom:0;width:24px;background:${C.am}"></div></div>`;
}
const header=(i)=>`<div style="position:absolute;left:88px;top:66px;display:flex;align-items:center;gap:16px">${ICONO_MARCA(70)}<div style="font-family:${BEBAS};font-size:36px;line-height:0.92;letter-spacing:0.05em;color:#fff"><div>EL INGENIERO</div><div style="color:${C.am}">DE DATOS</div></div></div>
 <div style="position:absolute;right:80px;top:84px;font-family:${BEBAS};font-size:34px;letter-spacing:0.12em;color:${C.gris}">${String(i).padStart(2,'0')} / ${String(N).padStart(2,'0')}</div>`;
const footer=(i)=>`<div style="position:absolute;left:88px;right:80px;bottom:62px;display:flex;justify-content:space-between;align-items:center">
 <div style="font-family:${INTER};font-weight:600;font-size:26px;color:${C.gris}">elingenierodedatos.com</div>
 ${i<N?`<div style="font-family:${BEBAS};font-size:38px;letter-spacing:0.1em;color:${C.am}">DESLIZA →</div>`:''}</div>`;
const svg=(inner,h=H)=>`<svg width="${W}" height="${h}" viewBox="0 0 ${W} ${h}" style="position:absolute;left:0;top:0">${inner}</svg>`;
const pregunta=(q,top)=>`<div style="position:absolute;left:88px;right:80px;top:${top}px;padding:30px 40px 34px 40px;border-radius:24px;background:linear-gradient(180deg,#173459,#081830);border:3px solid ${C.claro};border-left:10px solid ${C.am};box-shadow:0 16px 36px rgba(1,7,15,0.6)">
 <div style="font-family:${BEBAS};font-size:34px;letter-spacing:0.12em;color:${C.am};margin-bottom:10px">PREGÚNTATE</div>
 <div style="font-family:${INTER};font-weight:600;font-size:40px;line-height:1.22;color:#fff">${q}</div></div>`;

function lamina(i, cuerpo){
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Bebas Neue';src:url(file://${NM}/bebas-neue/files/bebas-neue-latin-400-normal.woff2) format('woff2');font-weight:400}
@font-face{font-family:'Inter';src:url(file://${NM}/inter/files/inter-latin-400-normal.woff2) format('woff2');font-weight:400}
@font-face{font-family:'Inter';src:url(file://${NM}/inter/files/inter-latin-600-normal.woff2) format('woff2');font-weight:600}
@font-face{font-family:'Inter';src:url(file://${NM}/inter/files/inter-latin-700-normal.woff2) format('woff2');font-weight:700}
@font-face{font-family:'Inter';src:url(file://${NM}/inter/files/inter-latin-800-normal.woff2) format('woff2');font-weight:800}
html,body{margin:0;padding:0}
#s{position:relative;width:${W}px;height:${H}px;overflow:hidden}
</style></head><body><div id="s">${fondo()}${cuerpo}${header(i)}${footer(i)}</div></body></html>`;
}
const titulo=(t,top,size=118,col=C.am)=>`<div style="position:absolute;left:88px;right:80px;top:${top}px;font-family:${BEBAS};font-size:${size}px;line-height:0.95;letter-spacing:0.02em;color:${col}">${t}</div>`;
const texto=(t,top,size=46,w=700)=>`<div style="position:absolute;left:88px;right:96px;top:${top}px;font-family:${INTER};font-weight:${w};font-size:${size}px;line-height:1.25;color:#fff">${t}</div>`;
const kicker=(t,top)=>`<div style="position:absolute;left:88px;top:${top}px;font-family:${BEBAS};font-size:36px;letter-spacing:0.14em;color:${C.gris}">${t}</div>`;

// ---------- las 8 láminas ----------
const L1=()=>{
  // línea de pulso: el ciclo "vivo"
  let pulso=`M88 0 L560 0 L590 -40 L622 70 L660 -120 L700 90 L730 -30 L760 0 L1080 0`;
  const s=svg(G(P(pulso,{stroke:C.am,sw:9})+Ci(88,0,14,{fill:C.am}),{y:735}));
  return s+titulo('TU TRABAJO NO ES<br>MOVER DATOS<br>DE UN LADO A OTRO.',230,132,C.bl)
   +`<div style="position:absolute;left:88px;right:96px;top:900px;font-family:${INTER};font-weight:400;font-size:52px;line-height:1.28;color:#fff"><b style="font-weight:800;color:${C.am}">Es cuidar todo su ciclo de vida.</b><br>Si solo piensas en herramientas, tus pipelines van a colapsar.</div>`;
};
const etapa=(i,num,nom,frase,q,on)=>svg(Ciclo({y:600,on}))+kicker(`ETAPA ${num} DE 4`,214)+titulo(nom,256,124)+texto(frase,392,44)+pregunta(q,940);
const L2=()=>etapa(2,1,'GENERACIÓN','Los datos nacen aquí, pero tú no controlas la fuente. Si la fuente cambia, tus procesos se rompen.','¿Con qué frecuencia, volumen y formato se generan estos datos?',0);
const L3=()=>etapa(3,2,'INGESTA','Llevar los datos del origen al almacenamiento es la fase más propensa a fallar.','¿De verdad necesitas streaming o te basta con batch?',1);
const L4=()=>etapa(4,3,'TRANSFORMACIÓN','Los datos crudos no le sirven al negocio. Aquí limpias, ordenas y aplicas sus reglas.','¿Qué valor le da al negocio transformar estos datos?',2);
const L5=()=>etapa(5,4,'SERVING','Si nadie usa los datos para analytics o machine learning, todo el esfuerzo fue en vano.','¿Tienen la calidad suficiente para que el negocio decida con confianza?',3);
const L6=()=>svg(Ciclo({y:600,base:true}))+kicker('¿NOTASTE QUE FALTABA UNA?',214)+titulo('ALMACENAMIENTO',256,124)+texto('No es un paso más. Es la base que sostiene a las otras cuatro etapas y define el rendimiento de todo el ciclo.',392,44)+pregunta('¿Tu almacenamiento aguanta la escala que viene sin volverse un cuello de botella?',940);
const L7=()=>{
  const U=['SEGURIDAD','GESTIÓN DE DATOS','DATAOPS','ARQUITECTURA','ORQUESTACIÓN','INGENIERÍA DE SOFTWARE'];
  let s=G(Ciclo({y:0,dim:false}),{x:0,y:0});
  // undercurrents: barras que corren por debajo de todo
  U.forEach((u,k)=>{const y=300+k*62;
    s+=R(100,y,880,50,{rx:12,fill:C.oscuro,stroke:k%2?C.claro:'#2b4d78',sw:3});
    s+=R(100,y,10,50,{rx:4,fill:C.am});
    s+=T(140,y+37,String(k+1).padStart(2,'0'),{size:32,fill:C.am,ls:2})+T(196,y+37,u,{size:34,fill:C.bl,ls:2});
  });
  return svg(G(s,{y:545}))+kicker('POR DEBAJO DE TODO',214)+titulo('LOS 6 UNDERCURRENTS',256,118)+texto('Atraviesan las cinco etapas. Véanlo como los cimientos de una casa: no se ven, pero lo sostienen todo.',380,34,600);
};
const L8=()=>{
  const s=svg(G(I.bookmark(C.am),{x:868,y:610,s:1.2}));
  return s+titulo('NO TE ENAMORES<br>DE UNA HERRAMIENTA.',250,126,C.bl)
   +`<div style="position:absolute;left:88px;right:250px;top:520px;font-family:${INTER};font-weight:800;font-size:56px;line-height:1.18;color:${C.am}">Domina el ciclo de vida de los datos.</div>`
   +`<div style="position:absolute;left:88px;right:96px;top:760px;padding:30px 36px;border-radius:24px;background:linear-gradient(180deg,#173459,#081830);border:3px solid ${C.claro};font-family:${INTER};font-weight:600;font-size:40px;line-height:1.25;color:#fff">Guarda este carrusel y revísalo antes de diseñar tu próximo pipeline.</div>`
   +`<div style="position:absolute;left:0;right:0;top:1010px;display:flex;flex-direction:column;align-items:center;gap:18px">
      <div style="display:flex;align-items:center;gap:18px">${ICONO_MARCA(96)}<div style="font-family:${BEBAS};font-size:52px;line-height:0.92;letter-spacing:0.05em;color:#fff"><div>EL INGENIERO</div><div style="color:${C.am}">DE DATOS</div></div></div>
    </div>`;
};

const LAMINAS=[L1,L2,L3,L4,L5,L6,L7,L8];
const browser=await chromium.launch();
const page=await browser.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
for(let k=0;k<LAMINAS.length;k++){
  const html=lamina(k+1,LAMINAS[k]());
  const f=`/tmp/lamina-${k+1}.html`; writeFileSync(f,html);
  await page.goto('file://'+f); await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:`${OUT}/${PREFIJO}-${String(k+1).padStart(2,'0')}-1080x1350.png`,clip:{x:0,y:0,width:W,height:H}});
}
await browser.close();
console.log('ok');
