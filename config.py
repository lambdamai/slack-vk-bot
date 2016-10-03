import os

try:
	confirmation_token_ = os.environ.get('CONFIRMATION_TOKEN')
	bot_secret_ = os.environ.get('SLACK_BOT_SECRET')
	channel_ = os.environ.get('CHANNEL')
	text_ = os.environ.get('TEXT')
	page_id_ = os.environ.get('PAGE_ID')
	access_token_ = os.environ.get('ACCESS_TOKEN')
except KeyError:
	print('no eniromental variables detected\nmake sure to set them')
