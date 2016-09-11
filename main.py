import json

from flask import Flask, request, abort

from auth import auth_slack, auth_vk
from config import *

app = Flask(__name__)


def create_msg(post):
	try:
		if post['copy_history']:
			post = post['copy_history'][0]
			author = vk.groups.getById(group_id=str(post['owner_id'])[1:])[0]
			author_name = author['name']
			author_link = 'https://vk.com/' + author['screen_name']
			author_icon = author['photo']
	except KeyError:
		author_icon, author_link, author_name = None, None, None

	try:
		if post['attachments'] and post['attachments'][0]['type'] == 'photo':
			photo = post['attachments'][0]
			image_url = photo['photo']['photo_1280']
			thumb_url = photo['photo']['photo_130']
	except KeyError:
		image_url, thumb_url = None, None

	text = post['text']
	ts = post['date']

	return json.dumps([{
		'fallback'   : '',
		'color'      : '#0093DA',
		'text'       : text,
		'ts'         : ts,
		'footer'     : 'Lambda ФРЭЛА | Лямбда',
		'footer_icon': 'http://lambda-it.ru/static/img/lambda_logo_mid.png',
		'image_url'  : image_url,
		'thumb_url'  : thumb_url,
		'author_name': author_name,
		'author_icon': author_icon,
		'author_link': author_link,
		'mrkdwn_in'  : ['text'],
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


vk = auth_vk()
slack = auth_slack()

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
