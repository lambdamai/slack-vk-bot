FROM python:alpine

RUN apk update && \
	apk add py-gunicorn && \
	rm -rf /var/cache/apk/*

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code

EXPOSE 5000

# Start gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "main:app"]