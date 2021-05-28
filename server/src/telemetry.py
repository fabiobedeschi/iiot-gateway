from json import dumps
from os import getenv

from paho.mqtt import publish


def _publish_single(payload):
    return publish.single(
        topic='v1/gateway/telemetry',
        payload=dumps(payload),
        hostname=getenv('THINGSBOARD_HOST'),
        port=int(getenv('THINGSBOARD_PORT')),
        qos=int(getenv('THINGSBOARD_QOS')),
        auth={'username': getenv('ACCESS_TOKEN')}
    )


def format_user_payload(user):
    return {
        f"user_{user.get('uuid')}": [
            {
                'ts': user.get('updated_at').timestamp() * 1000,
                'values': {
                    'delta': user.get('delta')
                }
            }
        ]
    }


def push_user_telemetry(user, custom_payload=None):
    payload = custom_payload or format_user_payload(user)
    return _publish_single(payload)


def format_waste_bin_payload(waste_bin):
    return {
        f"wb_{waste_bin.get('uuid')}": [
            {
                'ts': waste_bin.get('updated_at').timestamp() * 1000,
                'values': {
                    'fill_level': waste_bin.get('fill_level')
                }
            }
        ]
    }


def push_waste_bin_telemetry(waste_bin, custom_payload=None):
    payload = custom_payload or format_waste_bin_payload(waste_bin)
    return _publish_single(payload)
