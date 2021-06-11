import unittest
from os import environ

from server.app import app
from ..fixtures import Fixtures


class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True
        environ['DISABLE_TELEMETRY'] = 'true'
        cls.client = app.test_client()
        cls.fixtures = Fixtures()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fixtures.clean_database()
        cls.fixtures.close_connection()

    def setUp(self) -> None:
        self.fixtures.clean_database()

    def test_patch_user_successfully(self):
        uuid = 'f9b358cc522a4cb7a60c27da6fbed8f1'
        self.fixtures.insert_user(uuid, 0)

        response = self.client.patch(f'/users/{uuid}', json={'delta': 42})
        user = self.fixtures.find_user(uuid)

        self.assertEqual(200, response.status_code)
        self.assertEqual(uuid, response.json['uuid'])
        self.assertEqual(42, response.json['delta'])
        self.assertEqual(42, user['delta'])

    def test_patch_user_increment_one_by_default(self):
        uuid = 'f9b358cc522a4cb7a60c27da6fbed8f1'
        self.fixtures.insert_user(uuid, 0)

        response = self.client.patch(f'/users/{uuid}')
        user = self.fixtures.find_user(uuid)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, user['delta'])

    def test_patch_user_fail_if_user_does_not_exists(self):
        uuid = 'f9b358cc522a4cb7a60c27da6fbed8f1'
        ne_uuid = 'nonexistent-user-uuid'
        self.fixtures.insert_user(uuid, 0)

        response = self.client.patch(f'/users/{ne_uuid}', json={'delta': 42})
        user = self.fixtures.find_user(uuid)

        self.assertEqual(404, response.status_code)
        self.assertEqual(0, user['delta'])

    def test_patch_waste_bin_successfully(self):
        uuid = '579f44cfed4c4793a28e79f56c8f1aba'
        self.fixtures.insert_waste_bin(uuid, 0)

        response = self.client.patch(f'/waste_bins/{uuid}', json={'fill_level': 42})
        waste_bin = self.fixtures.find_waste_bin(uuid)

        self.assertEqual(200, response.status_code)
        self.assertEqual(uuid, response.json['uuid'])
        self.assertEqual(42, response.json['fill_level'])
        self.assertEqual(42, waste_bin['fill_level'])

    def test_patch_waste_bin_fail_if_data_is_missing(self):
        uuid = '579f44cfed4c4793a28e79f56c8f1aba'
        self.fixtures.insert_waste_bin(uuid, 0)

        response = self.client.patch(f'/waste_bins/{uuid}')
        waste_bin = self.fixtures.find_waste_bin(uuid)

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, waste_bin['fill_level'])

    def test_patch_waste_bin_fail_if_waste_bin_does_not_exists(self):
        uuid = '579f44cfed4c4793a28e79f56c8f1aba'
        ne_uuid = 'nonexistent-waste-bin-uuid'
        self.fixtures.insert_waste_bin(uuid, 0)

        response = self.client.patch(f'/waste_bins/{ne_uuid}', json={'fill_level': 42})
        waste_bin = self.fixtures.find_waste_bin(uuid)

        self.assertEqual(404, response.status_code)
        self.assertEqual(0, waste_bin['fill_level'])


if __name__ == '__main__':
    unittest.main()
