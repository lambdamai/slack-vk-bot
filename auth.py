from slacker import Slacker
from config import bot_secret


def auth_slack():
	api = Slacker(bot_secret)

	try:
		api.auth.test()
	except Exception as e:
		print('not authed\n', e)

	return api
