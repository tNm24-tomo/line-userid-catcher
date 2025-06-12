from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import hmac
import hashlib
import base64
import json
import requests

# .env読み込み
load_dotenv()

app = Flask(__name__)

# 環境変数から読み込み
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# 起動時にトークン表示（確認用）
print(f"🔐 ACCESS_TOKEN(先頭10文字): {ACCESS_TOKEN[:10] if ACCESS_TOKEN else 'None'}")
print(f"🔐 CHANNEL_SECRET(先頭10文字): {CHANNEL_SECRET[:10] if CHANNEL_SECRET else 'None'}")


def validate_signature(request_body: str, x_line_signature: str) -> bool:
    """LINE公式の署名検証ロジック"""
    hash_bytes = hmac.new(
        CHANNEL_SECRET.encode("utf-8"),
        request_body.encode("utf-8"),
        hashlib.sha256
    ).digest()
    computed_signature = base64.b64encode(hash_bytes).decode()
    return hmac.compare_digest(computed_signature, x_line_signature)


@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    x_line_signature = request.headers.get("X-Line-Signature", "")

    print("✅ Webhook received")
    print(f"📦 Raw body: {body}")
    print(f"🧾 X-Line-Signature: {x_line_signature}")

    if not validate_signature(body, x_line_signature):
        print("❌ Signature validation failed")
        abort(403)

    print("✅ Signature validated")

    try:
        data = json.loads(body)
        for event in data.get("events", []):
            user_id = event.get("source", {}).get("userId")
            reply_token = event.get("replyToken")
            if user_id and reply_token:
                reply_text = f"あなたのuserIdは\n{user_id}\nです。"
                send_reply(reply_token, reply_text)
                print(f"📣 userId: {user_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return "Bad Request", 400

    return "OK", 200


def send_reply(reply_token, text):
    """ユーザーに返信メッセージを送る"""
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"📤 Reply status: {response.status_code}, body: {response.text}")


if __name__ == "__main__":
    app.run(port=5050, debug=True)
