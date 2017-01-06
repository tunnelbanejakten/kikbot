# coding=utf-8
from flask import request, Response
from kik.messages import PictureMessage
from kik.messages import messages_from_json, TextMessage
from kik.messages.start_chatting import StartChattingMessage
from kik.messages.video import VideoMessage

from app import application
from app import kik
import requests


@application.route('/')
def index():
    return "Hej"


@application.before_request
def log_request_info():
    print('Headers: %s', request.headers)
    print('Body: %s', request.get_data())
    application.logger.info('Headers: %s', request.headers)
    application.logger.info('Body: %s', request.get_data())


@application.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, StartChattingMessage):
            reply_to_kik_message(message=message,
                                 response='Hej! Här kan du skicka era svar och bilder till Tunnelbanejakten. '
                                          'Vilken patrull är du med i?')
            trigger_ifttt_event(event='first_message',
                                sender=message.from_user)
        elif isinstance(message, TextMessage):
            reply_to_kik_message(message=message,
                                 response='Tack för ditt svar.')
            trigger_ifttt_event(event='new_message',
                                message=message.body,
                                sender=message.from_user)
        elif isinstance(message, PictureMessage):
            reply_to_kik_message(message=message,
                                 response='Tack för din bild.')
            trigger_ifttt_event(event='new_photo',
                                message=message.pic_url,
                                sender=message.from_user)
        elif isinstance(message, VideoMessage):
            reply_to_kik_message(message=message,
                                 response='Hmm, tyvärr kan du inte skicka videoklipp till oss. '
                                          'Kan du skicka en bild istället?')

    return Response(status=200)


def reply_to_kik_message(message, response):
    kik.send_messages([
        TextMessage(
            to=message.from_user,
            chat_id=message.chat_id,
            body=response
        )
    ])


def trigger_ifttt_event(event, message=None, sender=None):
    r = requests.post(
        'https://maker.ifttt.com/trigger/%s/with/key/m_IqDwoDWohGS_orXbk7y-S_wZEZaXWM7jQp8l4x5-x' % event,
        data={
            'value1': sender,
            'value2': message
        })
    print "IFTTT Response Code: %s" % r.status_code
