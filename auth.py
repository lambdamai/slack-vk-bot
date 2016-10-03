from slacker import Slacker
from config import bot_secret_
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
	resp = graph.get_object('me/accounts')
	page_access_token = None

	for page in resp['data']:
		if page['id'] == cfg['page_id']:
			page_access_token = page['access_token']

	graph = facebook.GraphAPI(page_access_token)

	return graph
