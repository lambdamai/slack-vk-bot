import json

from auth import auth_vk

vk = auth_vk()


class User(object):
	def __init__(self, id):
		self.id = id
		self.user = vk.users.get(user_ids=self.id, fields='photo_50')[0]

	def get_info(self):
		author_name = self.user['first_name'] + ' ' + self.user['last_name']
		author_link = 'https://vk.com/id' + str(self.user['uid'])
		author_icon = self.user['photo_50']

		return author_name, author_link, author_icon


class Group(object):
	def __init__(self, id):
		self.id = id
		self.group = vk.groups.getById(group_id=self.id)[0]

	def get_info(self):
		author_name = self.group['name']
		author_link = 'https://vk.com/' + self.group['screen_name']
		author_icon = self.group['photo']

		return author_name, author_link, author_icon


def get_image(photo):
	try:
		image_url = photo['photo_1280']
	except KeyError:
		try:
			image_url = photo['photo_807']
		except KeyError:
			image_url = photo['photo_604']

	thumb_url = photo['photo_75']

	return image_url, thumb_url


def create_msg(post):
	try:
		if post['copy_history']:
			post = post['copy_history'][0]
			if post['owner_id'] < 0:
				id = str(post['owner_id'])[1:]
				author = Group(id=id)
				author_name, author_link, author_icon = author.get_info()
			else:
				author = User(id=post['owner_id'])
				author_name, author_link, author_icon = author.get_info()
	except KeyError:
		try:
			if post['created_by']:
				author = User(id=post['created_by'])
				author_name, author_link, author_icon = author.get_info()
		except KeyError:
			author_name, author_link, author_icon = None, None, None

	try:
		if post['attachments'] and post['attachments'][0]['type'] == 'photo':
			image_url, thumb_url = get_image(post['attachments'][0]['photo'])
	except KeyError:
		image_url, thumb_url = None, None

	text = post['text']
	ts = post['date']

	return json.dumps([{
		'fallback'   : '',
		'color'      : '#0093DA',
		'text'       : text,
		'ts'         : ts,
		'footer'     : 'Lambda ФРЭЛА | Лямбда',
		'footer_icon': 'http://lambda-it.ru/static/img/lambda_logo_mid.png',
		'image_url'  : image_url,
		'thumb_url'  : thumb_url,
		'author_name': author_name,
		'author_icon': author_icon,
		'author_link': author_link,
		'mrkdwn_in'  : ['text'],
	}]
	)
