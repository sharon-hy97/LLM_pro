您好，這是一個簡單的 LINEBOT 健康小助理。
<br>
您可以透過指令下載完整程式碼：
<br>
```
git clone https://github.com/sharon-hy97/LLM_pro.git
```
<br>
1. 請先進入 Line_bot_health 資料夾
<br>
2. 請先將 final_lambda_package.zip 上傳至 AWS S3 (因為超過 10mb)，資料桶要注意地區。
<br>
3. 再到 Parameter Store 中儲存環境變數，例如 /linebot/channel_secret 和 /linebot/channel_access_token。

<br>
3. 更新 Lambda IAM 權限，因 Lambda 函數需要權限來存取 Parameter Store 的參數，所以需要編輯 Lambda 的 IAM 角色。例如：添加 Systems Manager 存取權限，AmazonSSMReadOnlyAccess 與 AmazonSSMFullAccess。
<br>
將 linebot_health.py 部署到 Lambda 後執行，即可在連接的 line 帳號進行對話。
```
python3 linebot_health.py
```
<br>