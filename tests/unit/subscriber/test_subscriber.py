import unittest
import unittest.mock

from paho.mqtt.client import MQTTMessage
from ujson import dumps

from subscriber.src.database import Database
from subscriber.src.subscriber import Subscriber


class TestSubscriber(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = unittest.mock.create_autospec(Database)
        cls.subscriber = Subscriber(db=cls.db)

    def test_on_message_create(self):
        self.db.insert_user.return_value = user = {
            'uuid': 'f51b3db90173408480d5f6c16a5652d0',
            'delta': 42
        }
        message = MQTTMessage()
        message.payload = dumps({'user': user, 'action': 'create'}).encode()

        result = self.subscriber.on_message(
            client=self.subscriber,
            userdata=None,
            message=message
        )

        self.db.insert_user.assert_called_with(uuid=user.get('uuid'), delta=user.get('delta'))
        self.assertEqual(user, result)

    def test_on_message_update(self):
        self.db.update_user.return_value = user = {
            'uuid': 'f51b3db90173408480d5f6c16a5652d0',
            'delta': 42
        }
        message = MQTTMessage()
        message.payload = dumps({'user': user, 'action': 'update'}).encode()

        result = self.subscriber.on_message(
            client=self.subscriber,
            userdata=None,
            message=message
        )

        self.db.update_user.assert_called_with(uuid=user.get('uuid'), delta=user.get('delta'))
        self.assertEqual(user, result)

    def test_on_message_delete(self):
        self.db.delete_user.return_value = user = {
            'uuid': 'f51b3db90173408480d5f6c16a5652d0'
        }
        message = MQTTMessage()
        message.payload = dumps({'user': user, 'action': 'delete'}).encode()

        result = self.subscriber.on_message(
            client=self.subscriber,
            userdata=None,
            message=message
        )

        self.db.delete_user.assert_called_with(uuid=user.get('uuid'))
        self.assertEqual(user, result)


if __name__ == '__main__':
    unittest.main()
