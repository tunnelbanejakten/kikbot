from flask import request, Response
from kik.messages import messages_from_json, TextMessage

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
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])
            event = 'new_message'
            r = requests.post(
                'https://maker.ifttt.com/trigger/%s/with/key/m_IqDwoDWohGS_orXbk7y-S_wZEZaXWM7jQp8l4x5-x' % event,
                data={
                    'value1': message.from_user,
                    'value2': message.body
                })
            print "IFTTT Response Code: %s" % r.status_code

    return Response(status=200)
