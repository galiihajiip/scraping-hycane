"""Interactive dashboard: outputs/dashboard/index.html (self-contained data; Plotly.js from cdnjs)."""
from __future__ import annotations

import json

import pandas as pd

from src.utils.common import ROOT

OUT = ROOT / "outputs" / "dashboard"


def main():
    g = pd.read_parquet(ROOT / "data" / "gold" / "hycane_social_listening_gold.parquet")
    ps = ROOT / "outputs" / "tables" / "persona_summary.csv"
    pname = dict(zip(*pd.read_csv(ps)[["persona_cluster", "persona_name"]].T.values)) if ps.exists() else {}
    d = pd.DataFrame({
        "p": g.platform, "f": g.source_family, "m": g.created_at.str[:7].fillna("unknown"),
        "l": g.text_language.where(g.text_language.isin(["en", "id", "ms", "de", "es"]), "other"),
        "c": g.country.fillna("unknown"), "x": g.author_experience_signal, "i": g.intent, "s": g.sentiment,
        "t": g.topic_label.fillna("(not in topic model)").astype(str),
        "r": g.persona_cluster.map(lambda v: f"P{int(v)} {pname.get(int(v), '')}" if pd.notna(v) else "(none)"),
        "pp": g.pain_points.fillna(""), "ft": g.feature_mentions.fillna(""), "v": g.is_customer_voice.astype(int),
        "sc": g.in_core_scope.astype(int), "u": g.source_url.fillna(""),
        "tx": g.text_model.str.slice(0, 220).str.replace(r"\s+", " ", regex=True)})
    res = json.loads((ROOT / "outputs" / "tables" / "analysis_results.json").read_text())
    # keep the page small: snippets/URLs only for a seeded random 6,000 rows; categorical columns dictionary-encoded
    keep_txt = d.sample(min(6000, len(d)), random_state=42).index
    d.loc[~d.index.isin(keep_txt), ["tx", "u"]] = ""
    data, dicts = {}, {}
    for c in d.columns:
        if c in ("v", "sc"):
            data[c] = d[c].tolist()
        else:
            cats = pd.Categorical(d[c].astype(str))
            dicts[c] = list(cats.categories)
            data[c] = cats.codes.tolist()
    data = {"cols": data, "dicts": dicts}
    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace(
        "__META__", json.dumps({"counts": res["counts"], "tf": res["timeframe_customer_voice"]}))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(html)
    print("dashboard rows", len(d), "size MB", round(len(html) / 1e6, 2))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HYCANE Social Listening</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.34.0/plotly.min.js"></script>
