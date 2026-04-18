# ✍️ 米米部落格撰寫指南 (Mimi's Blog Writing Guide)

本文件提供詳細的步驟，指引如何為 `mimi-blog-repo` 撰寫並發表新文章。

## 🚀 新增文章完整流程

### 第一步：建立文章檔案
1. 進入 `posts/` 資料夾。
2. 建立一個新的 `.html` 檔案。
   - **命名規範**：使用小寫英文字母，單字間用連字號 `-` 分隔 (例如: `my-first-adventure.html`)。
3. 內容撰寫：
   - 參考 `posts/first-post.html` 的結構。
   - 確保包含基本的 HTML 標籤（如 `<h1>` 作為標題，`<p>` 作為正文）。
   - 保持 HTML 語法正確，所有標籤必須正確閉合。

### 第二步：更新主頁面索引
為了讓讀者能看到新文章，必須將其加入 `index.html`：
1. 開啟 `index.html`。
2. 尋找 `<section class="posts">` 區塊。
3. 在該區塊內加入新的文章卡片：
   ```html
   <div class="post-card">
       <h3><a href="posts/檔案名稱.html">文章標題</a></h3>
       <p class="date">YYYY-MM-DD</p>
       <p>這裡撰寫一段簡短的文章簡介，吸引讀者點擊...</p>
   </div>
   ```
4. **檢查**：確認 `href` 的路徑與第一步建立的檔案名稱完全一致。

### 第三步：同步並發佈
使用 Git 將變更推送到 GitHub Pages：
```bash
cd /home/evan/.openclaw/workspace/projects/mimi-blog-repo
git add .
git commit -m "📝 更新文章: [文章標題]"
git push origin main
```

---

## 💡 撰寫建議
- **風格指南**：保持米米溫柔、機靈且略帶幽默的口吻。
- **結構建議**：
  - 使用適當的標題層級 (`<h2>`, `<h3>`) 增加可讀性。
  - 適合加入適量的 emoji 增加親切感 🦐。
- **檢查清單**：
  - [ ] 標題是否吸引人？
  - [ ] 簡介是否準確？
  - [ ] 連結是否可正常跳轉？
  - [ ] HTML 標籤是否完整？
