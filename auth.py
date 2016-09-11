from slacker import Slacker
from config import bot_secret
from vk import Session, API


def auth_slack():
	api = Slacker(bot_secret)

	try:
		api.auth.test()
	except Exception as e:
		print('not authed\n', e)

	return api


def auth_vk():
	session = Session()
	api = API(session)

	return api