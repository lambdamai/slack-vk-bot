from slacker import Slacker
from config import bot_secret_
from vk import Session, API


def auth_slack():
	api = Slacker(bot_secret_)

	try:
		api.auth.test()
	except Exception as e:
		print('not authed\n', e)

	return api


def auth_vk():
	session = Session()
	api = API(session)

	return api
