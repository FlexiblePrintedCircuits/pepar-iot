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

#LINE Access Token
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["3df819265eae58584bb90f44c95c07ce"]
#LINE Channel Secret
YOUR_CHANNEL_SECRET = os.environ["KFwpfQ+ftxQRMW7yANM+tJSr2c2v/pEyI4w8hViLr9Yfe8o6KohebcwjZHB79Kk+2vUTEKJ4bC0ZPLm9/Ipg/akXtiZORldfra3o2korfV9dBatRCr9uR246Dqm6TTyxosRKlMP/SyQxrJ9xC9mxjAdB04t89/1O/w1cDnyilFU="]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
