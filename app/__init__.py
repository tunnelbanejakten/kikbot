import os

from flask import Flask
from kik import KikApi, Configuration

application = Flask(__name__)

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    application.logger.addHandler(stream_handler)
    application.logger.setLevel(logging.DEBUG)

bot_username = os.environ.get('KIK_BOT_USERNAME')
bot_api_key = os.environ.get('KIK_BOT_APIKEY')
host_name = os.environ.get('APP_HOST_NAME')

kik = KikApi(bot_username, bot_api_key)

kik.set_configuration(
    Configuration(
        webhook=('https://%s/incoming' % host_name)
    )
)

from app import views
