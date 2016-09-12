import os

try:
	confirmation_token_ = os.environ.get('CONFIRMATION_TOKEN')
	bot_secret_ = os.environ.get('SLACK_BOT_SECRET')
	channel_ = os.environ.get('CHANNEL')
	text_ = os.environ.get('TEXT')
except KeyError:
	print('no eniromental variables detected\nmake sure to set them')
