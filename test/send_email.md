# Send email

## setting.py

``python``

    #已註冊，可直接使用
    
    EMAIL_HOST_USER = 'emailverify813024@gmail.com'  #寄件者電子郵件
    EMAIL_HOST_PASSWORD = 'ypxmmwshavsppnkn'  #Gmail應用程式的密碼

``

## view.py

``python``

    import smtplib
    from django.conf import settings
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from django.template import Template, Context
    from pathlib import Path
    
    # example sendEmail("ian66666@gmail.com", 'localhost:8000/admin/')
    def sendEmail(receiver, verifyUrl):
        print(verifyUrl)
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "Learn Code With Mike"  #郵件標題
        content["from"] = settings.EMAIL_HOST_USER  #寄件者
        content["to"] = receiver #收件者
        
        template = Template(Path("test/templates/email.html").read_text())
        context = Context({'verifyUrl': verifyUrl})
        body = template.render(context)
        content.attach(MIMEText(body, 'html'))  #郵件內容
        
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login(settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD)  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)

``