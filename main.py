from flask import Flask, jsonify, request, abort
from auth import auth_slack

GROUP_DOMAIN = 'lambdafrela'
CONFIRMATION_TOKEN = '55a22c56'

app = Flask(__name__)

slack = auth_slack()


@app.route('/', methods=['POST'])
def index(slack):
	if not request.json or 'type' not in request.json:
		abort(400)
	if request.json['type'] == 'confirmation':
		return CONFIRMATION_TOKEN, 201
	if request.json['type'] == 'wall_post_new':
		object = request.json['object']
		text = object['text']
		slack.chat.postMessage('#admin', text, username='vk-bot')

if __name__ == '__main__':
	app.run(debug=True)
