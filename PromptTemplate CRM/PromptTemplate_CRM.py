from openai import OpenAI
client = OpenAI(api_key="")

print(f"您好，歡迎使用客服機器人，請輸入您的退貨資訊... (請按 Enter 繼續...)")
a = input("消費者姓名：")
b = input("訂單編號：")
c = input("收貨地址：")
d = input("E-Mail:")

def chat(mes):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一個客服機器人，請處理客戶(user)服務事項，文體以電子郵件格式回覆，字體為繁體中文"},
            {"role": "user", "content": mes}
            ])
    #加content才不會有前後面的亂碼
    return(completion.choices[0].message.content)
mes = f"填寫退貨明細，訂單編號為:  {b} ，消費者姓名: {a}，地址: {c}，E-Mail： {d}"
print(chat(mes))
