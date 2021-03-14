from json import dumps
from os import getenv

from paho.mqtt import publish


class Telemetry:
    def _publish_single(self, payload):
        publish.single(
            topic='v1/gateway/telemetry',
            payload=dumps(payload),
            hostname=getenv('THINGSBOARD_HOST'),
            port=int(getenv('MOSQUITTO_PORT')),
            qos=int(getenv('MOSQUITTO_QOS')),
            auth={'username': getenv('ACCESS_TOKEN')}
        )

    def push_user_telemetry(self, user):
        payload = {
            f"user_{user.get('uuid')}": [
                {
                    'ts': user.get('updated_at').timestamp() * 1000,
                    'values': {
                        'delta': user.get('delta')
                    }
                }
            ]
        }
        self._publish_single(payload)

    def push_waste_bin_telemetry(self, waste_bin):
        payload = {
            f"wb_{waste_bin.get('uuid')}": [
                {
                    'ts': waste_bin.get('updated_at').timestamp() * 1000,
                    'values': {
                        'fill_level': waste_bin.get('fill_level')
                    }
                }
            ]
        }
        self._publish_single(payload)
