#!/usr/bin/env python3
"""
Telegram Bot Webhook 服務
接收並處理群組訊息，自動回覆「發書」指令
"""

from flask import Flask, request, jsonify
import requests
import random
import os

app = Flask(__name__)

# 設定
BOT_TOKEN = "7674985836:AAEniE0_DBi-4nDH1u0kfYLocyicWSyI4X8"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 書籍資料庫
BOOKS = [
    {"title": "原子習慣", "author": "詹姆斯·克利爾", "category": "自我成長",
     "description": "微小改變如何產生巨大成效",
     "quote": "習慣是自我改進的複利。",
     "link": "https://www.goodreads.com/book/show/40121378-atomic-habits"},
    {"title": "深度工作", "author": "卡爾·紐波特", "category": "效率提升",
     "description": "如何在分心的世界保持專注",
     "quote": "專注於少數重要的事情，拒絕無價值的忙碌。",
     "link": "https://www.calnewport.com/books/deep-work/"},
    {"title": "窮爸爸富爸爸", "author": "羅伯特·清崎", "category": "理財",
     "description": "財務智商的九堂課",
     "quote": "窮人為錢工作，富人讓錢為他們工作。",
     "link": "https://www.richdad.com/"},
    {"title": "人類大歷史", "author": "哈拉瑞", "category": "歷史",
     "description": "從動物到上帝的旅程",
     "quote": "智人之所以能征服世界，是因為獨特語言讓我們能談論虛構的事物。",
     "link": "https://www.ynharari.com/book/sapiens/"},
    {"title": "心流", "author": "米哈里·契克森米哈伊", "category": "心理學",
     "description": "最優體驗的心理學",
     "quote": "當挑戰與技能完美匹配時，就會進入心流狀態。",
     "link": "https://www.amazon.com/Flow-Psychology-Experience-Mihaly-Csikszentmihalyi/dp/0061339202"},
    {"title": "黑天鵝效應", "author": "納西姆·塔勒布", "category": "思考方式",
     "description": "如何面對不可預測的未來",
     "quote": "我們熱衷於統計和預測，卻忽略了罕見事件的力量。",
     "link": "https://www.nassimnicholas.com/books/the-black-swans"},
    {"title": "原則", "author": "瑞·達利歐", "category": "商業",
     "description": "生活和工作的一般原則",
     "quote": "理解現實如何運作，是做出良好決策的基礎。",
     "link": "https://www.principles.com/"},
    {"title": "快思慢想", "author": "丹尼爾·卡尼曼", "category": "心理學",
     "description": "思考，快與慢",
     "quote": "系統一快速、本能；系統二緩慢、理性。",
     "link": "https://books.wwnorton.com/books/9780374533557/"},
    {"title": "刻意練習", "author": "安德斯·艾瑞克森", "category": "自我成長",
     "description": "如何從新手到大師",
     "quote": "天才不是天生，而是刻意練習的結果。",
     "link": "https://peaks卓越圖書.com/book/peak/"},
    {"title": "華頓商學院最受歡迎的談判課", "author": "史都華·戴蒙", "category": "溝通",
     "description": "如何在任何談判中獲得更好的結果",
     "quote": "談判的目標不是戰勝對方，而是滿足雙方的需求。",
     "link": "https://www.whartonhamburg.com/the-wharton-executive-negotiation-workshop/"},
    {"title": "被討厭的勇氣", "author": "岸見一郎 & 古賀史健", "category": "心理學",
     "description": "阿德勒心理學的勇氣之書",
     "quote": "你的不幸，是自己選擇的。",
     "link": "https://www.bookmall.com.tw/9789861371858"},
    {"title": "牧羊少年奇幻之旅", "author": "保羅·科爾賀", "category": "文學",
     "description": "追尋你的個人傳奇",
     "quote": "當你真心渴望某樣東西時，整個宇宙都會聯合起來幫助你。",
     "link": "https://www.paulocoelhoblog.com/the-alchemist/"}
]

def get_random_book():
    return random.choice(BOOKS)

def format_book_message(book):
    message = f"""
📚 *每日書籍推薦*
━━━━━━━━━━━━━━━
📖 *{book['title']}*
✍️ {book['author']}
📁 {book['category']}
━━━━━━━━━━━━━━━
💡 {book['description']}
━━━━━━━━━━━━━━━
📜 *金句*
「{book['quote']}」
━━━━━━━━━━━━━━━
🔗 了解更多
{book['link']}
━━━━━━━━━━━━━━━
🌟 每天進步一點點！"""
    return message.strip()

def send_message(chat_id, text, reply_to_message_id=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    return requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # 檢查是否有訊息
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        message_id = message.get('message_id')

        # 檢查是否為「發書」指令
        if text in ['發書', '書', '推薦', '/start', '/book']:
            book = get_random_book()
            reply = format_book_message(book)
            send_message(chat_id, reply, message_id)
            return jsonify({"ok": True, "sent": True})

        # 自動回覆其他訊息
        elif text and not text.startswith('/'):
            reply = "👋 嗨！輸入「發書」或「書」獲得書籍推薦！"
            send_message(chat_id, reply, message_id)
            return jsonify({"ok": True, "replied": True})

    return jsonify({"ok": True})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "bot": "checkin_jiji_bot"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