<style>
:root{--surface:#fcfcfb;--panel:#ffffff;--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--grid:#e6e5e1;--s1:#2a78d6;--pos:#2a78d6;--neg:#e34948;--neu:#b9b8b2;--mix:#4a3aa7;--amb:#dcdbd6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--surface:#1a1a19;--panel:#222220;--ink:#ffffff;--ink2:#c3c2b7;--muted:#9a998f;--grid:#383835;--s1:#3987e5;--pos:#3987e5;--neg:#e66767;--neu:#77766f;--mix:#9085e9;--amb:#4a4a46}}
:root[data-theme="dark"]{--surface:#1a1a19;--panel:#222220;--ink:#ffffff;--ink2:#c3c2b7;--muted:#9a998f;--grid:#383835;--s1:#3987e5;--pos:#3987e5;--neg:#e66767;--neu:#77766f;--mix:#9085e9;--amb:#4a4a46}
body{margin:0;background:var(--surface);color:var(--ink);font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 16px 8px;max-width:1300px;margin:auto}h1{font-size:20px;margin:0 0 4px}.sub{color:var(--ink2);font-size:13px}
.filters{display:flex;flex-wrap:wrap;gap:8px;padding:10px 16px;max-width:1300px;margin:auto;position:sticky;top:0;background:var(--surface);z-index:5;border-bottom:1px solid var(--grid)}
.filters label{font-size:11px;color:var(--ink2);display:flex;flex-direction:column;gap:2px}
select,input{background:var(--panel);color:var(--ink);border:1px solid var(--grid);border-radius:6px;padding:4px 6px;font-size:12px;max-width:170px}
button{background:var(--panel);color:var(--ink);border:1px solid var(--grid);border-radius:6px;padding:6px 10px;cursor:pointer;align-self:flex-end}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;max-width:1300px;margin:12px auto;padding:0 16px}
.tile{background:var(--panel);border:1px solid var(--grid);border-radius:10px;padding:10px 12px}.tile b{font-size:22px;display:block}.tile span{color:var(--ink2);font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:12px;max-width:1300px;margin:auto;padding:0 16px 16px}
.card{background:var(--panel);border:1px solid var(--grid);border-radius:10px;padding:10px;min-width:0}.card h3{margin:2px 4px 0;font-size:14px}.card .n{color:var(--muted);font-size:11px;margin:0 4px}
.chart{height:330px}table{width:100%;border-collapse:collapse;font-size:12px}td,th{border-bottom:1px solid var(--grid);padding:4px;text-align:left;vertical-align:top}
a{color:var(--s1)}.note{max-width:1300px;margin:0 auto 24px;padding:0 16px;color:var(--ink2);font-size:12px}
@media (max-width:520px){.grid{grid-template-columns:1fr}select{max-width:140px}}
</style></head><body>
<header><h1>HYCANE — Hydroponic Social Listening Dashboard</h1>
<div class="sub">Observed public digital discourse, not a population survey. Labels are model/rule-predicted unless stated. <span id="meta"></span></div></header>
<div class="filters" id="filters"></div>
<div class="tiles" id="tiles"></div>
<div class="grid">
 <div class="card"><h3>Sentiment</h3><div class="n" id="n_sent"></div><div class="chart" id="c_sent"></div></div>
 <div class="card"><h3>Platform</h3><div class="n" id="n_plat"></div><div class="chart" id="c_plat"></div></div>
 <div class="card"><h3>Pain points (multi-label)</h3><div class="n" id="n_pain"></div><div class="chart" id="c_pain"></div></div>
 <div class="card"><h3>Primary intent</h3><div class="n" id="n_int"></div><div class="chart" id="c_int"></div></div>
 <div class="card"><h3>Feature mentions</h3><div class="n" id="n_feat"></div><div class="chart" id="c_feat"></div></div>
 <div class="card"><h3>Timeline (by year)</h3><div class="n" id="n_time"></div><div class="chart" id="c_time"></div></div>
 <div class="card"><h3>Topics (top 15)</h3><div class="n" id="n_top"></div><div class="chart" id="c_top"></div></div>
 <div class="card"><h3>Personas</h3><div class="n" id="n_per"></div><div class="chart" id="c_per"></div></div>
</div>
<div class="grid"><div class="card" style="grid-column:1/-1"><h3>Matching records (first 60 with snippets)</h3><div class="n">Snippets (≤220 characters) are embedded for a seeded random sample of 6,000 records to keep the page small; open the source for context.</div><div id="tbl"></div></div></div>
<div class="note">Exclusions applied before this dashboard: irrelevant, unrelated meanings, spam, duplicates. Use the Scope filter to include cannabis-context and news/promotional records. Sources: data/gold/hycane_social_listening_gold.parquet.</div>
<script>
const RAW=__DATA__, M=__META__; const D={}; for(const c in RAW.cols){const dc=RAW.dicts[c]; D[c]=dc?RAW.cols[c].map(i=>dc[i]):RAW.cols[c]} const N=D.p.length;
document.getElementById('meta').textContent=`Gold n=${M.counts.gold.toLocaleString()}; customer-voice core n=${M.counts.customer_voice.toLocaleString()}; timeframe ${M.tf}.`;
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const F=[["scope","Scope",null],["p","Platform"],["f","Source family"],["l","Language"],["c","Country (explicit)"],["x","Experience"],["i","Intent"],["s","Sentiment"],["t","Topic"],["r","Persona"]];
const fe=document.getElementById('filters'); const state={};
function uniq(k){return [...new Set(D[k])].sort()}
F.forEach(([k,lab])=>{const L=document.createElement('label');L.textContent=lab;const s=document.createElement('select');s.id='f_'+k;
 if(k==='scope'){[['voice','Customer voice (core)'],['core','Core scope (incl. news/promo)'],['all','All gold (incl. cannabis-context)']].forEach(([v,t])=>s.add(new Option(t,v)))}
 else{s.add(new Option('All','')); uniq(k).forEach(v=>s.add(new Option(v.length>40?v.slice(0,40)+'…':v,v)))}
 s.onchange=render;L.appendChild(s);fe.appendChild(L)});
[['from','From (YYYY-MM)'],['to','To (YYYY-MM)']].forEach(([k,t])=>{const L=document.createElement('label');L.textContent=t;const i=document.createElement('input');i.id='f_'+k;i.placeholder=k==='from'?'2008-01':'2026-12';i.size=8;i.onchange=render;L.appendChild(i);fe.appendChild(L)});
const b=document.createElement('button');b.textContent='Reset';b.onclick=()=>{fe.querySelectorAll('select,input').forEach(e=>{e.value=e.tagName==='SELECT'&&e.id==='f_scope'?'voice':''});render()};fe.appendChild(b);
function idx(){const sc=document.getElementById('f_scope').value,fr=document.getElementById('f_from').value,to=document.getElementById('f_to').value;
 const sel={};F.slice(1).forEach(([k])=>{const v=document.getElementById('f_'+k).value;if(v)sel[k]=v});const out=[];
 for(let j=0;j<N;j++){if(sc==='voice'&&!D.v[j])continue;if(sc==='core'&&!D.sc[j])continue;let ok=true;for(const k in sel){if(D[k][j]!==sel[k]){ok=false;break}}
  if(!ok)continue;if(fr&&D.m[j]<fr)continue;if(to&&D.m[j]>to)continue;out.push(j)}return out}
function count(I,k,multi){const c={};I.forEach(j=>{const v=D[k][j];if(multi){if(!v)return;v.split('|').forEach(x=>{if(x)c[x]=(c[x]||0)+1})}else c[v]=(c[v]||0)+1});return Object.entries(c).sort((a,b)=>b[1]-a[1])}
const layout=(h)=>({margin:{l:150,r:20,t:6,b:30},paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:css('--ink2'),size:11},xaxis:{gridcolor:css('--grid'),zeroline:false},yaxis:{automargin:true},height:h||330,showlegend:false});
function hbar(id,pairs,n,denomLabel,color){pairs=pairs.slice(0,15).reverse();Plotly.react(id,[{type:'bar',orientation:'h',x:pairs.map(p=>p[1]),y:pairs.map(p=>p[0].length>34?p[0].slice(0,34)+'…':p[0]),marker:{color:color||css('--s1')},
 hovertemplate:'%{y}: %{x:,} ('+'%{customdata:.1f}% of '+n.toLocaleString()+')<extra></extra>',customdata:pairs.map(p=>100*p[1]/Math.max(1,n))}],layout(),{displayModeBar:false,responsive:true})}
