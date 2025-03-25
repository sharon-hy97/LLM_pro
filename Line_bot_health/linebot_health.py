from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from openai import OpenAI
import boto3  # 匯入 boto3 用於存取 Parameter Store
import json
import logging

# 設定 Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 使用 boto3 客戶端存取 Parameter Store
ssm_client = boto3.client('ssm')

def get_parameter(name):
    """從 Parameter Store 獲取參數"""
    try:
        response = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"無法從 Parameter Store 獲取參數 {name}: {e}")
        raise

# 從 Parameter Store 獲取必要參數
CHANNEL_SECRET = get_parameter('/linebot/channel_secret')
CHANNEL_ACCESS_TOKEN = get_parameter('/linebot/channel_access_token')
OPENAI_API_KEY = get_parameter('/openai/api_key')

# 初始化 OpenAI 客戶端
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# 初始化 Line Bot API 和 Webhook Handler
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def get_openai_chat_completion(user_message):
    """使用 OpenAI API 獲取回應"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
    ai_reply = response.choices[0].message.content.strip()
    return ai_reply

def lambda_handler(event, context):
    # get request body as text
    body = event['body']
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        json_data = json.loads(body)
        # 獲取 replyToken 和訊息內容
        event_object = json_data['events'][0]
        reply_token = event_object['replyToken']
        user_message = event_object['message']['text']
        
        #記錄使用者訊息
        logger.info(f"收到使用者訊息: {user_message}")

        # 呼叫 OpenAI 獲取回應
        ai_reply = get_openai_chat_completion(user_message)

        #記錄機器人回應
        logger.info(f"機器人回應: {ai_reply}")
        
        # 使用 Line Messaging API 回應用戶
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=ai_reply)
        )

    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature.")
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
        }

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }