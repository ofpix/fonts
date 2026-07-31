#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build index.html + style.css for the font palette site."""
import os, json, html
from gen_shots import FONTS, TEXTS

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "site")
os.makedirs(SITE, exist_ok=True)

LANGS = [
    ("zh-TW", "繁體中文", "Traditional Chinese"),
    ("ja", "日本語", "Japanese"),
    ("en", "English", "English"),
]

def card(f, i):
    kinds = [("display", "Display 標題"), ("body", "Body 正文"), ("weights", "Weights 字重")]
    slides = "".join(
        f'<img class="slide" src="screenshots/{f["id"]}-{k}.png" alt="{f["name"]} {label}" loading="lazy">'
        for k, label in kinds
    )
    weights = " / ".join(l for l, _ in f["weights"])
    return f"""
<article class="card" id="card-{f['id']}">
  <header class="card-head">
    <div>
      <h3 class="fname">{html.escape(f['name'])}</h3>
      <p class="fsub">{html.escape(f['sub'])}</p>
    </div>
    <span class="fmeta">{weights}</span>
  </header>
  <p class="fdesc">{html.escape(f.get('desc', ''))}</p>
  <div class="swiper" tabindex="0" aria-label="{html.escape(f['name'])} 樣張，左右滑動">
    {slides}
  </div>
  <footer class="card-foot">← 左右滑動查看更多樣張 →</footer>
</article>"""

def build():
    cards = {lang: [] for lang, _, _ in LANGS}
    for i, f in enumerate(FONTS):
        cards[f["lang"]].append(card(f, i))

    tabs = ""
    panels = ""
    for idx, (lang, label, en) in enumerate(LANGS):
        active = " active" if idx == 0 else ""
        tabs += f'<button class="tab{active}" data-lang="{lang}">{label}<small>{en}</small></button>'
        panels += f'<section class="panel{active}" data-panel="{lang}"><div class="grid">{"".join(cards[lang])}</div></section>'

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Font Palette — 字體選擇庫</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-head">
  <h1>Font Palette <span>字體選擇庫</span></h1>
  <p>設計時快速翻閱的常用字體樣張 · 每個字體包含 標題 / 正文 / 字重 三張樣張，左右滑動查看</p>
</header>

<nav class="tabs" role="tablist">
  {tabs}
</nav>

<main>
  {panels}
</main>

<footer class="site-foot">Font Palette · 樣張由本地字體渲染生成 · 2026</footer>

<script>
(function(){{
  var tabs = document.querySelectorAll('.tab');
  var panels = document.querySelectorAll('.panel');
  tabs.forEach(function(t){{
    t.addEventListener('click', function(){{
      tabs.forEach(function(x){{ x.classList.remove('active'); }});
      panels.forEach(function(p){{ p.classList.remove('active'); }});
      t.classList.add('active');
      document.querySelector('[data-panel="' + t.dataset.lang + '"]').classList.add('active');
    }});
  }});
}})();
</script>
</body>
</html>"""
    with open(os.path.join(SITE, "index.html"), "w") as fh:
        fh.write(html_doc)

    css = """
*{margin:0;padding:0;box-sizing:border-box;}
:root{--bg:#faf9f7;--ink:#1a1a1a;--mut:#888;--line:#e8e6e2;--accent:#b4532a;}
body{background:var(--bg);color:var(--ink);font-family:'Noto Sans CJK TC','Noto Sans',system-ui,sans-serif;line-height:1.6;}
.site-head{padding:48px 24px 24px;max-width:1440px;margin:0 auto;text-align:center;}
.site-head h1{font-size:32px;letter-spacing:.04em;}
.site-head h1 span{color:var(--accent);font-weight:400;font-size:22px;margin-left:8px;}
.site-head p{color:var(--mut);font-size:13px;margin-top:8px;}
.tabs{display:flex;justify-content:center;gap:8px;padding:16px 12px;position:sticky;top:0;background:rgba(250,249,247,.92);backdrop-filter:blur(6px);z-index:10;}
.tab{border:1px solid var(--line);background:#fff;color:var(--ink);padding:10px 22px;border-radius:999px;cursor:pointer;font-size:15px;display:flex;align-items:baseline;gap:8px;transition:all .15s;}
.tab small{color:var(--mut);font-size:11px;letter-spacing:.05em;}
.tab:hover{border-color:#ccc;}
.tab.active{background:var(--ink);color:#fff;border-color:var(--ink);}
.tab.active small{color:#bbb;}
main{max-width:1440px;margin:0 auto;padding:8px 24px 64px;}
.panel{display:none;}
.panel.active{display:block;}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;padding:16px 18px 12px;gap:12px;}
.fname{font-size:17px;letter-spacing:.02em;}
.fsub{font-size:12px;color:var(--mut);margin-top:2px;}
.fdesc{font-size:13px;color:#555;line-height:1.7;padding:0 18px 14px;}
.fmeta{font-size:11px;color:#bbb;white-space:nowrap;padding-top:4px;}
.swiper{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:thin;background:#f4f2ef;}
.swiper::-webkit-scrollbar{height:6px;}
.swiper::-webkit-scrollbar-thumb{background:#d8d4ce;border-radius:3px;}
.slide{flex:0 0 100%;width:100%;height:auto;scroll-snap-align:start;display:block;}
.card-foot{font-size:11px;color:#ccc;text-align:center;padding:8px;letter-spacing:.08em;}
.site-foot{text-align:center;color:#bbb;font-size:12px;padding:32px 0 48px;}

@media (max-width:1024px){.grid{grid-template-columns:1fr;}}
@media (max-width:480px){.site-head h1{font-size:24px;}main{padding:8px 12px 48px;}}
"""
    with open(os.path.join(SITE, "style.css"), "w") as fh:
        fh.write(css)
    print("site built")

if __name__ == "__main__":
    build()
