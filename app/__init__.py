import os

from flask import Flask
from kik import KikApi, Configuration

application = Flask(__name__)

bot_username = os.environ.get('KIK_BOT_USERNAME')
bot_api_key = os.environ.get('KIK_BOT_APIKEY')

kik = KikApi(bot_username, bot_api_key)

kik.set_configuration(
    Configuration(
        webhook='https://helloworld-kikbot.herokuapp.com/incoming'
    )
)

from app import views
