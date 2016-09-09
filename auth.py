from slacker import Slacker
import vk


def auth_slack():
	try:
		with open('slack.key', 'r') as api_key:
			bot_secret = api_key.readline()
	except FileNotFoundError or UnicodeError:
		print('Put bot_secret in slack.key file')

	api = Slacker(bot_secret)

	try:
		api.auth.test()
	except:
		print('auth is not successful')

	return api


def auth_vk():
	try:
		with open('vk.key', 'r') as api_key:
			app_id = api_key.readline()
			app_secret = api_key.readline()
	except FileNotFoundError or UnicodeError:
		print('Put app_id and app_secret in vk.key file')

	session = vk.AuthSession(app_id=app_id)
	api = vk.API(session=session)

	return api
