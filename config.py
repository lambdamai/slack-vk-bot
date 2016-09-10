import os

try:
	confirmation_token = os.environ.get('CONFIRMATION_TOKEN')
	bot_secret = os.environ.get('SLACK_BOT_SECRET')
	channel = os.environ.get('CHANNEL')
	text = os.environ.get('TEXT')
except KeyError:
	print('no eniromental variables detected\nmake sure to set them')
