from flask import Flask, request, abort
from auth import auth_slack

GROUP_DOMAIN = 'lambdafrela'
CONFIRMATION_TOKEN = '55a22c56'

app = Flask(__name__)


@app.route('/callback/xE4sA', methods=['GET', 'POST'])
def callback():
	if not request.json or 'type' not in request.json:
		abort(400)

	if request.json['type'] == 'confirmation':
		return CONFIRMATION_TOKEN

	if request.json['type'] == 'wall_post_new':
		slack = auth_slack()
		object = request.json['object']
		text = object['text']
		slack.chat.postMessage('#admin', text, username='vk-bot')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
