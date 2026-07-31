# Font Palette 字體選擇庫

個人字體選擇庫：一個頁面，三種語言（繁體中文 / 日本語 / English），每款字體以「標題 + 正文 + 字重」三張樣張呈現，設計時快速翻閱選擇。

🔗 線上頁面：https://ofpix.github.io/fonts/

## 收錄流程（新增字體）

1. **下載字體** → `fonts/<font-id>/`（Google Fonts 經 gwfh API，或廠商官網）
2. **編輯 `gen_shots.py`** 的 `FONTS` 清單，加入：
   - `id` / `name` / `sub`（副標題）/ `desc`（**風格與適用場景介紹**）
   - `family`（CSS family 名）與 `weights`（主要字重）
   - 下載的 ttf 需配置 `src`（@font-face 路徑）；系統字體 `system: True` 即可
3. **重新生成樣張 + 頁面**
   ```bash
   python3 gen_shots.py   # 生成 HTML 樣張模板
   python3 build_site.py  # 重建 index.html + style.css
   ```
   樣張截圖（chrome headless）：
   ```bash
   google-chrome --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
     --window-size=900,640 --screenshot=site/screenshots/<id>-<kind>.png \
     "file://$PWD/shots/<id>-<kind>.html"
   ```
   （`kind` = display / body / weights；weights 樣張即字重對比）
4. **commit + push** → GitHub Pages 自動部署

## 結構

```
├── gen_shots.py      # 字體清單 + 樣張模板生成
├── build_site.py     # 生成 index.html + style.css
├── fonts/            # 字體原始檔（本地，.gitignore 不入庫）
├── shots/            # 樣張 HTML 模板（不入庫）
└── site/             # 發佈內容（repo 根）
    ├── index.html
    ├── style.css
    └── screenshots/  # 樣張 PNG
```

## 樣張設計

- **Display**：H1 56px Bold + H2 24px Medium — 看標題氣勢
- **Body**：H2 26px + 正文 16px/1.8 — 看閱讀感
- **Weights**：同一句話 × 所有主要字重並排 — 看字重家族

樣張文案（三語對應）：「每個人都閃耀獨特光芒 / 在 AI 時代守住人文主義立場」
