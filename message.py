import json

from auth import auth_vk

vk = auth_vk()


class User(object):
    def __init__(self, id):
        self.id = id
        self.user = vk.users.get(user_ids=self.id, fields='photo_50')[0]

    def footer(self):
        footer = self.user['first_name'] + ' ' + self.user['last_name']
        footer_icon = self.user['photo_50']
        return footer, footer_icon


class Group(object):
    def __init__(self, id):
        self.id = id
        self.group = vk.groups.getById(group_id=self.id)[0]

    def footer(self):
        footer = self.group['name']
        footer_icon = self.group['photo']

        return footer, footer_icon


class Slack(object):
    def __init__(self, post):
        try:
            if post['copy_history']:
                self.repost = Repost(post['copy_history'][0])
                self.post = Post(post)
        except KeyError:
            self.post = Post(post, attachments=True)

    def create_attachments(self):
        data_to_send = Post.post_data_prepare(self.post)
        try:
            if self.repost:
                data_repost_to_send = Post.post_data_prepare(self.repost)
                return json.dumps([data_to_send, data_repost_to_send])
        except AttributeError:
            data_to_send['mrkdwn_in'] = ['text']
        return json.dumps([data_to_send])

    @staticmethod
    def send_message(auth, channel, text, attachments=None, as_user=True):
        auth.chat.post_message(channel=channel,
                               text=text,
                               attachments=attachments,
                               as_user=as_user)


class Post(object):
    def __init__(self, post, attachments=None):
        self.text = post['text']
        self.ts = post['date']
        self.color = '#0093DA'
        self.footer = 'Lambda ФРЭЛА | Лямбда'
        self.footer_icon = 'http://lambda-it.ru/static/img/lambda_logo_mid.png'
        if attachments:
            try:
                if post['attachments']:
                    self.image_url, self.thumb_url = self.get_image(
                        post['attachments'])
            except KeyError:
                self.image_url, self.thumb_url = None, None
        else:
            self.image_url, self.thumb_url = None, None

    @staticmethod
    def get_image(attachments):
        for attachment in attachments:
            if attachment['type'] == 'photo':
                image = attachment['photo']
                try:
                    image_url = image['photo_1280']
                except KeyError:
                    try:
                        image_url = image['photo_807']
                    except KeyError:
                        image_url = image['photo_604']
                thumb_url = image['photo_75']
                return image_url, thumb_url
            else:
                return None, None
    
    @staticmethod
    def post_data_prepare(post):
        return {
            'fallback':    '',
            'color':       post.color,
            'text':        post.text,
            'ts':          post.ts,
            'footer':      post.footer,
            'footer_icon': post.footer_icon,
            'image_url':   post.image_url,
            'thumb_url':   post.thumb_url,
        }


class Repost(Post):
    def __init__(self, repost):
        Post.__init__(self, post=repost)
        self.text = repost['text']
        self.ts = repost['date']
        self.color = '#2393DA'
        self.footer, self.footer_icon = self.get_footer(repost)
        try:
            if repost['attachments']:
                self.image_url, self.thumb_url = self.get_image(
                    repost['attachments'])
        except KeyError:
            self.image_url, self.thumb_url = None, None

    @staticmethod
    def get_footer(post):
        if post['owner_id'] < 0:
            author = Group(id=str(post['owner_id'])[1:])
            footer, footer_icon = author.footer()
            return footer, footer_icon
        else:
            author = User(id=post['owner_id'])
            footer, footer_icon = author.footer()
            return footer, footer_icon
