FROM python:alpine

RUN apk update && \
	apk add py-gunicorn && \
	rm -rf /var/cache/apk/*

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Start gunicorn
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "main:app"]