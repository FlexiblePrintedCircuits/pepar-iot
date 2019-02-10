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

app = Flask(__name__)

line_bot_api = LineBotApi('AJ03tYuaMQXQNXojwbdDSah6XbwAYtpISFrGz7T8A6tVgmRL6wMt3Q2W5qdAPWXY2vUTEKJ4bC0ZPLm9/Ipg/akXtiZORldfra3o2korfV+ooBQ61n0LFbpWjsTxl2X36qIN9x8sCk/xoIesLy7fhQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1a78827b03d52b212fbea6a431718d18')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="hogehoge"))


if __name__ == "__main__":
    app.run()