function render(){const I=idx(),n=I.length;const yrs={};I.forEach(j=>{const y=D.m[j].slice(0,4);yrs[y]=(yrs[y]||0)+1});
 const sent=count(I,'s'),order=['POSITIVE','NEUTRAL','MIXED','AMBIGUOUS','NEGATIVE'],sc={POSITIVE:css('--pos'),NEUTRAL:css('--neu'),MIXED:css('--mix'),AMBIGUOUS:css('--amb'),NEGATIVE:css('--neg')};
 const sm=Object.fromEntries(sent);
 Plotly.react('c_sent',[{type:'bar',x:order,y:order.map(o=>sm[o]||0),marker:{color:order.map(o=>sc[o])},hovertemplate:'%{x}: %{y:,} (%{customdata:.1f}%)<extra></extra>',customdata:order.map(o=>100*(sm[o]||0)/Math.max(1,n))}],{...layout(),margin:{l:40,r:10,t:6,b:30}},{displayModeBar:false,responsive:true});
 hbar('c_plat',count(I,'p'),n);hbar('c_pain',count(I,'pp',true),n);hbar('c_int',count(I,'i'),n);hbar('c_feat',count(I,'ft',true),n);hbar('c_top',count(I,'t'),n);hbar('c_per',count(I,'r'),n);
 const ys=Object.keys(yrs).filter(y=>y!=='unkn').sort();Plotly.react('c_time',[{type:'bar',x:ys,y:ys.map(y=>yrs[y]),marker:{color:css('--s1')},hovertemplate:'%{x}: %{y:,}<extra></extra>'}],{...layout(),margin:{l:40,r:10,t:6,b:30}},{displayModeBar:false,responsive:true});
 ['n_sent','n_plat','n_pain','n_int','n_feat','n_time','n_top','n_per'].forEach(id=>document.getElementById(id).textContent=`n = ${n.toLocaleString()} filtered records (denominator for %)`);
 const neg=(sm.NEGATIVE||0)/Math.max(1,n),pains=count(I,'pp',true);
 document.getElementById('tiles').innerHTML=[[n.toLocaleString(),'records in filter'],[new Set(I.map(j=>D.p[j])).size,'platforms'],[(100*neg).toFixed(1)+'%','negative (model)'],[pains.length?pains[0][0]:'—','most frequent pain'],[I.filter(j=>D.l[j]==='id').length.toLocaleString(),'Indonesian-language']].map(([b,s])=>`<div class="tile"><b>${b}</b><span>${s}</span></div>`).join('');
 const rows=I.filter(j=>D.tx[j]).slice(0,60).map(j=>`<tr><td>${D.p[j]}</td><td>${D.m[j]}</td><td>${D.s[j]}</td><td>${D.i[j]}</td><td>${D.pp[j]}</td><td>${D.tx[j].replace(/</g,'&lt;')}</td><td>${D.u[j]?`<a href="${D.u[j]}" target="_blank" rel="noopener">source</a>`:''}</td></tr>`).join('');
 document.getElementById('tbl').innerHTML=`<div style="overflow-x:auto"><table><tr><th>Platform</th><th>Month</th><th>Sentiment</th><th>Intent</th><th>Pains</th><th>Snippet</th><th></th></tr>${rows}</table></div>`}
render();
</script></body></html>
"""

if __name__ == "__main__":
    main()
