# # # # # # from flask import Flask, request, abort
# # # # # # from dotenv import load_dotenv
# # # # # # import os
# # # # # # import hmac
# # # # # # import hashlib
# # # # # # import base64
# # # # # # import json
# # # # # # import requests

# # # # # # # .env 読み込み
# # # # # # load_dotenv()

# # # # # # app = Flask(__name__)

# # # # # # # .env に書いたキーを取得
# # # # # # CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")      # 必須
# # # # # # ACCESS_TOKEN    = os.getenv("ACCESS_TOKEN")       # 返信に使う

# # # # # # # -------------------------------
# # # # # # # LINE公式「署名を検証する」サンプルをベースに実装
# # # # # # # -------------------------------

# # # # # # def validate_signature(request_body: str, x_line_signature: str) -> bool:
# # # # # #     """
# # # # # #     公式ドキュメント準拠:
# # # # # #       1. request_body の HMAC-SHA256 を計算
# # # # # #       2. Base64 エンコード
# # # # # #       3. ヘッダーの X-Line-Signature と一致するか比較
# # # # # #     """
# # # # # #     hash_bytes = hmac.new(
# # # # # #         CHANNEL_SECRET.encode('utf-8'),
# # # # # #         request_body.encode('utf-8'),
# # # # # #         hashlib.sha256
# # # # # #     ).digest()
# # # # # #     computed_signature = base64.b64encode(hash_bytes).decode()

# # # # # #     # デバッグ表示
# # # # # #     print(f"🧾 X-Line-Signature: {x_line_signature}")
# # # # # #     print(f"🧮 Computed-Signature: {computed_signature}")

# # # # # #     # 安全な比較
# # # # # #     return hmac.compare_digest(x_line_signature, computed_signature)


# # # # # # @app.route("/callback", methods=["POST"])
# # # # # # def callback():
# # # # # #     # 1) 署名ヘッダー取得
# # # # # #     x_line_signature = request.headers.get("X-Line-Signature", "")
# # # # # #     # 2) リクエストボディ（テキスト）取得
# # # # # #     request_body = request.get_data(as_text=True)

# # # # # #     print("==============================")
# # # # # #     print("✅ Webhook hit")
# # # # # #     print(f"📦 Raw body: {request_body}")

# # # # # #     # 3) 署名検証
# # # # # #     if not validate_signature(request_body, x_line_signature):
# # # # # #         print("❌ Signature validation failed → 403")
# # # # # #         abort(403)   # LINE へ 403 返却

# # # # # #     print("✅ Signature validation success")

# # # # # #     # 4) JSON 解析
# # # # # #     try:
# # # # # #         data = json.loads(request_body)
# # # # # #     except json.JSONDecodeError as err:
# # # # # #         print(f"❌ JSON decode error: {err}")
# # # # # #         return "Bad Request", 400

# # # # # #     # 5) イベント処理
# # # # # #     for event in data.get("events", []):
# # # # # #         user_id     = event.get("source", {}).get("userId")
# # # # # #         reply_token = event.get("replyToken")
# # # # # #         print(f"🔔 eventType={event.get('type')}, userId={user_id}")

# # # # # #         # メッセージイベントのみ返信
# # # # # #         if user_id and reply_token:
# # # # # #             reply_text = f"あなたのuserIdは\n{user_id}\nです。"
# # # # # #             send_reply(reply_token, reply_text)

# # # # # #     return "OK", 200


# # # # # # def send_reply(reply_token: str, text: str):
# # # # # #     """ユーザーにテキスト返信"""
# # # # # #     url = "https://api.line.me/v2/bot/message/reply"
# # # # # #     headers = {
# # # # # #         "Content-Type": "application/json",
# # # # # #         "Authorization": f"Bearer {ACCESS_TOKEN}"
# # # # # #     }
# # # # # #     body = {
# # # # # #         "replyToken": reply_token,
# # # # # #         "messages": [{"type": "text", "text": text}]
# # # # # #     }
# # # # # #     res = requests.post(url, headers=headers, data=json.dumps(body))
# # # # # #     print(f"📤 Reply status={res.status_code}, body={res.text}")


