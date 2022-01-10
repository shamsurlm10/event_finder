import os
from flaskr import mail
from flask_mail import Message

def send_mail(to: str, subject: str, body: str):
    msg=Message("Password Reset Request", 
                sender=os.getenv("MAIL_USERNAME"), 
                recipients=[to])
    
    msg.subject = subject
    msg.body = body
    mail.send(msg)