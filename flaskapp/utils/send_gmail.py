"""
This module contains the send_otp_email method,
which is used to send an OTP email to the user.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import jsonify


def send_otp_email(email,password,to_email,body,subject):
    """
    This method is used to send an OTP email to the user.
    """
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

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp
