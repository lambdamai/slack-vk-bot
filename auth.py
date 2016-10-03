from slacker import Slacker
from config import bot_secret_, page_id_, access_token_
from vk import Session, API
import facebook


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


def auth_facebook(cfg):
	graph = facebook.GraphAPI(cfg['access_token'])
	resp = graph.get_object('lambdafrela')
	page_access_token = None

	try:
		if resp['id'] == cfg['page_id']:
			page_access_token = cfg['access_token']
	except KeyError:
		print('not authed fb')

	graph = facebook.GraphAPI(page_access_token)

	return graph
