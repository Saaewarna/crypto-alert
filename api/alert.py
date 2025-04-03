# api/alert.py
import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

ALERTS = {
    'ADAUSDT': {'above': 1.30, 'below': 0.50},
    'SEIUSDT': {'above': 2.00, 'below': 0.50}
}

def get_price(symbol):
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
        res = requests.get(url).json()
        return float(res['price'])
    except:
        return None

def send_alert(symbol, price, direction):
    message = f"⚠️ {symbol} {direction} batas: ${price:.4f}"
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(telegram_url, data={'chat_id': CHAT_ID, 'text': message})

@app.route('/api/alert', methods=['GET'])
def alert_handler():
    result = []
    for symbol, levels in ALERTS.items():
        price = get_price(symbol)
        if price:
            if price >= levels['above']:
                send_alert(symbol, price, "naik di atas")
                result.append(f"{symbol} naik: ${price}")
            elif price <= levels['below']:
                send_alert(symbol, price, "turun di bawah")
                result.append(f"{symbol} turun: ${price}")
    return jsonify({"result": result or "Tidak ada alert dikirim."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
