import json

from flask import Flask, request, abort

from auth import auth_slack
from config import *

app = Flask(__name__)


def create_msg(post):
	text = post['text']
	footer = 'Lambda ФРЭЛА | Лямбда'
	ts = post['date']
	return json.dumps([{
		'fallback'   : '',
		'color'      : '#0093DA',
		'text'       : text,
		'ts'         : ts,
		'footer'     : footer,
		'footer_icon': 'http://lambda-it.ru/static/img/lambda_logo_mid.png',
	}]
	)


def send_message(channel, text='', attachments=None, as_user=True):
	slack.chat.post_message(channel=channel,
							text=text,
							attachments=attachments,
							as_user=as_user)


@app.route('/callback/xE4sA', methods=['GET', 'POST'])
def callback():
	if not request.json or 'type' not in request.json:
		abort(400)

	if request.json['type'] == 'confirmation':
		return confirmation_token

	if request.json['type'] == 'wall_post_new':
		post = request.json['object']
		send_message(channel=channel, text=text, attachments=create_msg(post))
		return 'ok', 200


slack = auth_slack()

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
