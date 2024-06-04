import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_otp_email(email,password,to_email,otp):
    try:
        host = "smtp-mail.outlook.com"
        port = 587

        message = MIMEMultipart('alternative')
        message['Subject'] = "Verify Email"
        message['From'] = email
        message['To']= to_email

        html = """<html>
        <head></head>
<body>
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
          <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
          </div>
          <p style="font-size:1.1em">Hi,</p>
          <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
          <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
          <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
          <hr style="border:none;border-top:1px solid #eee" />
          <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
            <p>Your Brand Inc</p>
            <p>1600 Amphitheatre Parkway</p>
            <p>California</p>
          </div>
        </div>
      </div>
</body>
        
        </html>""".format(otp=otp)
        
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
