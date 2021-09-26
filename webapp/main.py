import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageMessage, MessageEvent, TextMessage, TextSendMessage

from fastapi import FastAPI
app = FastAPI()

CHANNEL_SECRET = os.environ['CHANNEL_SECRET']

handler = WebhookHandler(CHANNEL_SECRET)

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

# テキストを受け取る部分
@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    if event.message.text == "ミカンおくるね":
        text = "おっけい！"
    else:
        text = "ミカンまだかい？"

    #linebotのAPIを使っている．ここでTextSendMessageはpython用のLineBotSDK．
    # 引数であるeventの正体は調査中．
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

# FastAPI
@app.get("/")
def hello():
    # Flask
    # host = os.getenv('HOST', '0.0.0.0')
    # port = int(os.getenv('PORT', '5000'))
    # app.run()

    # FastAPI
    return {"Hello": "World"}

if __name__ == '__main__':
    main()
