#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate font specimen screenshots via chrome headless."""
import os, subprocess, sys, json, html

BASE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE, "shots")
OUT = os.path.join(BASE, "site", "screenshots")
os.makedirs(SHOTS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# ---------------- copy ----------------
# Sample texts per language
TEXTS = {
    "zh-TW": {
        "h1": "每個人都閃耀獨特光芒",
        "h2": "在 AI 時代守住人文主義立場",
        "body": "在這樣一個「控制」的時代，外部化力量遠大於個體。人生變成了這樣的模式：我們以各種方式成長到某一時間點，開始問自己，我是誰？我為什麼變成現在的我？於是，接下來的人生就是對抗外部壓力，不斷動態地主動重塑自我的過程。",
        "short": "天地玄黃 宇宙洪荒 世事如棋 人海浮沉",
        "meta": "繁中 · 標題/正文/字重",
    },
    "ja": {
        "h1": "一人ひとりが独自の光を放つ",
        "h2": "AI時代に人文主義の立場を守る",
        "body": "「管理」の時代にあって、外部の力は個人をはるかに上回っている。人生はこんなパターンになる。私たちはさまざまな形で成長し、ある時点で自問し始める——私は誰なのか？ なぜ私は今の私になったのか？ そして、それからの人生は、外部の圧力に抗いながら、能動的に自己を組み直し続けるプロセスとなる。",
        "short": "いろはにほへと ちりぬるを わかよたれそ",
        "meta": "日本語 · タイトル/本文/ウェイト",
    },
    "en": {
        "h1": "Everyone Shines with a Unique Light",
        "h2": "Holding the Humanist Line in the Age of AI",
        "body": "In an age of \u201ccontrol,\u201d external forces far outweigh the individual. Life turns into this pattern: we grow in various ways until a certain point, when we begin to ask ourselves \u2014 who am I? Why have I become what I am? And so, the rest of life becomes a process of actively reshaping ourselves against external pressure, again and again.",
        "short": "The quick brown fox jumps over the lazy dog 0123456789",
        "meta": "English · Display / Body / Weights",
    },
}

# Font definitions.
# src: None -> system font (just use family name). Else list of (weight, ttf path)
FONTS = [
    # --- Traditional Chinese ---
    {"id": "noto-sans-tc", "name": "Noto Sans TC", "sub": "思源黑體 · 現代黑體", "lang": "zh-TW",
     "desc": "現代黑體的標竿，中性清晰、筆畫均勻，螢幕閱讀表現佳。UI、正文、通用場景萬用首選。",
     "family": "'Noto Sans CJK TC'", "system": True, "weights": [("Light", 300), ("Regular", 400), ("Medium", 500), ("Bold", 700), ("Black", 900)]},
    {"id": "noto-serif-tc", "name": "Noto Serif TC", "sub": "思源宋體 · 現代宋體", "lang": "zh-TW",
     "desc": "現代宋體，橫細直粗的結構勻稱而不匠氣。文章、書籍、正式場合的氣質首選。",
     "family": "'Noto Serif CJK TC'", "system": True, "weights": [("Light", 300), ("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("Black", 900)]},
    {"id": "ukai-tw", "name": "AR PL UKai TW", "sub": "楷體 · 手寫楷書", "lang": "zh-TW",
     "desc": "傳統楷書，帶手寫溫度與文人氣。詩詞、文化類內容、溫潤質感的標題很對味。",
     "family": "'AR PL UKai TW'", "system": True, "weights": [("Book", 400)]},
    {"id": "uming-tw", "name": "AR PL UMing TW", "sub": "明體 · 傳統明體", "lang": "zh-TW",
     "desc": "經典明體，筆畫對比強烈、骨架硬朗，古籍、報刊、復古氛圍的傳統選擇。",
     "family": "'AR PL UMing TW'", "system": True, "weights": [("Light", 400)]},
    # --- Japanese ---
    {"id": "noto-sans-jp", "name": "Noto Sans JP", "sub": "ゴシック体 · 現代ゴシック", "lang": "ja",
     "desc": "日文黑體標準，清晰中性。UI、正文、任何通用場景都安全。",
     "family": "'Noto Sans CJK JP'", "system": True, "weights": [("Light", 300), ("Regular", 400), ("Medium", 500), ("Bold", 700), ("Black", 900)]},
    {"id": "noto-serif-jp", "name": "Noto Serif JP", "sub": "明朝体 · トラディショナル", "lang": "ja",
     "desc": "日文明朝體，端莊優雅、閱讀感佳。書籍、報導、正式編輯設計。",
     "family": "'Noto Serif CJK JP'", "system": True, "weights": [("Light", 300), ("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("Black", 900)]},
    {"id": "zen-maru-gothic", "name": "Zen Maru Gothic", "sub": "丸ゴシック · やわらかい印象", "lang": "ja",
     "desc": "日文圓體，轉角圓潤、氛圍柔和親切。兒童、生活感、可愛風格的標題很適合。",
     "family": "'Zen Maru Gothic'", "system": False,
     "src": [("400", os.path.join(BASE, "fonts/zen-maru-gothic/zen-maru-gothic-v19-japanese-regular.ttf")),
             ("700", os.path.join(BASE, "fonts/zen-maru-gothic/zen-maru-gothic-v19-japanese-700.ttf"))],
     "weights": [("Regular", 400), ("Bold", 700)]},
    # --- English ---
    {"id": "inter", "name": "Inter", "sub": "Grotesk · UI / 正文首選", "lang": "en",
     "desc": "瑞士風格怪誕體，為螢幕設計。小尺寸與數字的可讀性極佳，UI 介面首選。",
     "family": "'Inter'", "system": False,
     "src": [("400", os.path.join(BASE, "fonts/inter/inter-v20-latin-regular.ttf")),
             ("500", os.path.join(BASE, "fonts/inter/inter-v20-latin-500.ttf")),
             ("700", os.path.join(BASE, "fonts/inter/inter-v20-latin-700.ttf"))],
     "weights": [("Regular", 400), ("Medium", 500), ("Bold", 700)]},
    {"id": "playfair-display", "name": "Playfair Display", "sub": "高対比セリフ · エレガント", "lang": "en",
     "desc": "高對比 Didone 襯線，筆畫極具裝飾性。雜誌、時尚、優雅大標題的首選。",
     "family": "'Playfair Display'", "system": False,
     "src": [("400", os.path.join(BASE, "fonts/playfair-display/playfair-display-v40-latin-regular.ttf")),
             ("500", os.path.join(BASE, "fonts/playfair-display/playfair-display-v40-latin-500.ttf")),
             ("700", os.path.join(BASE, "fonts/playfair-display/playfair-display-v40-latin-700.ttf"))],
     "weights": [("Regular", 400), ("Medium", 500), ("Bold", 700)]},
    {"id": "montserrat", "name": "Montserrat", "sub": "幾何学サンセリフ · タイトル向き", "lang": "en",
     "desc": "幾何無襯線，源自蒙特婁街頭招牌。現代、強烈、有辨識度，品牌與海報標題。",
     "family": "'Montserrat'", "system": False,
     "src": [("400", os.path.join(BASE, "fonts/montserrat/montserrat-v31-latin-regular.ttf")),
             ("500", os.path.join(BASE, "fonts/montserrat/montserrat-v31-latin-500.ttf")),
             ("700", os.path.join(BASE, "fonts/montserrat/montserrat-v31-latin-700.ttf"))],
     "weights": [("Regular", 400), ("Medium", 500), ("Bold", 700)]},
    {"id": "jetbrains-mono", "name": "JetBrains Mono", "sub": "等幅 · コード／データ向き", "lang": "en",
     "desc": "工程師設計的等寬字體，細節講究（斜體、連字、可讀性）。程式碼、數據、技術內容。",
     "family": "'JetBrains Mono'", "system": False,
     "src": [("400", os.path.join(BASE, "fonts/jetbrains-mono/jetbrains-mono-v24-latin-regular.ttf")),
             ("500", os.path.join(BASE, "fonts/jetbrains-mono/jetbrains-mono-v24-latin-500.ttf")),
             ("700", os.path.join(BASE, "fonts/jetbrains-mono/jetbrains-mono-v24-latin-700.ttf"))],
     "weights": [("Regular", 400), ("Medium", 500), ("Bold", 700)]},
]

def face_block(f):
    if f.get("system"):
        return ""
    faces = []
    for weight, path in f["src"]:
        faces.append(
            "@font-face{font-family:%s;font-weight:%s;src:url('file://%s') format('truetype');}"
            % (f["family"], weight, path)
        )
    return "\n".join(faces)

def render(f, kind, t):
    fam = f["family"]
    faces = face_block(f)
    name = f["name"]
    sub = f["sub"]
    if kind == "display":
        body = f"""
<div class="frame">
  <div class="tag">{name} <span>· {sub}</span></div>
  <div class="disp">
    <h1 style="font-family:{fam};font-weight:700;">{html.escape(t['h1'])}</h1>
    <h2 style="font-family:{fam};font-weight:500;">{html.escape(t['h2'])}</h2>
  </div>
  <div class="foot">Display 樣張 · タイトル見本 · Heading specimen — H1 700 / H2 500</div>
</div>"""
    elif kind == "body":
        body = f"""
<div class="frame">
  <div class="tag">{name} <span>· {sub}</span></div>
  <div class="bd">
    <h2 style="font-family:{fam};font-weight:600;">{html.escape(t['h2'])}</h2>
    <p style="font-family:{fam};font-weight:400;">{html.escape(t['body'])}</p>
  </div>
  <div class="foot">Body 正文 · 本文 16px / 行高 1.8</div>
</div>"""
    else:  # weights
        rows = []
        for label, w in f["weights"]:
            rows.append(f'<div class="wrow"><span class="wlabel">{label} {w}</span><span class="wtext" style="font-family:{fam};font-weight:{w};">{html.escape(t["short"])}</span></div>')
        body = f"""
<div class="frame">
  <div class="tag">{name} <span>· {sub}</span></div>
  <div class="ws">{''.join(rows)}</div>
  <div class="foot">Weights 字重 · ウェイト比較</div>
</div>"""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#faf9f7;color:#1a1a1a;font-family:'Noto Sans CJK TC',sans-serif;}}
.frame{{width:900px;height:640px;padding:40px 48px;display:flex;flex-direction:column;background:#fff;border:1px solid #eee;}}
.tag{{font-size:13px;letter-spacing:.08em;color:#888;margin-bottom:8px;}}
.tag span{{color:#bbb;}}
.disp{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px;}}
.disp h1{{font-size:56px;line-height:1.25;letter-spacing:.02em;}}
.disp h2{{font-size:24px;line-height:1.6;color:#555;font-weight:500;}}
.bd{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:24px;}}
.bd h2{{font-size:26px;line-height:1.5;}}
.bd p{{font-size:16px;line-height:1.8;color:#444;max-width:780px;}}
.ws{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:14px;}}
.wrow{{display:flex;align-items:baseline;gap:24px;}}
.wlabel{{flex:0 0 120px;font-size:12px;color:#999;letter-spacing:.05em;}}
.wtext{{font-size:26px;line-height:1.4;}}
.foot{{font-size:11px;color:#ccc;letter-spacing:.12em;margin-top:16px;}}
</style></head><body>
{body}
</body></html>"""

def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    jobs = []
    for f in FONTS:
        if only and f["id"] not in only:
            continue
        for kind in ("display", "body", "weights"):
            html = render(f, kind, TEXTS[f["lang"]])
            p = os.path.join(SHOTS, f"{f['id']}-{kind}.html")
            with open(p, "w") as fh:
                fh.write(html)
            jobs.append((f["id"], kind, p))
    print(json.dumps(jobs))

if __name__ == "__main__":
    main()
