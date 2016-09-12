import json

from auth import auth_vk

vk = auth_vk()


def get_group_info(post):
	author = vk.groups.getById(group_id=str(post['owner_id'])[1:])[0]
	author_name = author['name']
	author_link = 'https://vk.com/' + author['screen_name']
	author_icon = author['photo']

	return author_icon, author_link, author_name


def get_user_info(post):
	author = vk.users.get(user_ids=str(post['owner_id']), fields='photo_50')[0]
	author_name = author['first_name'] + ' ' + author['last_name']
	author_link = 'https://vk.com/id' + str(author['uid'])
	author_icon = author['photo_50']

	return author_icon, author_link, author_name


def create_msg(post):
	try:
		if post['copy_history']:
			post = post['copy_history'][0]
			if str(post['owner_id'])[0] == '-':
				author_icon, author_link, author_name = get_group_info(post)
			else:
				author_icon, author_link, author_name = get_user_info(post)
	except KeyError:
		author_icon, author_link, author_name = None, None, None

	try:
		if post['attachments'] and post['attachments'][0]['type'] == 'photo':
			photo = post['attachments'][0]
			image_url = photo['photo']['photo_1280']
			thumb_url = photo['photo']['photo_130']
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
