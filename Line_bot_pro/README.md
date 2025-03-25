您好，這是一個簡單的 OpenAI LINEBOT 聊天機器人。
<br>
首先請安裝並啟動 ngrok
```
ngrok http 5000
```
注意!啟動後先不要關閉cmd視窗。
將本地服務映射到 ngrok 提供的公開網址。
<br>
設定環境變數:OPENAI_API_KEY
並自行去開設Line帳號，取得：CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN
<br>

啟動範例程式碼，確認可以接收到 Webhook 事件。
<br>
將 ngrok 提供的公開網址配置到 LINE Developer 中的 Webhook 設定。
<br>
測試訊息是否能正確回傳。
<br>

<br>
您可以透過指令下載完整程式碼：
<br>
```
git clone https://github.com/sharon-hy97/mariadb_dialog.git
```

進入資料夾後先執行：requiment.txt 安裝所有需要的套件
<br>
```
pip reOOOO.txt
```

這會讓您所有下載內容變成腳本，可以直接運用。
<br>
<br>
此只需修改第53行中的機器人基本設定：
<br>
```
"content": "你是一個客服機器人，請使用正體中文zh-tw回應"
```
<br>