from logging import getLogger
from os import getenv

from paho.mqtt.client import Client
from ujson import loads

from .database import Database

logger = getLogger()


class Subscriber(Client):

    def __init__(self, db=None):
        super().__init__()
        self.db = db or Database(keep_retrying=True)
        self.on_connect = self.sub_on_connect
        self.on_subscribe = self.sub_on_subscribe
        self.on_message = self.sub_on_message

    def sub_on_connect(self, client, userdata, flags, rc):
        logger.info('Successfully connected to mqtt broker.')
        client.subscribe(
            topic=getenv('GW_ZONE'),
            qos=int(getenv('USERSERVICE_QOS', 0))
        )

    def sub_on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info(f'Successfully subscribed to "{getenv("GW_ZONE")}" topic.')

    def sub_on_message(self, client, userdata, message):
        logger.info(f'Received message: {message}')
        payload = loads(message.payload)
        action, user = payload.get('action'), payload.get('user')

        response = None
        if 'create' == action:
            response = self.db.insert_user(
                uuid=user.get('uuid'),
                delta=user.get('delta')
            )
        elif 'update' == action:
            response = self.db.update_user(
                uuid=user.get('uuid'),
                delta=user.get('delta')
            )
        elif 'delete' == action:
            response = self.db.delete_user(
                uuid=user.get('uuid')
            )

        return response
