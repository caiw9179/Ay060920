leaper=open('leaper.svgfrag').read()
html=r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>点亮动画审核 · 小猫的AJ专属赛博图鉴</title>
<style>
:root{
  --mute:#555; --dim:#888; --soft:#bdbdbd; --fg:#fff;
  --sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,"JetBrains Mono",Consolas,"Noto Sans Mono CJK SC",monospace;
  --ease:cubic-bezier(.2,.8,.2,1);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000;color:var(--fg);font-family:var(--sans);-webkit-font-smoothing:antialiased}
body.all{background:#0b0b0b}
.stage{display:flex;gap:15px;justify-content:center;padding:28px 0 30px}
body.solo .stage{padding:0;gap:0}
.col{display:flex;flex-direction:column;align-items:center;gap:14px}
.lbl{width:390px;height:56px;font-family:var(--mono);font-size:13px;color:#9a9a9a;letter-spacing:.12em;text-align:center;line-height:1.7}
.lbl b{color:#fff;font-family:var(--sans);font-size:15px;letter-spacing:.06em;display:block}
body.solo .lbl{display:none}
.phone{width:390px;height:844px;background:#000;position:relative;overflow:hidden}
body.all .phone{border-radius:34px;outline:1px solid #222}
/* header (same as app) */
header{padding:22px 20px 6px;display:flex;justify-content:space-between}
h1{font-size:19px;font-weight:600;letter-spacing:.04em;display:flex;align-items:center;gap:9px}
h1 .cat{width:30px;height:22px;color:#fff;overflow:visible}
.brand p{margin-top:6px;font-family:var(--mono);font-size:11px;color:var(--mute);letter-spacing:.08em}
.brand p b{color:var(--soft);font-weight:500}
.dots{color:#888;font-size:18px;letter-spacing:2px;padding-top:2px}
.nav{display:flex;align-items:center;padding:10px 0 12px}
.tabs{flex:1;display:flex;gap:22px;padding:0 20px}
.tab{font-size:16px;font-weight:500;color:#666;padding:6px 0;letter-spacing:.03em}
.tab.on{color:#fff;font-weight:700}
.tab .n{font-family:var(--mono);font-size:10px;font-weight:400;margin-left:3px;vertical-align:top;opacity:.6}
.plus{width:40px;margin-right:10px;text-align:center;font-size:24px;font-weight:300}
.hall{padding:2px 20px 14px;display:flex;justify-content:space-between;align-items:baseline;font-family:var(--mono);font-size:11px;color:var(--mute);letter-spacing:.06em}
.bar{flex:1;height:1px;background:#1c1c1c;margin:0 12px;position:relative;align-self:center}
.bar i{position:absolute;left:0;top:0;height:1px;background:#fff;width:33%}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;padding:0 16px}
/* card (same as app) */
.card{position:relative;aspect-ratio:1/1;border-radius:14px;overflow:hidden;background:#1c1c1e;isolation:isolate}
.jm{position:absolute;top:11px;left:11px;width:15px;height:14px;color:#2c2c2e;z-index:0}
.offimg{position:absolute;left:9%;right:9%;top:16%;bottom:26%;display:grid;place-items:center}
.offimg img{max-width:100%;max-height:100%;object-fit:contain;filter:grayscale(1) brightness(1.05) contrast(.95);opacity:.3}
.corner{position:absolute;top:10px;right:10px;font-family:var(--mono);font-size:9px;color:#3a3a3d;letter-spacing:.1em;z-index:3}
.uname{position:absolute;left:12px;right:12px;bottom:11px;font-size:11px;font-weight:500;color:#6a6a6e;z-index:3}
.ph{position:absolute;inset:0;z-index:1}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.grad{position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 72%,rgba(0,0,0,.92) 100%)}
.tag{position:absolute;left:12px;right:12px;bottom:11px;z-index:3}
.tag .nm{font-size:13px;font-weight:600;line-height:1.3;color:#fff}
.tag .dt{font-family:var(--mono);font-size:10px;margin-top:3px;letter-spacing:.06em;color:rgba(255,255,255,.62)}
/* animated-card layers */
.fx{position:absolute;inset:0;z-index:4;pointer-events:none;opacity:0}
.scan{position:absolute;left:0;right:0;top:0;height:1px;z-index:4;pointer-events:none;opacity:0;background:rgba(255,255,255,.95);box-shadow:0 0 6px rgba(255,255,255,.35)}
.scan::before{content:"";position:absolute;left:0;right:0;bottom:1px;height:36px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.07))}
.target .ph,.target .grad,.target .tag{opacity:0}
.note{max-width:1200px;margin:0 auto;padding:0 40px 30px;font-family:var(--mono);font-size:11px;color:#555;line-height:1.9;text-align:center}
body.solo .note{display:none}
</style></head>
<body>
<svg width="0" height="0" style="position:absolute"><defs>__LEAPER__</defs></svg>
<div class="stage" id="stage"></div>
<p class="note">右上角卡片在循环演示：灰卡（官方商品图 30% 灰度）→ 点亮为实拍图（此处实拍图为占位：官方图彩色版 + 深灰背景）。系统开启「减少动态效果」时三版都退化为 200ms 淡入。</p>
<script>
const EASE='cubic-bezier(.22,1,.36,1)';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
CSS.registerProperty&&CSS.registerProperty({name:'--p',syntax:'<percentage>',inherits:false,initialValue:'0%'});
const V={
 A:{t:'A · 斜扫',d:'柔边遮罩左下→右上扫开，1px 光边随行淡出 · 720ms'},
 B:{t:'B · 显影',d:'饱和度 0→1，缩放 1.02→1，文字上浮 8px · 900ms'},
 C:{t:'C · 扫描线',d:'细光线自上而下扫过一次，色彩随线填充 · 800ms'},
};
const jm='<svg class="jm" viewBox="5 13.06 240 223.88"><use href="#leaper"/></svg>';
function unlit(img,name,target){return `<div class="card${target?' target':''}">${jm}<div class="offimg"><img src="../official/${img}.webp"></div><span class="corner">待点亮</span><div class="uname">${name}</div>`+(target?`<div class="ph"><img src="ph-chicago.jpg"></div><div class="grad"></div><div class="tag"><div class="nm">AJ1 芝加哥</div><div class="dt">2026.10.24</div></div><div class="fx"></div><div class="scan"></div>`:'')+`</div>`}
function lit(photo,name,date){return `<div class="card"><div class="ph"><img src="${photo}"></div><div class="grad"></div><div class="tag"><div class="nm">${name}</div><div class="dt">${date}</div></div></div>`}
function phone(k){return `<div class="col"><div class="lbl"><b>${V[k].t}</b>${V[k].d}</div><div class="phone" id="ph${k}">
<header><div class="brand"><h1><svg class="cat" viewBox="8.5 22 48 35"><g fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"><path d="M15.6 47.6 Q11 46 11.6 40.6 L12.4 34 L10.6 27 L16 30.2 Q18.4 29 21 29.4 L24.6 25.4 L24.6 30.6 Q33 23.6 43 25.6 Q53.6 28 54 39 Q54.2 47.6 44 48.6 L20 48.6"/><path d="M52.6 44.6 Q51.6 54.4 36 54.6 Q26.4 54.6 22.8 51.2"/><path d="M14.8 38.2 Q16.6 39.8 18.6 38.4"/></g></svg><span>小猫的AJ专属赛博图鉴</span></h1><p>已点亮 <b>02</b> / 06 · 1 个展厅</p></div><div class="dots">···</div></header>
<div class="nav"><div class="tabs"><span class="tab on">AJ1<span class="n">6</span></span></div><span class="plus">+</span></div>
<div class="hall"><span>AJ1 展厅</span><span class="bar"><i></i></span><span>2/6 已点亮</span></div>
<div class="grid">${lit('ph-unc.jpg','AJ1 北卡蓝','2024.05.20')}${unlit('aj1-chicago','AJ1 芝加哥',true)}${unlit('aj1-bred','AJ1 禁穿 Bred')}${unlit('aj1-royal','AJ1 皇家蓝 Royal')}${unlit('aj1-black-toe','AJ1 黑脚趾')}${unlit('aj1-unc','AJ1 北卡蓝 UNC')}</div>
</div></div>`}

/* each builder returns a list of Animations (paused) and total length */
function build(k,card){
 const q=s=>card.querySelector(s), A=[];
 const ph=q('.ph'),img=q('.ph img'),grad=q('.grad'),tag=q('.tag'),fx=q('.fx'),scan=q('.scan');
 const un=[q('.offimg'),q('.corner'),q('.uname'),q('.jm')];
 const an=(el,kf,o)=>{const a=el.animate(kf,Object.assign({fill:'both',easing:EASE},o));a.pause();A.push(a);return a};
 if(reduce){
   [ph,grad,tag].forEach(e=>an(e,[{opacity:0},{opacity:1}],{duration:200,easing:'ease-out'}));
   return {A,len:200};
 }
 if(k==='A'){
   const D=720, ease='cubic-bezier(.5,.05,.2,1)';
   ph.style.opacity=1;
   const m='linear-gradient(45deg,#000 calc(var(--p) - 16%),transparent var(--p))';
   ph.style.webkitMaskImage=ph.style.maskImage=m; grad.style.webkitMaskImage=grad.style.maskImage=m;
   an(ph,[{'--p':'0%'},{'--p':'118%'}],{duration:D,easing:ease});
   an(grad,[{'--p':'0%'},{'--p':'118%'}],{duration:D,easing:ease}); grad.style.opacity=1;
   // light edge: 1px crisp line + faint glow behind, rides the front then fades
   fx.style.background='linear-gradient(45deg,transparent calc(var(--p) - 28%),rgba(255,255,255,.06) calc(var(--p) - 8.4%),transparent calc(var(--p) - 8.4%),rgba(255,255,255,.85) calc(var(--p) - 8.1%),rgba(255,255,255,.85) calc(var(--p) - 7.9%),transparent calc(var(--p) - 7.6%))';
   an(fx,[{'--p':'0%'},{'--p':'118%'}],{duration:D,easing:ease});
   an(fx,[{opacity:0},{opacity:1,offset:.1},{opacity:.9,offset:.55},{opacity:0}],{duration:D,easing:'linear'});
   un.forEach(e=>an(e,[{opacity:1},{opacity:0}],{duration:220,delay:D*.28,easing:'linear'}));
   an(tag,[{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:420,delay:D*.55});
   return {A,len:D*.55+420};
 }
 if(k==='B'){
   const D=900;
   an(q('.offimg'),[{opacity:1,filter:'blur(0)'},{opacity:0,filter:'blur(2px)'}],{duration:500,easing:'cubic-bezier(.4,0,.2,1)'});
   [q('.corner'),q('.uname'),q('.jm')].forEach(e=>an(e,[{opacity:1},{opacity:0}],{duration:260,easing:'linear'}));
   an(ph,[{opacity:0},{opacity:1}],{duration:420,easing:'cubic-bezier(.4,0,.2,1)'});
   an(img,[{filter:'saturate(0) brightness(.82)',transform:'scale(1.02)'},{filter:'saturate(1) brightness(1)',transform:'scale(1)'}],{duration:D});
   an(grad,[{opacity:0},{opacity:1}],{duration:500,delay:380});
   an(tag,[{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:520,delay:380});
   return {A,len:D};
 }
 if(k==='C'){
   const D=800, ease='cubic-bezier(.45,.05,.25,1)';
   ph.style.opacity=1; grad.style.opacity=1;
   [ph,grad].forEach(e=>an(e,[{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)'}],{duration:D,easing:ease}));
   const H=card.offsetHeight;
   an(scan,[{transform:'translateY(0)'},{transform:`translateY(${H-1}px)`}],{duration:D,easing:ease});
   an(scan,[{opacity:0},{opacity:1,offset:.06},{opacity:1,offset:.62},{opacity:0,offset:.86},{opacity:0}],{duration:D,easing:'linear'});
   un.forEach(e=>an(e,[{opacity:1},{opacity:0}],{duration:180,delay:D*.55,easing:'linear'}));
   an(tag,[{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:420,delay:D*.62});
   return {A,len:D*.62+420};
 }
}
const P=new URLSearchParams(location.search), mode=(P.get('v')||'all').toUpperCase();
const keys=mode==='ALL'?['A','B','C']:[mode];
document.body.className=keys.length>1?'all':'solo';
document.getElementById('stage').innerHTML=keys.map(phone).join('');
const runs=[];
addEventListener('load',()=>{
 keys.forEach(k=>{const card=document.querySelector('#ph'+k+' .target');runs.push(Object.assign({card,k},build(k,card)));});
 window.seek=t=>runs.forEach(r=>r.A.forEach(a=>{a.currentTime=t}));       // for frame capture
 window.lenOf=k=>runs.find(r=>r.k===k).len;
 const HOLD0=+(P.get('h0')||1200), HOLD1=1300, BACK=350;
 const L=Math.max(...runs.map(r=>r.len)), CYC=HOLD0+L+HOLD1+BACK;
 window.CYC=CYC;
 // deterministic frame renderer (used for video capture): same timeline as the live loop
 window.frameAt=T=>{const t=T%CYC; runs.forEach(r=>{r.card.style.transition='none';
   let op=1; if(t<BACK) op=t/BACK; else if(t>CYC-BACK) op=1-(t-(CYC-BACK))/BACK;
   const at=(t<BACK||t>CYC-BACK)?(t<BACK?0:L+HOLD1):Math.max(0,t-HOLD0);
   r.A.forEach(a=>{a.currentTime=(t>CYC-BACK)?1e5:(t<HOLD0?0:at)}); r.card.style.opacity=op;});};
 if(P.get('static')) {window.ready=true;return}
 function cycle(){
   runs.forEach(r=>{r.A.forEach(a=>{a.currentTime=0;a.pause()});r.card.style.transition=`opacity ${BACK}ms linear`;r.card.style.opacity=1});
   setTimeout(()=>{runs.forEach(r=>r.A.forEach(a=>a.play()));
     const L=Math.max(...runs.map(r=>r.len));
     setTimeout(()=>{ // soft reset back to grey for the loop (review-only)
       runs.forEach(r=>{r.card.style.transition=`opacity ${BACK}ms linear`;r.card.style.opacity=0});
       setTimeout(cycle,BACK);
     },L+HOLD1);
   },HOLD0);
 }
 cycle(); window.ready=true;
});
</script></body></html>'''
open('anim-review.html','w').write(html.replace('__LEAPER__',leaper))
