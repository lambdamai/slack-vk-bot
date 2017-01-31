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
        try:
            if self.repost:
                return json.dumps([{
                    'fallback':    '',
                    'color':       self.post.color,
                    'text':        self.post.text,
                    'ts':          self.post.ts,
                    'footer':      self.post.footer,
                    'footer_icon': self.post.footer_icon,
                    'image_url':   self.post.image_url,
                    'thumb_url':   self.post.thumb_url,
                }, {
                    'fallback':    '',
                    'color':       self.repost.color,
                    'text':        self.repost.text,
                    'ts':          self.repost.ts,
                    'footer':      self.repost.footer,
                    'footer_icon': self.repost.footer_icon,
                    'image_url':   self.repost.image_url,
                    'thumb_url':   self.repost.thumb_url,
                }])
        except AttributeError:
            return json.dumps([{
                'fallback':    '',
                'color':       self.post.color,
                'text':        self.post.text,
                'ts':          self.post.ts,
                'footer':      self.post.footer,
                'footer_icon': self.post.footer_icon,
                'image_url':   self.post.image_url,
                'thumb_url':   self.post.thumb_url,
                'mrkdwn_in':   ['text'],
            }])

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
        # try:
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
