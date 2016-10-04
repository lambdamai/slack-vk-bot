from flask import Flask, abort, request, render_template

from auth import auth_facebook, auth_slack
from config import *
from message import *

app = Flask(__name__)

cfg = {
	'page_id'     : page_id_,
	'access_token': access_token_
}


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/callback/xE4sA', methods=['GET', 'POST'])
def callback():
	if not request.json or 'type' not in request.json:
		abort(400)

	if request.json['type'] == 'confirmation':
		return confirmation_token_

	if request.json['type'] == 'wall_post_new':
		post = request.json['object']

		slack_message = Slack(post=post).create_message()
		Slack.send_message(auth=slack, channel=channel_, text=text_, attachments=slack_message)

		facebook_post = Facebook(post=post)
		facebook_attachment = facebook_post.create_message()
		facebook_text = facebook_post.get_text(post=post)
		Facebook.send_message(auth=facebook, text=facebook_text, attachment=facebook_attachment)

		return 'ok', 200


slack = auth_slack()

facebook = auth_facebook(cfg=cfg)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
