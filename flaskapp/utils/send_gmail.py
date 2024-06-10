import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_otp_email(email,password,to_email,body,subject):
    try:
        host = "smtp-mail.outlook.com"
        port = 587

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = email
        message['To']= to_email

        html = body
        
        html_part = MIMEText(html, 'html')
        message.attach(html_part)

        smtp = smtplib.SMTP(host,port)
        smtp.starttls()
        smtp.login(email,password)
        smtp.sendmail(email, to_email, message.as_string())
        smtp.quit()

        return True

    except Exception as e:
        return False
    
# print(send_otp_email("sankalp2004developer@outlook.com", "Developer@2004", "sankalp2004gaikwad@gmail.com", 3456))
