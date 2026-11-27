(function(){
"use strict";
const root=document.getElementById("ari-market-intelligence");
if(!root)return;
const url=root.dataset.feed;
const el=(tag,text)=>{const n=document.createElement(tag);if(text!=null)n.textContent=text;return n;};
const add=(parent,tag,text)=>{const n=el(tag,text);parent.append(n);return n;};
const num=n=>n==null?"—":Number(n).toLocaleString("en-US");
function table(parent,headers,rows){
 const wrap=add(parent,"div");wrap.style.overflowX="auto";
 const t=add(wrap,"table"), head=add(add(t,"thead"),"tr");
 headers.forEach(h=>add(head,"th",h));
 const body=add(t,"tbody");
 rows.forEach(row=>{const tr=add(body,"tr");row.forEach(v=>add(tr,"td",v));});
}
function render(d){
 if(d.schema_version!==1||!d.latest||!Array.isArray(d.trends))throw Error("Invalid feed");
 root.replaceChildren();
 add(root,"h2","Market Overview");
 add(root,"p","Latest observed scan: "+d.as_of.slice(0,10)+(d.latest.complete?"":" · Partial source coverage"));
 const cards=add(root,"div");cards.style.cssText="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px";
 [["Observed active listings",num(d.latest.observed_active_listings)],["Mapped countries",num(d.latest.observed_countries.length)]].forEach(([label,value])=>{const c=add(cards,"div");c.style.cssText="border:1px solid #dbe2ec;border-radius:10px;padding:14px";add(c,"small",label);add(c,"h3",value);});
 table(root,["Vendor","Observed active","Source status"],Object.entries(d.latest.vendors).map(([v,s])=>[v,num(s.active_listings),s.source_status]));
 add(root,"h2","Weekly Market Pulse");
 add(root,"p","Seven days ending at the latest scan. Dashes indicate insufficient comparable history, not zero activity.");
 table(root,["Vendor","New","Archived","Reopened","Verified scans"],Object.entries(d.weekly_pulse).map(([v,s])=>[v,num(s.events?.new),num(s.events?.archived),num(s.events?.reopened),num(s.verified_scans)]));
 add(root,"h2","Historical Market Trends");
 add(root,"p","Observed listings by vendor. Missing source observations are not treated as zero.");
 const vendors=[...new Set(d.trends.flatMap(s=>Object.keys(s.vendors)))];
 const ns="http://www.w3.org/2000/svg", svg=document.createElementNS(ns,"svg");svg.setAttribute("viewBox","0 0 640 280");svg.setAttribute("role","img");svg.setAttribute("aria-label","Historical observed listings by vendor");svg.style.width="100%";root.append(svg);
 const times=d.trends.map(s=>Date.parse(s.at)), lo=Math.min(...times),hi=Math.max(...times),max=Math.max(1,...d.trends.flatMap(s=>Object.values(s.vendors).filter(v=>v!=null)));
 const x=i=>50+560*(times[i]-lo)/(hi-lo||1), y=v=>230-200*v/max;
 function shape(tag,attrs,text){const n=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!=null)n.textContent=text;svg.append(n);}
 for(let i=0;i<=4;i++){const v=max*i/4;shape("line",{x1:50,x2:610,y1:y(v),y2:y(v),stroke:"#dbe2ec"});shape("text",{x:45,y:y(v)+4,"text-anchor":"end","font-size":10,fill:"currentColor"},Math.round(v));}
 const colors=["#2563eb","#059669","#b45309","#9333ea","#64748b"];
 vendors.forEach((v,j)=>{let path="",started=false;d.trends.forEach((s,i)=>{const n=s.vendors[v];if(n==null){started=false;return;}path+=(started?" L":" M")+x(i)+" "+y(n);started=true;});shape("path",{d:path,stroke:colors[j%colors.length],fill:"none","stroke-width":2});});
 shape("text",{x:50,y:252,"font-size":11,fill:"currentColor"},d.trends[0].at.slice(0,10));shape("text",{x:610,y:252,"text-anchor":"end","font-size":11,fill:"currentColor"},d.trends.at(-1).at.slice(0,10));
 const legend=add(root,"p");vendors.forEach((v,i)=>{const s=add(legend,"span","● "+v+"  ");s.style.color=colors[i%colors.length];});
 const detail=add(root,"details");add(detail,"summary","View historical observations");table(detail,["Date",...vendors],d.trends.map(s=>[s.at,...vendors.map(v=>num(s.vendors[v]))]));
}
fetch(url,{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("Feed unavailable");return r.json();}).then(render).catch(()=>{root.textContent="Market analytics are temporarily unavailable. The vacancy directory remains available.";});
})();