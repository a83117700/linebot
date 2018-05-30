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
import os
import Luis_handler
import google_sheet

app = Flask(__name__)

handler = WebhookHandler('99dd2331052c6790122bbf11df028ac1') 
line_bot_api = LineBotApi('Hr4G/v9C8g+GDrUeyBN0t0u9WlqjxBsUOuRJquRl7mOd/QVOzC5ac7EZs8ZOVLFbbOYh/N5eVl7Lurmcx+4dUGpszUTapHFu2TT6eeHjCnuBlrRIOEeLWaxzbYejsfzx6APLyxPYH+AXD8zulT/TFQdB04t89/1O/w1cDnyilFU=') 

global status 
status = 'init'
global user_ID


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
                                label='查詢她的喜好',
                                text='查詢她的喜好',
                                data='retrieve'
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
                                label='查詢她的喜好',
                                text='查詢她的喜好',
                                data='retrieve'
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
            #try:
            global user_ID
            user_ID = event.source.user_id
            google_sheet.insert_sheet(
                                        user_ID, 
                                        str(text_entity['food']), 
                                        str(text_entity['like']), 
                                        str(text_entity['flavor']), 
                                        str(text_entity['size']), 
                                        str(text_entity['store'])
                                        )
            """except:
                                                    message = TextSendMessage(text = '紀錄失敗啦幹')
                                                    line_bot_api.reply_message(event.reply_token,message)"""

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
    elif event.postback.data == 'retrieve':
        """global status
                                status = 'retrieve'"""
        msg = '她的喜好是...'
        global user_ID
        user_ID = event.source.user_id
        google_sheet.retrieve(user_ID, 'like')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=msg))
    """elif event.postback.data == 'datetime_postback':
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
                elif event.postback.data == 'date_postback':
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=event.postback.params['date']))"""


# ================= 機器人區塊 End =================

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
