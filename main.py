#coding:utf-8
import os
import sys
from flask import Flask, request, abort, send_file

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, MessageImagemapAction, ImagemapArea, ImagemapSendMessage, BaseSize, LocationSendMessage
)
import requests

app = Flask(__name__)

# 環境変数から各種KEYを取得
channel_secret = os.environ['3df819265eae58584bb90f44c95c07ce']
channel_access_token = os.environ['DqUsUzaNE1qSjeqMYKAVKTnO1DFw2nnE/MvvgQp8cI8WZOCuhi8Hemr8LUcpwX5X2vUTEKJ4bC0ZPLm9/Ipg/akXtiZORldfra3o2korfV8jEDQOTc2OWK00eBenWnoDFJNrRT0e0KzOvbv4qdBRoAdB04t89/1O/w1cDnyilFU=']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

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
    if event.type == "message":
        if (event.message.text == "あ"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='いうえお')
                ]
            )
        if (event.message.text == "か"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="きくけこ")
                ]
            )
        if event.message.text == "さ":
            line_bot_api.reply_message(
                event.reply_token,
                [
                    LocationSendMessage(
                    TextSendMessage(text="しすせそ")
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="まだその言葉は教えてもらってないんです")
                ]
            )

if __name__ == "__main__":
    app.run()
