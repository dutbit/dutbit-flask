import os
import time
from email.message import EmailMessage
from smtplib import SMTP_SSL
from threading import Thread

from flask import current_app

SENDER = "dutbit@163.com"


def send_mail(to, subject, content):
    if current_app.config["DEBUG"] and not os.getenv("FLASK_MAIL_PASS"):
        return
    Thread(target=t_send_mail, args=(to, subject, content)).start()


def t_send_mail(to, subject, content):
    print("sleep1")
    time.sleep(3)
    print("sleep2")
    msg = create_mail(to, subject, content)
    smtpObj = SMTP_SSL("smtp.163.com", 465)
    smtpObj.login(SENDER, os.getenv("MAIL_PASS"))
    smtpObj.send_message(msg)
    print("sleep3")


def create_mail(to, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg["From"] = SENDER
    msg["To"] = to
    msg["Subject"] = subject
    return msg
