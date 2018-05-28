class Menu(object):
     """docstring for Menu"""
     def __init__(self, arg):
         super(Menu, self).__init__()
         self.arg = arg
          
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
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='https://www.facebook.com/'
                    )
                ]
            )
        )