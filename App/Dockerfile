FROM python:3-alpine

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD first_app.py /first_app.py
ADD config.py /config.py
ADD web_app /web_app
ADD migrations /migrations

ADD run.sh /run.sh

EXPOSE 5000

CMD ["/run.sh"]
