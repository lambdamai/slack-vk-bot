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


class Slack(object):
	def __init__(self, post):
		try:
			if post['copy_history']:
				self.get_repost_info(post=post['copy_history'][0])
		except KeyError:
			try:
				if post['created_by']:
					self.get_post_info(post=post)
			except KeyError:
				self.author_name, self.author_link, self.author_icon = \
					None, None, None
		try:
			if post['attachments'] and post['attachments'][0]['type'] == 'photo':
				image = post['attachments'][0]['photo']
				self.image_url, self.thumb_url = get_image(image)
		except KeyError:
			self.image_url, self.thumb_url = None, None

		self.text = post['text']
		self.ts = post['date']
		self.color = '#0093DA'
		self.footer = 'Lambda ФРЭЛА | Лямбда'
		self.footer_icon = 'http://lambda-it.ru/static/img/lambda_logo_mid.png'

	def get_repost_info(self, post):
		if post['owner_id'] < 0:
			author = Group(id=str(post['owner_id'])[1:])
			self.author_name, self.author_link, self.author_icon = \
				author.get_info()
		else:
			author = User(id=post['owner_id'])
			self.author_name, self.author_link, self.author_icon = \
				author.get_info()

	def get_post_info(self, post):
		author = User(id=post['created_by'])
		self.author_name, self.author_link, self.author_icon = \
			author.get_info()

	def create_message(self):
		return json.dumps([{
			'fallback'   : '',
			'color'      : self.color,
			'text'       : self.text,
			'ts'         : self.ts,
			'footer'     : self.footer,
			'footer_icon': self.footer_icon,
			'image_url'  : self.image_url,
			'thumb_url'  : self.thumb_url,
			'author_name': self.author_name,
			'author_icon': self.author_icon,
			'author_link': self.author_link,
			'mrkdwn_in'  : ['text'],
		}]
		)

	@staticmethod
	def send_message(auth, channel, text, attachments=None, as_user=True):
		auth.chat.post_message(channel=channel,
		                       text=text,
		                       attachments=attachments,
		                       as_user=as_user)


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

