from slacker import Slacker
import os


def auth_slack():

	bot_secret = os.environ.get('SLACK_BOT_SECRET')

	api = Slacker(bot_secret)

	try:
		api.auth.test()
	except:
		print('auth is not successful')

	return api
