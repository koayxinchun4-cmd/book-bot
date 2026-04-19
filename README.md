# book-bot

進階版 `book-bot`：以 Telegram Webhook 為核心的書籍推薦機器人。

## 功能

- 隨機書籍推薦（輸入：`發書`、`書`、`推薦`、`/book`）
- 指令說明（`/start`、`/help`）
- 健康檢查端點（`GET /health`）
- Webhook 訊息接收（`POST /webhook`）

## 快速開始

### 1) 安裝套件

```bash
pip install -r requirements.txt
```

### 2) 設定環境變數

請先建立 `.env`（或直接在部署平台設定環境變數）：

```bash
BOT_TOKEN=你的_telegram_bot_token
PORT=5000
```

> ⚠️ `BOT_TOKEN` 必填，程式啟動時若未設定會直接報錯。

### 3) 啟動服務

```bash
python telegram_webhook.py
```

## API 路由

- `POST /webhook`：Telegram webhook 入口
- `GET /health`：服務健康檢查

## 下一步升級路線（建議）

建議優先順序：

1. **Telegram 實戰化（最高優先）**
   - 新增搜尋書籍（Open Library）與查詢歷史
   - 把書單改為資料庫（SQLite / Postgres）
2. **推薦系統智慧化**
   - 從「隨機推薦」升級為「偏好 + 歷史」推薦
3. **部署與可觀測性**
   - 部署到 Render / Railway
   - 加入結構化 logging 與錯誤告警
4. **Web 管理後台（可選）**
   - 使用 Flask/FastAPI 提供管理頁面（書單、分類、統計）

## 安全提醒

請勿把 bot token 寫死在程式碼中，務必透過環境變數管理。
