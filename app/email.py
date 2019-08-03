from flask import Flask
from flask_mail import Mail, Message
from threading import Thread

def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)

def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
  recipients=[to])
  msg.body = "This is a test message!"
  msg.html = "Flasky testing <b> Archu </b>"
  thr = Thread(target=send_async_email, args=[app,msg])
  thr.start()
  return thr
