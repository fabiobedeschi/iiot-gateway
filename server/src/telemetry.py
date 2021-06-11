from json import dumps
from os import getenv

from paho.mqtt import publish


def _publish_single(payload, topic, hostname, port, qos, auth):
    return publish.single(
        topic=topic,
        payload=payload,
        hostname=hostname,
        port=port,
        qos=qos,
        auth=auth
    )


def _publish_single_tb(payload):
    return _publish_single(
        topic='v1/gateway/telemetry',
        payload=dumps(payload),
        hostname=getenv('THINGSBOARD_HOST'),
        port=int(getenv('THINGSBOARD_PORT')),
        qos=int(getenv('THINGSBOARD_QOS')),
        auth={'username': getenv('ACCESS_TOKEN')}
    )


def _publish_single_userservice(payload):
    return _publish_single(
        topic=getenv('USERSERVICE_TOPIC'),
        payload=dumps(payload),
        hostname=getenv('USERSERVICE_HOST'),
        port=int(getenv('USERSERVICE_PORT')),
        qos=int(getenv('USERSERVICE_QOS')),
        auth=None
    )


def format_user_payload_thingsboard(user):
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


def format_user_payload_userservice(user):
    return {
        "user": {
            "uuid": user["uuid"],
            "delta": user["delta"]
        }
    }


def push_user_telemetry(user, custom_payload=None):
    payload = custom_payload or format_user_payload_thingsboard(user)
    return _publish_single_tb(payload)


def push_user_update(user, custom_payload=None):
    payload = custom_payload or format_user_payload_userservice(user)
    return _publish_single_userservice(payload)


def format_waste_bin_payload_thingsboard(waste_bin):
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
    payload = custom_payload or format_waste_bin_payload_thingsboard(waste_bin)
    return _publish_single_tb(payload)
