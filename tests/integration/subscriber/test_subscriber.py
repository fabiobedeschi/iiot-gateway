import unittest
from os import getenv
from time import sleep

from paho.mqtt import publish
from ujson import dumps

from subscriber.src.subscriber import Subscriber
from ..fixtures import Fixtures

TOPIC = 'dummy-topic'


class TestSubscriber(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = Fixtures()
        cls.subscriber = Subscriber(topic=TOPIC)
        cls.subscriber.connect(
            host=getenv('USERSERVICE_HOST'),
            port=int(getenv('USERSERVICE_PORT', 1883)),
            keepalive=int(getenv('USERSERVICE_KA', 60))
        )
        cls.subscriber.loop_start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.subscriber.loop_stop()
        cls.fixtures.clean_database()
        cls.fixtures.close_connection()

    def setUp(self) -> None:
        self.fixtures.clean_database()

    def test_create_user_on_message_successfully(self):
        user = {'uuid': 'c184584fa10e4809a96f24b4cc68c892', 'delta': 42}
        publish.single(
            topic=TOPIC, payload=dumps({'user': user, 'action': 'create'}),
            hostname=getenv('USERSERVICE_HOST'), port=int(getenv('USERSERVICE_PORT')), qos=1
        )
        sleep(0.5)

        saved_user = self.fixtures.find_user(user['uuid'])
        self.assertIsNotNone(saved_user)
        self.assertEqual(42, saved_user['delta'])

    def test_update_user_on_message_successfully(self):
        user = {'uuid': '16f39b703ffa41cb9af4d904b773efe2', 'delta': 42}
        self.fixtures.insert_user(user['uuid'], 0)
        publish.single(
            topic=TOPIC, payload=dumps({'user': user, 'action': 'update'}),
            hostname=getenv('USERSERVICE_HOST'), port=int(getenv('USERSERVICE_PORT')), qos=1
        )
        sleep(0.5)

        saved_user = self.fixtures.find_user(user['uuid'])
        self.assertIsNotNone(saved_user)
        self.assertEqual(42, saved_user['delta'])

    def test_delete_user_on_message_successfully(self):
        user = {'uuid': '575743bf68ee467688f2b692274b031e', 'delta': 42}
        self.fixtures.insert_user(user['uuid'], 42)
        publish.single(
            topic=TOPIC, payload=dumps({'user': user, 'action': 'delete'}),
            hostname=getenv('USERSERVICE_HOST'), port=int(getenv('USERSERVICE_PORT')), qos=1
        )
        sleep(0.5)

        saved_user = self.fixtures.find_user(user['uuid'])
        self.assertIsNone(saved_user)


if __name__ == '__main__':
    unittest.main()
