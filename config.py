import os
import configparser

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

try:
    config.read(config_file)
except configparser.ParsingError as e:
    print(e)

confirmation_token_ = config['VK']['CONFIRMATION_TOKEN']
bot_secret_ = config['SLACK']['SLACK_BOT_SECRET']
channel_ = config['SLACK']['CHANNEL']
text_ = config['SLACK']['TEXT']
path_ = config['SERVER']['PATH']