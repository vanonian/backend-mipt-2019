FROM python:3-alpine

RUN apk add --update bash

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD messenger.py /messenger.py
ADD wait-for-it.sh /wait-for-it.sh

CMD ["/wait-for-it.sh", "rabbit:5672", "--", "python", "-u", "/messenger.py"]
