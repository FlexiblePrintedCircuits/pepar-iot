#最終更新日: 2019/02/26
#このプログラムは鳥羽商船高専のI1弓削が書いたものです。
#いろんなサイトからコピーしてるところもあるので著作権どうちゃらは知りません。
#LINE　BOTのサーバはherokuを使っています
#注釈がだいぶ適当ですが、許して下さい
#変数名がクソとか関数名がクソとかはごめんやけど僕のネーミングセンスが悪いだけです。許してちょんまげ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
import os
import imaplib
import email
from time import sleep

app = Flask(__name__)
app.debug = False
#Flaskではデフォルトでデバッグモードがオンなので、デバッグデバッグモードをオフにする

#トークンとシリアルキーを登録
line_bot_api = LineBotApi(your_api_token)
handler = WebhookHandler(your_serial_key)

global GetPeparDis

def GetMail():
    mail=imaplib.IMAP4_SSL('imap.gmail.com',993)
    mail.login(your_email,your_pass)
    mail.select('inbox')

    type,data=mail.search(None,'ALL')
    #while(1):
    for i in data[0].split():
        #受信しているメール取得
        #文字コードはiso-2022-jp
        ok,x=mail.fetch(i,'RFC822')
        ms=email.message_from_string(x[0][1].decode('iso-2022-jp'))

        #メールの内容だけを取得
        maintext=ms.get_payload()
        global Strmaintext
        Strmaintext=str(maintext)

        #最新のメールだけ欲しいので、最後の２文字を取得
        #データは１６進文字列で取得される
    Strmaintext=Strmaintext[-6:-4]
    #取得した１６進文字列を数値型１０進に変換
    Intmaintext=int(Strmaintext, 16)

    if (Intmaintext >= 5):
        return 10
    elif (Intmaintext < 5) and (Intmaintext >= 4):
        return 20
    elif (Intmaintext < 4) and (Intmaintext >= 3):
        return 30
    elif (Intmaintext < 3) and (Intmaintext >= 2):
        return 40
    elif (Intmaintext < 2):
        return 50

@app.route("/", methods=['GET'])
def webhook():
    PushDis = GetMail()

    if PushDis == 10:
        user_id = "Ue8baeea0f29de588e397c74e7b3dcf31"

        messages = TextSendMessage(text="あと１０ｍ以下です！早めの補充を！")
        line_bot_api.push_message(user_id, messages=messages)

        messagesImage = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg"
        )
        line_bot_api.push_message(user_id, messages=messagesImage)

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

def make_image_message(PeparDis):
    #トイレットペーパーの厚みから適切な画像を返す関数
    #LINEBOTはhttpsじゃないとできないので、httpでなくhttpsで画像を指定
    #画像ファイルはpngでなくjpeg形式
    #画像サイズにも制約があるが忘れた。調べてくれ。

    global messages

    #original_content_urlは、送信した画像をタッチしたら開く画像
    #preview_image_urlは、送信したら勝手に見える画像のプレビュー
    if (PeparDis == 50):
        messages = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214183132.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214183132.jpg"
        )
        return messages
    elif (PeparDis == 40):
        messages = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182919.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182919.jpg"
        )
        return messages
    elif (PeparDis == 30):
        messages = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182922.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182922.jpg"
        )
        return messages
    elif (PeparDis == 20):
        messages = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182925.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182925.jpg"
        )
        return messages
    elif (PeparDis == 10):
        messages = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg"
        )
        return messages

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.type == "message":
        if (event.message.text == "あとどれぐらい？"):
            SendMes = GetMail()
            SendImage = make_image_message(SendMes)
            SendMes = str(SendMes)
            SendMessage = ("あと" + SendMes + "m以下です！")
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=SendMessage),
                    messages
                ]
            )
        if (event.message.text == "ユーザーIDを教えて"):
            #これはテスト用。特に意味はない
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=event.source.user_id)
                ]
            )

if __name__ == "__main__":
    #環境によるがapp.run()だけでは動かなかったはず
    #ローカル環境で動いてもherokuで動くとは限らないのでポートを指定する
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)