# book-bot

An upgraded `book-bot`: a Telegram webhook-based book recommendation bot.

## Features

- Random book recommendations (`book`, `recommend`, `/book`, plus legacy Chinese commands).
- Command help (`/start`, `/help`).
- Health check endpoint (`GET /health`).
- Webhook receiver (`POST /webhook`).

## Quick Start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` file (or set variables directly on your deployment platform):

```bash
BOT_TOKEN=your_telegram_bot_token
PORT=5000
```

> ⚠️ `BOT_TOKEN` is required. The app will fail fast at startup if missing.

### 3) Start the service

```bash
python telegram_webhook.py
```

## API Routes

- `POST /webhook`: Telegram webhook entry point.
- `GET /health`: Service health check.

## Suggested Next Upgrades

Recommended priority:

1. **Production-ready Telegram experience (highest priority)**
   - Add book search (Open Library) and user history.
   - Move the static list to a database (SQLite/Postgres).
2. **Smarter recommendation system**
   - Upgrade from random recommendations to preference + history based recommendations.
3. **Deployment and observability**
   - Deploy to Render or Railway.
   - Add structured logging and alerting.
4. **Web admin panel (optional)**
   - Add a Flask/FastAPI admin UI for books, categories, and statistics.

## Security Note

Never hardcode your bot token in source code. Always use environment variables.
