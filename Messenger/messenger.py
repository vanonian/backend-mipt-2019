#!/usr/bin/env python3
import pika
import sys
import time
import string
import smtplib
import traceback


def send_email(sender, pwd, subj_tag, recipient, html):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, pwd)
    if subj_tag=="ver":
        body = "\r\n".join((
            "From: %s" % sender,
            "To: %s" % recipient,
            "Subject: Email verification",
            "",
            html
            ))
    else:
        body = "\r\n".join((
            "From: %s" % sender,
            "To: %s" % recipient,
            "Subject: 1,2,3 Check",
            "",
            html
            ))
    server.sendmail(sender, [recipient], body)
    print("Send email: ", body, file=sys.stderr, flush = True)
    server.quit()


def callback(ch, method, properties, body):
    data = body.decode()
    sender, pwd, subj_tag, recipient, html = data.split(';')
    send_email(sender, pwd, subj_tag, recipient, html)
    print("Sended to: ", recipient, '\n', file=sys.stderr, flush = True)

conn_par = pika.ConnectionParameters(host='rabbit', port=5672)
connection = pika.BlockingConnection(conn_par)
channel = connection.channel()

channel.queue_declare(queue='mail')

channel.basic_consume(callback, queue='mail', no_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)
