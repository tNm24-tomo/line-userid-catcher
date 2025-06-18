# LINE Bot - UID取得用ツール

LINE Messaging API を使って、自分自身の `userId` を取得するためのシンプルなWebhookアプリケーションです。

## ✨ 作成者の動漫

Webhook URLを設定しただけで、よくわからないまま `403 Forbidden`、タイムアウト、トーク返信されず...

結果、同じように迷う人を止めるための「完全動作確認済み」リポジトリを作成しました。

---

## 📄 前提

- Python 3.x
- Flask 
- LINE Developers で作成したチャネル
- ngrok アカウント

---

## 📁 構成

```
UID取得/
├── .env
├── webhook.py
└── venv/
```

### .env 内容
```
CHANNEL_SECRET=xxxxxxxxxxxxxxxxxxxx
ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 実行コマンド

### Flask 起動
```bash
python webhook.py
```

### ngrok 起動
```bash
ngrok http 5050
```

Webhook URL: `https://xxxx.jp.ngrok.io/callback` に設定

---

## 📂 webhook.py (署名検証 + userId 返信)

```python
from flask import Flask, request, abort
import os, json, hmac, hashlib, base64, requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get("X-Line-Signature", "")

    # 署名検証
    hash = hmac.new(CHANNEL_SECRET.encode(), body.encode(), hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode()

    if not hmac.compare_digest(signature, computed_signature):
        abort(403)

    data = json.loads(body)
    for event in data.get("events", []):
        user_id = event.get("source", {}).get("userId")
        reply_token = event.get("replyToken")

        if user_id and reply_token:
            print(f"📣 userId: {user_id}")
            send_reply(reply_token, f"あなたのuserIdは\n{user_id}\nです。")

    return "OK", 200

def send_reply(token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "replyToken": token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
```

---

## 🚫 よくある誤動

| 現象 | 原因 |
|--------|--------|
| 403 Forbidden | 署名不一致/署名検証無視/環境変数None |
| ターミナルに出力がない | `print`は出るがWebhookそもそも来てない |
| 返信がない | ACCESS_TOKEN 間違い or 勝手に`None` |
| ポート 5000 使用中 | AirPlay or 別プロセスが占有中 |

---

## ✅ 使い道

- userId取得のみを用途とした初期試験
- 現場でのWebhook動作確認
- LIFFやPush利用前の初期テスト

---

## 💼 LICENSE

MIT License
