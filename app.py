# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('')
# 必須放上自己的Channel Secret
handler = WebhookHandler('')
# 必須放上自己的ID
line_bot_api.push_message('', TextSendMessage(text='上線囉！'))

# 監聽所有來自 /callback 的 Post Request
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

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('你好',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('你好！'))
    elif re.match('版本',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('雲端版本04011108'))
    elif re.match('看菜單',message):        
        image_message = ImageSendMessage(
            original_content_url='https://cpok.tw/wp-content/uploads/2022/11/unnamed-file-110.jpg',
            preview_image_url='https://whityeat.com/wp-content/uploads/20201127033420_6.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message) 
    elif re.match('餐廳位置',message):
        location_message = LocationSendMessage(
            title='中國文化大學推廣教育部建國校區',
            address='(大夏館)',
            latitude=25.02630789511882,
            longitude=121.53799565219462          
        )
        line_bot_api.reply_message(event.reply_token, location_message)    
    elif re.match('訂位',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='問問題',
            template=ConfirmTemplate(
                text='選擇用餐時段',
                actions=[
                    PostbackAction(
                        label='午餐',
                        display_text='你選擇午餐',
                        data='action=其實不喜歡'
                    ),
                    MessageAction(
                        label='晚餐',
                        text='你選擇晚餐'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)                    
    elif re.match('點餐',message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='免費教學影片',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://cpok.tw/wp-content/uploads/2023/03/11.png',
                        action=PostbackAction(
                            label='麥當勞套餐',
                            display_text='麥當勞套餐',
                            data='action=麥當勞套餐回傳'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://s3.goodlife.tw/system/att/000/015/212/image/1485386709.png',
                        action=PostbackAction(
                             label='肯德基套餐',
                            display_text='肯德基套餐',
                            data='action=肯德基套餐回傳'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://www.mos.com.tw/Upload/images/202107/202107-%E5%B1%85%E5%AE%B6%E9%98%B2%E7%96%AB%E5%84%AA%E6%83%A0%E5%B0%88%E5%8D%80EDM-%E6%97%A9%E9%A4%90.jpg',
                        action=PostbackAction(
                             label='摩斯套餐',
                            display_text='摩斯套餐',
                            data='action=摩斯套餐回傳'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)          
    elif re.match('查紀錄',message):
         line_bot_api.reply_message(event.reply_token,TextSendMessage('開發中'))            
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