# # # # # # if __name__ == "__main__":
# # # # # #     # debug=True でホットリロード＆詳細トレース有効
# # # # # #     app.run(port=5000, debug=True)
# # # # # from flask import Flask, request
# # # # # from dotenv import load_dotenv
# # # # # import os
# # # # # import json
# # # # # import requests

# # # # # # .env 読み込み
# # # # # load_dotenv()

# # # # # app = Flask(__name__)

# # # # # CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")      # 署名検証を復活させる時に使う
# # # # # ACCESS_TOKEN   = os.getenv("ACCESS_TOKEN")
# # # # # print(f"🔐 ACCESS_TOKEN(先頭10文字): {ACCESS_TOKEN[:10] if ACCESS_TOKEN else 'None'}")
# # # # # print(f"🔐 CHANNEL_SECRET(先頭10文字): {CHANNEL_SECRET[:10] if CHANNEL_SECRET else 'None'}")



# # # # # # ─────────────────────────────
# # # # # # 署名検証をスキップした最小バージョン
# # # # # # ─────────────────────────────
# # # # # @app.route("/callback", methods=["POST"])
# # # # # def callback():
# # # # #     print("✅ webhook hit")
# # # # #     body = request.get_data(as_text=True)
# # # # #     print(f"📦 Raw body: {body}")

# # # # #     # 受信イベントをパースし、メッセージイベントなら userId を返信
# # # # #     try:
# # # # #         data = json.loads(body)
# # # # #         for event in data.get("events", []):
# # # # #             user_id     = event.get("source", {}).get("userId")
# # # # #             reply_token = event.get("replyToken")

# # # # #             if user_id and reply_token:
# # # # #                 print(f"📣 userId: {user_id}")
# # # # #                 send_reply(reply_token, f"あなたのuserIdは\n{user_id}\nです。")
# # # # #     except json.JSONDecodeError as err:
# # # # #         print(f"❌ JSON decode error: {err}")

# # # # #     return "OK", 200   # ← 必ず200を返す

# # # # # # LINEへの返信
# # # # # def send_reply(reply_token: str, text: str):
# # # # #     url = "https://api.line.me/v2/bot/message/reply"
# # # # #     headers = {
# # # # #         "Content-Type": "application/json",
# # # # #         "Authorization": f"Bearer {ACCESS_TOKEN}"
# # # # #     }
# # # # #     payload = {
# # # # #         "replyToken": reply_token,
# # # # #         "messages": [{"type": "text", "text": text}]
# # # # #     }
# # # # #     res = requests.post(url, headers=headers, data=json.dumps(payload))
# # # # #     print(f"📤 Reply status={res.status_code}, body={res.text}")

# # # # # if __name__ == "__main__":
# # # # #     app.run(port=5000, debug=True)

# # # # from flask import Flask, request
# # # # import json
# # # # import os
# # # # import requests
# # # # from dotenv import load_dotenv

# # # # # 環境変数読み込み
# # # # load_dotenv()

# # # # app = Flask(__name__)

# # # # # 環境変数からトークン取得
# # # # ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# # # # print(f"🔐 ACCESS_TOKEN(先頭10文字): {ACCESS_TOKEN[:10] if ACCESS_TOKEN else 'None'}")

# # # # @app.route("/callback", methods=["POST"])
# # # # def callback():
# # # #     print("✅ webhook hit")
    
# # # #     # 生のリクエストボディを取得
# # # #     body = request.get_data(as_text=True)
# # # #     print(f"📦 Raw body: {body}")

# # # #     try:
# # # #         data = json.loads(body)
# # # #         for event in data.get("events", []):
# # # #             user_id = event.get("source", {}).get("userId")
# # # #             reply_token = event.get("replyToken")

# # # #             if user_id:
# # # #                 print(f"📣 userId: {user_id}")

