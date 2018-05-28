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
    ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
)
#import Luis_handler

app = Flask(__name__)

handler = WebhookHandler('99dd2331052c6790122bbf11df028ac1') 
line_bot_api = LineBotApi('Hr4G/v9C8g+GDrUeyBN0t0u9WlqjxBsUOuRJquRl7mOd/QVOzC5ac7EZs8ZOVLFbbOYh/N5eVl7Lurmcx+4dUGpszUTapHFu2TT6eeHjCnuBlrRIOEeLWaxzbYejsfzx6APLyxPYH+AXD8zulT/TFQdB04t89/1O/w1cDnyilFU=') 


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
    data = event.message.data

    if(text == 'postback text'):
        message = TextSendMessage(text = data)
        line_bot_api.reply_message(event.reply_token,message)
    elif(text == '請以一句話詳細的輸入你喜歡或討厭的食物'):
        message = TextSendMessage(text = '不愛阿你長那麼醜')
        line_bot_api.reply_message(event.reply_token,message)
    else:
        message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/1z9Uxdg.jpg',
                    title='Menu',
                    text='Please select',
                    actions=[
                        PostbackTemplateAction(
                            label='postback',
                            text='postback text',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='紀錄食物喜好',
                            text='請以一句話詳細的輸入你喜歡或討厭的食物'
                        ),
                        URITemplateAction(
                            label='偷看帥哥FB',
                            uri='https://www.facebook.com/'
                        )
                    ]
                )
            )
        #message = TextSendMessage(text = text)
        line_bot_api.reply_message(event.reply_token,message)


    # 針對使用者各種訊息的回覆 Start =========
    #line_bot_api.reply_message(event.reply_token,message)
        #TextSendMessage(text=msg)
        

    # 針對使用者各種訊息的回覆 End =========

# ================= 機器人區塊 End =================

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
