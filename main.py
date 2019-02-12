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
app.debug = False

line_bot_api = LineBotApi('fN9eTrok5OB5/jnV2iS7CIuJky0xfG39XXY5ftvbPMFiglJE8m9RA4X5UI3VPuvi2vUTEKJ4bC0ZPLm9/Ipg/akXtiZORldfra3o2korfV/0UbvWSbIfAwl4RHYOQg0I79awhL9fbRJ0j5/HEQmaewdB04t89/1O/w1cDnyilFU=')
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
    print("aa")
    if event.type == "message":
        if (event.message.text == "あ"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='あ')
                ]
            )

if __name__ == "__main__":
    app.run()
    #port = int(os.getenv("PORT"))
    #app.run(host="0.0.0.0", port=port)
