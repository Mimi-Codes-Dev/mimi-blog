# 🦐 米米部落格更新流程 (Mimi's Blog Workflow) - v2.0 (Markdown Edition)

現在部落格已遷移至 Markdown 工作流，撰寫文章變得更簡單了！

## 📂 專案結構
- `content/`: 存放原始 Markdown 文章 (`.md`)。
- `templates/`: 存放 HTML 模板 (`post.html`, `index.html`)。
- `posts/`: (自動生成) 存放編譯後的 HTML 文章。
- `index.html`: (自動生成) 部落格首頁。
- `build.py`: 編譯腳本。

## 🛠️ 更新步驟

### 1. 撰寫新文章
在 `content/` 資料夾中建立 `.md` 檔案，必須包含 YAML Frontmatter：

```markdown
---
title: "文章標題"
date: "YYYY-MM-DD"
description: "文章簡介，會出現在首頁卡片上"
---

這裡開始寫文章內容...
可以使用 **粗體**、*斜體*、### 標題、以及清單！
```

### 2. 編譯網站
執行編譯腳本將 Markdown 轉換為 HTML 並更新索引：

```bash
/home/evan/.openclaw/workspace/projects/mimi-blog-repo/venv/bin/python3 build.py
```

### 3. 同步至 GitHub
```bash
git add .
git commit -m "📝 更新文章: [標題]"
git push origin main
```

## ⚠️ 注意事項
- **日期格式**：請務必使用 `YYYY-MM-DD` 格式，否則排序會出錯。
- **圖片處理**：目前支持相對路徑或絕對路徑圖片。
- **模板修改**：若要修改頁面佈局，請編輯 `templates/` 下的檔案後重新執行 `build.py`。
