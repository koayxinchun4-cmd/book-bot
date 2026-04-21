#!/usr/bin/env python3
"""
Telegram bot webhook service.
Receives and processes Telegram messages, then replies with book recommendations.
"""

from flask import Flask, request, jsonify
import requests
import random
import os

app = Flask(__name__)


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Book catalog
BOOKS = [
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self-Improvement",
        "description": "How tiny changes produce remarkable results",
        "quote": "Habits are the compound interest of self-improvement.",
        "link": "https://www.goodreads.com/book/show/40121378-atomic-habits",
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "category": "Productivity",
        "description": "How to stay focused in a distracted world",
        "quote": "Focus on what matters and reject low-value busyness.",
        "link": "https://www.calnewport.com/books/deep-work/",
    },
    {
        "title": "Rich Dad Poor Dad",
        "author": "Robert Kiyosaki",
        "category": "Personal Finance",
        "description": "Lessons on building financial intelligence",
        "quote": "The poor work for money; the rich make money work for them.",
        "link": "https://www.richdad.com/",
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "category": "History",
        "description": "A brief history of humankind",
        "quote": "Shared stories let humans cooperate at massive scale.",
        "link": "https://www.ynharari.com/book/sapiens/",
    },
    {
        "title": "Flow",
        "author": "Mihaly Csikszentmihalyi",
        "category": "Psychology",
        "description": "The psychology of optimal experience",
        "quote": "Flow appears when challenge and skill are in balance.",
        "link": "https://www.amazon.com/Flow-Psychology-Experience-Mihaly-Csikszentmihalyi/dp/0061339202",
    },
    {
        "title": "The Black Swan",
        "author": "Nassim Nicholas Taleb",
        "category": "Decision-Making",
        "description": "How to think about rare and unpredictable events",
        "quote": "Rare events can dominate history more than we expect.",
        "link": "https://www.nassimnicholas.com/books/the-black-swan/",
    },
    {
        "title": "Principles",
        "author": "Ray Dalio",
        "category": "Business",
        "description": "Core principles for life and work",
        "quote": "Understanding reality is the foundation of good decisions.",
        "link": "https://www.principles.com/",
    },
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "category": "Psychology",
        "description": "An exploration of two systems of thinking",
        "quote": "System 1 is fast and intuitive; System 2 is slow and analytical.",
        "link": "https://books.wwnorton.com/books/9780374533557/",
    },
    {
        "title": "Peak",
        "author": "Anders Ericsson",
        "category": "Self-Improvement",
        "description": "How deliberate practice builds expertise",
        "quote": "Great performance is built, not born.",
        "link": "https://www.hmhbooks.com/shop/books/peak/9780544947221",
    },
    {
        "title": "Getting More",
        "author": "Stuart Diamond",
        "category": "Communication",
        "description": "Practical methods for better negotiation outcomes",
        "quote": "Negotiation should solve needs, not defeat people.",
        "link": "https://www.whartonhamburg.com/the-wharton-executive-negotiation-workshop/",
    },
    {
        "title": "The Courage to Be Disliked",
        "author": "Ichiro Kishimi & Fumitake Koga",
        "category": "Psychology",
        "description": "An Adlerian perspective on freedom and growth",
        "quote": "You can choose your present and your direction forward.",
        "link": "https://www.bookmall.com.tw/9789861371858",
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Literature",
        "description": "A fable about pursuing your personal legend",
        "quote": "When you truly want something, the world helps you pursue it.",
        "link": "https://www.paulocoelhoblog.com/the-alchemist/",
    },
]


def get_random_book():
    return random.choice(BOOKS)


def format_book_message(book):
    message = f"""
📚 *Daily Book Recommendation*
━━━━━━━━━━━━━━━
📖 *{book['title']}*
✍️ {book['author']}
📁 {book['category']}
━━━━━━━━━━━━━━━
💡 {book['description']}
━━━━━━━━━━━━━━━
📜 *Quote*
「{book['quote']}」
━━━━━━━━━━━━━━━
🔗 Learn more
{book['link']}
━━━━━━━━━━━━━━━
🌟 Progress a little every day!"""
    return message.strip()


def send_message(chat_id, text, reply_to_message_id=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    return requests.post(url, json=payload, timeout=10)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True) or {}

    # Check whether the update contains a message
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        message_id = message.get('message_id')

        # Recommendation triggers (English + legacy Chinese aliases)
        if text.lower() in ['book', 'recommend', '/book', '發書', '書', '推薦']:
            book = get_random_book()
            reply = format_book_message(book)
            send_message(chat_id, reply, message_id)
            return jsonify({"ok": True, "sent": True})

        if text in ['/start', '/help']:
            help_text = (
                "👋 Welcome to Book Bot!\n"
                "Available commands:\n"
                "- book / recommend /book: get a random book recommendation\n"
                "- /help: show this help message"
            )
            send_message(chat_id, help_text, message_id)
            return jsonify({"ok": True, "help": True})

        # Auto-reply to other non-command messages
        if text and not text.startswith('/'):
            reply = "👋 Hi! Type `book` or `recommend` to get a recommendation."
            send_message(chat_id, reply, message_id)
            return jsonify({"ok": True, "replied": True})

    return jsonify({"ok": True})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "bot": "book-bot"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
