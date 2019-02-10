from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["AJ03tYuaMQXQNXojwbdDSah6XbwAYtpISFrGz7T8A6tVgmRL6wMt3Q2W5qdAPWXY2vUTEKJ4bC0ZPLm9/Ipg/akXtiZORldfra3o2korfV+ooBQ61n0LFbpWjsTxl2X36qIN9x8sCk/xoIesLy7fhQdB04t89/1O/w1cDnyilFU="]
#channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#channel_secret = os.environ["LINE_CHANNEL_SECRET"]
LINE_CHANNEL_SECRET = os.environ["1a78827b03d52b212fbea6a431718d18"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
#line_bot_api = LineBotApi(channel_access_token)
#handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="hogehoge"))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
