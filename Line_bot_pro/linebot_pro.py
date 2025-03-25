# 引入 Flask 框架處理 HTTP 請求
from flask import Flask, request

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from openai import OpenAI

# 初始化 Flask，建立一個 Flask 應用程式實例，__name__ 是當前模組名稱，Flask 會根據這個名稱來識別應用程式。
app = Flask(__name__)

#CHANNEL_SECRET:鑰去linebot網站找
CHANNEL_SECRET = ""
#CHANNEL_ACCESS_TOKEN:要去linebot網站找
CHANNEL_ACCESS_TOKEN = ""

#設定根路由，這個路由會回應 GET 請求，簡單返回 "Hi" 來檢查伺服器是否正常運行。
@app.route("/", methods=['GET'])
def home():
    return "Hi"

#設定根路由，這個路由會處理來自 LINE 平台的 POST 請求，即當用戶發送訊息到 LINE Bot 時會觸發這個路由。
@app.route("/", methods=['POST'])
def linebot():
    #讀取來自 HTTP 請求的原始數據（用戶發送的訊息）。
    body = request.get_data(as_text=True)
    #將從請求中取得的 JSON 字串解析為 Python 字典。
    json_data = json.loads(body)
    print(json_data)
    try:
        #初始化 LineBotApi 實例，這個實例用來與 LINE 平台交互，發送訊息等。
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        #初始化 WebhookHandler 實例，這個實例用來處理 webhook 請求的簽名驗證等操作。
        handler = WebhookHandler(CHANNEL_SECRET)
        #從請求的 headers 中取得 LINE 的簽名，用於驗證請求是否來自 LINE 平台。
        signature = request.headers['X-Line-Signature']
        #處理 LINE 發送過來的 webhook 資料，並驗證簽名。
        handler.handle(body, signature)
        #初始化 OpenAI 客戶端，用來與 GPT-4 模型進行對話。
        client = OpenAI()
        #解析出 LINE 發送過來的 replyToken，這是用來回覆訊息的關鍵。
        #先前通過 json.loads(body) 解析的 Python 字典。從這個字典中的event提取資料
        #每個事件都有一個 replyToken，它是用來回覆訊息的唯一標識符。當你從 LINE 接收到一個訊息時，你需要使用這個 replyToken 來回應 LINE 平台，並確保訊息能正確地發送回給對應的用戶。
        tk = json_data['events'][0]['replyToken']         # 取得 reply token

        #message 物件可以包含多種不同類型的訊息，如文字訊息（text）、圖片（image）等。在這裡，我們關心的是用戶發送的文字訊息，因此會從中提取 text 屬性。
        #從第一個事件的 message 屬性中提取出用戶發送的文字訊息，並將其存儲在變數 msg 中。這樣，你就可以使用 msg 來處理用戶的訊息，並將它傳遞給 GPT 模型進行處理。
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息

        #呼叫 OpenAI API，將用戶的訊息傳遞給 GPT-4 模型進行處理並獲得回應。
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "你是一個客服機器人，請使用正體中文zh-tw回應"},
                   {"role": "user", "content": msg}]) #
        #將 GPT 模型的回應包裝成 LINE Bot 可以發送的訊息格式。
        text_message = TextSendMessage(text = completion.choices[0].message.content)          # 回傳同樣的訊息
        #在python中輸出要回復的訊息
        print(completion.choices[0].message.content)
        # 使用 LINE Messaging API 回應用戶訊息
        line_bot_api.reply_message(tk, text_message)       # 回傳訊息
        
    except Exception as e:
        # 捕獲任何錯誤並打印錯誤訊息
        print('error: ' + str(e))
    # 回應 HTTP 請求，表示處理成功
    return 'OK'

# 啟動 Flask 伺服器，監聽 5000 端口
app.run(port="5000")

