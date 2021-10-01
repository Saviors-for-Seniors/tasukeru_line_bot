import os
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageMessage, MessageEvent, TextMessage, TextSendMessage

from fastapi import FastAPI, HTTPException, BackgroundTasks 
from starlette.requests import Request

from aiolinebot import AioLineBotApi

import requests

import sys
sys.path.append(os.path.dirname(__file__))
from dialogue_system.bot import Bot

app = FastAPI()

CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']

handler = WebhookHandler(CHANNEL_SECRET)
parser = WebhookParser(CHANNEL_SECRET)
line_bot_api = AioLineBotApi(CHANNEL_ACCESS_TOKEN)

bot = Bot()

@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", "")
    )

    background_tasks.add_task(handle_events, events=events)

    return "ok"

async def handle_events(events):
    for event in events:
        try:
            print(event.message.text)
            await get_bot_reply(event)
        except Exception as e:
            print("Error !!", e)

async def get_bot_reply(event):
    '''ユーザの入力をbotに渡し、返事を取得する'''
    text = event.message.text
    # botから返事を取得する
    reply = bot.reply(text)
    # line botにメッセージを送る
    await line_bot_api.reply_message_async(
        event.reply_token,
        TextMessage(text=reply))

# FastAPI
@app.get("/healthcheck")
def hello():
    return {"Hello": "World"}