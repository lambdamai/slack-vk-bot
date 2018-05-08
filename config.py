import os
import configparser

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

try:
    config.read(config_file)
except configparser.ParsingError as e:
    print(e)

CONFIRMATION_TOKEN = config['VK']['CONFIRMATION_TOKEN']
BOT_SECRET = config['SLACK']['SLACK_BOT_SECRET']
CHANNEL = config['SLACK']['CHANNEL']
TEXT = config['SLACK']['TEXT']
PATH = config['SERVER']['PATH']