from flask import Flask, abort, request, render_template

import config
from auth import auth_slack
from message import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route(config.PATH, methods=['GET', 'POST'])
def callback():
    if not request.json or 'type' not in request.json:
        abort(400)

    if request.json['type'] == 'confirmation':
        return config.CONFIRMATION_TOKEN

    if request.json['type'] == 'wall_post_new':
        post = request.json['object']

        attachments = Slack(post=post).create_attachments()
        Slack.send_message(auth=slack, channel=config.CHANNEL,
            text=config.TEXT, attachments=attachments)

        return 'ok', 200


slack = auth_slack()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
