from slacker import Slacker
from vk import Session, API
from config import BOT_SECRET


def auth_slack():
	api = Slacker(BOT_SECRET)

	try:
		api.auth.test()
	except Exception as e:
		print('slack not authed\n', e)

	return api


def auth_vk():
	try:
		session = Session()
		api = API(session)
	except Exception as e:
		print('vk not authed\n', e)

	return api
