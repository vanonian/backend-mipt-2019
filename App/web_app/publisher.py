import os
import pika
import sys
import time

class Publisher():

    def connect(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(self.conn_par)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue='mail')
                break

            except Exception as e:
                print('Problem: \n', e, file=sys.stderr, flush = True)
                time.sleep(5)

    def __init__(self):
        self.conn_par = pika.ConnectionParameters(host='rabbit', port=5672)

        #MUST understand why wait-for-it doesn't work and I have to invent bike
        #But I can reconnect if my heart had stoped
        self.connect()

    def publish_task(self, sender, pwd, subj_tag, email, html):
        data = ";".join(["ishmukruslan@gmail.com","ApotoxinE4869","ver", email, html])
        while True:
            try:
                self.channel.basic_publish(exchange='', routing_key='mail', body=data)
                print('Sended task:', email, "\n", file=sys.stderr, flush=True)
                break
            except pika.exceptions.ConnectionClosed as e:
                print('Problem: \n', e, file=sys.stderr, flush = True)
                time.sleep(5)
                self.connect()
