from logging import getLogger
from os import getenv
from typing import Optional

from paho.mqtt.client import Client
from ujson import loads

from src.database import Database

db: Optional[Database] = None
mqtt_client: Optional[Client] = None
logger = getLogger()


def on_connect(client, userdata, flags, rc):
    logger.info('Successfully connected to mqtt broker')

    global db
    db = Database()

    client.subscribe(
        topic=getenv('GW_ZONE'),
        qos=int(getenv('USERSERVICE_QOS', 0))
    )


def on_subscribe(client, userdata, mid, granted_qos):
    logger.info(f'Successfully subscribed to "{getenv("GW_ZONE")}" topic')


def on_message(client, userdata, message):
    logger.info(f'Received message: {message}')
    payload = loads(message.payload)
    action, user = payload.get('action'), payload.get('user')

    if 'create' == action:
        db.insert_user(
            uuid=user.get('uuid'),
            delta=user.get('delta')
        )
    elif 'update' == action:
        db.update_user(
            uuid=user.get('uuid'),
            delta=user.get('delta')
        )
    elif 'delete' == action:
        db.delete_user(
            uuid=user.get('uuid')
        )


if __name__ == '__main__':
    mqtt_client = Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message

    mqtt_client.connect(
        host=getenv('USERSERVICE_HOST'),
        port=int(getenv('USERSERVICE_PORT', 1883)),
        keepalive=int(getenv('USERSERVICE_KA', 60))
    )
    mqtt_client.loop_forever()
