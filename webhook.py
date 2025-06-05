from dotenv import load_dotenv
import os

load_dotenv()  # .envを読み込む

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")


from flask import Flask, request, abort
import json
import hashlib
import hmac
import base64
import requests
import os

app = Flask(__name__)

# ↓ 環境変数か直接文字列で設定
CHANNEL_SECRET = '07a593b8271095f8473d6f9cd05983ce'  # Messaging API → Channel Secret
ACCESS_TOKEN = 'hxFx/HxdRpH6v5wfysUD8Vo2uO5JuarBvWH//RRT/e3oTpQG162AFz5mjLwJHxotFsU5twqB0lBwtHqpUKBbK25C8G9EvTi/iLqihe0RNntOZ9rSOi53F8sck9t82NHXCta4YVB29mS9wYWdcSKv9QdB04t89/1O/w1cDnyilFU='

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")

    body = request.get_data(as_text=True)
    print(f"📦 Raw body: {body}")

    # ↓ 署名検証
    hash = hmac.new(
        CHANNEL_SECRET.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    computed_signature = base64.b64encode(hash).decode()

    if not hmac.compare_digest(signature, computed_signature):
        print("❌ Invalid signature")
        abort(403)

    print("✅ Valid signature")

    try:
        data = json.loads(body)

        for event in data.get("events", []):
            user_id = event.get("source", {}).get("userId")
            reply_token = event.get("replyToken")

            if user_id and reply_token:
                print(f"📣 userId: {user_id}")
                send_reply(reply_token, f"あなたのuserIdは\n{user_id}\nです。")

        return "OK", 200

    except Exception as e:
        print(f"❌ Exception: {e}")
        return "Bad Request", 400


def send_reply(reply_token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print(f"📤 LINE Reply: {response.status_code} {response.text}")

if __name__ == "__main__":
    app.run(port=5000)
