import json

from auth import auth_vk

vk = auth_vk()


def get_group(id):
	return vk.groups.getById(group_id=id)[0]


def get_user(id):
	return vk.users.get(user_ids=id, fields='photo_50')[0]


def get_group_info(author):
	author_name = author['name']
	author_link = 'https://vk.com/' + author['screen_name']
	author_icon = author['photo']

	return author_icon, author_link, author_name


def get_user_info(author):
	author_name = author['first_name'] + ' ' + author['last_name']
	author_link = 'https://vk.com/id' + str(author['uid'])
	author_icon = author['photo_50']

	return author_icon, author_link, author_name


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
				author = get_group(str(post['owner_id'])[1:])
				author_icon, author_link, author_name = get_group_info(author)
			else:
				author = get_user(str(post['owner_id']))
				author_icon, author_link, author_name = get_user_info(author)
	except KeyError:
		try:
			if post['created_by']:
				author = get_user(str(post['created_by']))
				author_icon, author_link, author_name = get_user_info(author)
		except KeyError:
			author_icon, author_link, author_name = None, None, None

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