# # # #             if reply_token:
# # # #                 send_reply(reply_token, f"あなたのuserIdは\n{user_id}\nです。")

# # # #         return "OK", 200

# # # #     except Exception as e:
# # # #         print(f"❌ JSON decode error: {e}")
# # # #         return "Bad Request", 400

# # # # def send_reply(reply_token, text):
# # # #     """LINEにメッセージ返信"""
# # # #     url = "https://api.line.me/v2/bot/message/reply"
# # # #     headers = {
# # # #         "Content-Type": "application/json",
# # # #         "Authorization": f"Bearer {ACCESS_TOKEN}"
# # # #     }
# # # #     payload = {
# # # #         "replyToken": reply_token,
# # # #         "messages": [{"type": "text", "text": text}]
# # # #     }

# # # #     res = requests.post(url, headers=headers, data=json.dumps(payload))
# # # #     print(f"📤 LINE Reply: {res.status_code} {res.text}")

# # # # if __name__ == "__main__":
# # # #     app.run(port=5000, debug=True)

# # # from flask import Flask, request
# # # import json

# # # app = Flask(__name__)

# # # # @app.route("/callback", methods=["POST"])
# # # # def callback():
# # # #     print("✅ webhook hit")

# # # #     # リクエストの生データを表示
# # # #     body = request.get_data(as_text=True)
# # # #     print(f"📦 Raw body:\n{body}")

# # # #     try:
# # # #         data = json.loads(body)
# # # #         events = data.get("events", [])
# # # #         print(f"📊 events: {events}")

# # # #         for event in events:
# # # #             print("🔔 Event type:", event.get("type"))
# # # #             print("👤 userId:", event.get("source", {}).get("userId"))

# # # #     except Exception as e:
# # # #         print(f"❌ JSON decode error: {e}")

# # # #     return "OK", 200

# # # # @app.route("/callback", methods=["POST"])
# # # # def callback():
# # # #     body = request.get_data(as_text=True)
# # # #     print("✅ Webhook received")
# # # #     print(f"📦 Raw body: {body}")
# # # #     return "OK", 200

# # # # @app.route("/callback", methods=["POST"])
# # # # def callback():
# # # #     body = request.get_data(as_text=True)
# # # #     with open("log.txt", "a") as f:
# # # #         f.write("✅ Webhook received\n")
# # # #         f.write(f"📦 Raw body: {body}\n")
# # # #     return "OK", 200

# # # @app.route("/callback", methods=["POST"])
# # # def callback():
# # #     body = request.get_data(as_text=True)
# # #     with open("log.txt", "a") as f:
# # #         f.write("✅ Webhook received\n")
# # #         f.write(f"📦 Raw body: {body}\n")
# # #         f.flush()  # ★ここが重要
# # #     return "OK", 200


# # # if __name__ == "__main__":
# # #     app.run(port=5000, debug=True)
# # # from flask import Flask, request

# # # app = Flask(__name__)

# # # @app.route("/callback", methods=["POST"])
# # # def callback():
# # #     try:
# # #         body = request.get_data(as_text=True)
# # #         print("✅ Webhook received")
# # #         print(f"📦 Raw body: {body}")
# # #         return "OK", 200
# # #     except Exception as e:
# # #         print(f"❌ Error: {e}")
# # #         return "ERROR", 200  # ← 必ず200返す（本番ではNG）
        
# # # if __name__ == "__main__":
# # #     app.run(port=5000, debug=True)



# # from flask import Flask, request

# # app = Flask(__name__)

# # @app.route("/callback", methods=["POST"])
# # def callback():
# #     print("✅ Webhook received")
# #     print(f"📦 Raw body: {request.get_data(as_text=True)}")
# #     return "OK", 200

# # if __name__ == "__main__":
# #     app.run(port=5000, debug=True)

# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/callback", methods=["POST"])
# def callback():
#     print("✅ Webhook received")
#     print(f"📦 Raw body: {request.get_data(as_text=True)}")
#     return "OK", 200

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5050, debug=True)  # ★ host を 0.0.0.0 に変更


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
