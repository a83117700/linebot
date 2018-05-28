# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, PostbackEvent,
)
import Luis_handler

import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

app = Flask(__name__)

handler = WebhookHandler('99dd2331052c6790122bbf11df028ac1') 
line_bot_api = LineBotApi('Hr4G/v9C8g+GDrUeyBN0t0u9WlqjxBsUOuRJquRl7mOd/QVOzC5ac7EZs8ZOVLFbbOYh/N5eVl7Lurmcx+4dUGpszUTapHFu2TT6eeHjCnuBlrRIOEeLWaxzbYejsfzx6APLyxPYH+AXD8zulT/TFQdB04t89/1O/w1cDnyilFU=') 

global status 
status = 'init'

@app.route('/')
def index():
    return "<p>Hello World!</p>"

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


# ================= 機器人區塊 Start =================


@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
    text = event.message.text #message from user
    global status


    if event.message.text != "":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
        pass
        #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'sweet-man-d9c2b8272f1f.json'
        GSpreadSheet = 'food'
        while True:
            try:
                scope = ['https://spreadsheets.google.com/feeds']
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                worksheet = gc.open(GSpreadSheet).sheet1
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt=""
            textt+=event.message.text
            if textt!="":
                worksheet.append_row((datetime.datetime.now(), textt))
                print('新增一列資料到試算表' ,GSpreadSheet)
                return textt    
    
    if(status == 'init'):
        if(text == 'Hi'):
            message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://i.imgur.com/1z9Uxdg.jpg',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackTemplateAction(
                                label='功能維修中',
                                text='我手賤想點',
                                data='no'
                            ),
                            PostbackTemplateAction(
                                label='紀錄食物喜好',
                                text='紀錄食物喜好',
                                data='food'
                            ),
                            URITemplateAction(
                                label='偷看帥哥FB',
                                uri='https://www.facebook.com/'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token,message)
        else:
            message = TextSendMessage(text = text)
            line_bot_api.reply_message(event.reply_token,message)
    elif(status == 'food'):
        text_entity = Luis_handler.luis(text)
        if(text == 'Hi'):
            global status
            status = 'init'
            msg = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://i.imgur.com/1z9Uxdg.jpg',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackTemplateAction(
                                label='功能維修中',
                                text='我手賤想點',
                                data='no'
                            ),
                            PostbackTemplateAction(
                                label='紀錄食物喜好',
                                text='紀錄食物喜好',
                                data='food'
                            ),
                            URITemplateAction(
                                label='偷看帥哥FB',
                                uri='https://www.facebook.com/'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token,msg)
        elif(text == '紀錄食物喜好'):
            pass
        elif(type(text_entity) is str):
            msg = text_entity+'\n若已紀錄完請輸入Hi回到選單'
            message = TextSendMessage(text = msg)
            line_bot_api.reply_message(event.reply_token,message)
        else:
            msg = '已記錄: '+str(text_entity['like'])+str(text_entity['store'])+str(text_entity['size'])+str(text_entity['flavor'])+str(text_entity['food'])+'\n請繼續紀錄，或輸入Hi回到選單'
            msg = msg.replace('None','')
            message = TextSendMessage(text = msg)
            line_bot_api.reply_message(event.reply_token,message)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'food':
        global status
        status = 'food'
        msg = '請以一句話詳細的紀錄她喜歡或討厭的食物\n紀錄完請輸入Hi回到選單'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=msg))
    """elif event.postback.data == 'datetime_postback':
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
                elif event.postback.data == 'date_postback':
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=event.postback.params['date']))"""


# ================= 機器人區塊 End =================

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
