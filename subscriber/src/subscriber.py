from logging import getLogger
from os import getenv
import requests

from paho.mqtt.client import Client
from ujson import loads

from .database import Database

logger = getLogger()


class Subscriber(Client):

    def __init__(self, db=None, topic=None):
        super().__init__()
        self.db = db or Database(keep_retrying=True)
        self.topic = topic
        self.on_connect = self.sub_on_connect
        self.on_subscribe = self.sub_on_subscribe
        self.on_message = self.sub_on_message

    def sub_on_connect(self, client, userdata, flags, rc):
        logger.info('Successfully connected to mqtt broker.')
        client.subscribe(
            topic=self.topic or getenv('GW_ZONE'),
            qos=int(getenv('USERSERVICE_QOS', 0))
        )
        self.obtain_all_users_in_zone()

    def obtain_all_users_in_zone(self):
        response = requests.get(
            url=f"http://{getenv('USERSERVICE_HOST')}:{getenv('USERSERVICE_HTTP_PORT', '80')}/users",
            params={'area': getenv('GW_ZONE')}
        )
        for user in response.json():
            self.db.insert_user(uuid=user['uuid'])

    def sub_on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info(f'Successfully subscribed to "{self.topic or getenv("GW_ZONE")}" topic.')

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
