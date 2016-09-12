from flask import Flask, request, abort

from auth import auth_slack
from config import *
from message import *

app = Flask(__name__)


def send_message(channel, text=text_, attachments=None, as_user=True):
	slack.chat.post_message(channel=channel,
							text=text,
							attachments=attachments,
							as_user=as_user)


@app.route('/callback/xE4sA', methods=['GET', 'POST'])
def callback():
	if not request.json or 'type' not in request.json:
		abort(400)

	if request.json['type'] == 'confirmation':
		return confirmation_token_

	if request.json['type'] == 'wall_post_new':
		post = request.json['object']
		attachments = create_msg(post)
		send_message(channel=channel_, text=text_, attachments=attachments)
		return 'ok', 200


slack = auth_slack()

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
