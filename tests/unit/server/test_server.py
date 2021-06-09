import unittest
import unittest.mock

from server.src.database import Database
from server.src.server import GatewayServer


class TestGatewayServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = unittest.mock.create_autospec(Database)
        cls.server = GatewayServer(db=cls.db, telemetry=False)

    def test_find_all_users_successfully(self):
        self.db.find_all_users.return_value = expected_result = [
            {'uuid': '668e2987956a4943a9e6a2c77e56dc17'},
            {'uuid': '86c822ee6f9a4f69b2f57a9c8702e4a2'},
            {'uuid': '94565bc0210546f6990bce590d94be39'}
        ]
        result, code = self.server.find_all_users()

        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_find_user_successfully(self):
        self.db.find_user.return_value = expected_result = {
            'uuid': '668e2987956a4943a9e6a2c77e56dc17'
        }
        result, code = self.server.find_user(uuid='668e2987956a4943a9e6a2c77e56dc17')

        self.db.find_user.assert_called_with(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_find_user_not_exists(self):
        self.db.find_user.return_value = expected_result = None
        result, code = self.server.find_user(uuid='668e2987956a4943a9e6a2c77e56dc17')

        self.db.find_user.assert_called_with(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.assertEqual(expected_result, result)
        self.assertEqual(404, code)

    def test_update_user_successfully(self):
        self.db.update_user.return_value = expected_result = {
            'uuid': '668e2987956a4943a9e6a2c77e56dc17',
            'delta': 1200
        }
        result, code = self.server.update_user(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'delta': 100}
        )

        self.db.update_user.assert_called_with(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            delta=100
        )
        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_update_user_not_exists(self):
        self.db.update_user.return_value = expected_result = None
        result, code = self.server.update_user(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'delta': 100}
        )

        self.db.update_user.assert_called_with(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            delta=100
        )
        self.assertEqual(expected_result, result)
        self.assertEqual(404, code)

    def test_update_user_malformed_data(self):
        self.skipTest('Not used anymore.')

        self.db.update_user.return_value = expected_result = None
        result, code = self.server.update_user(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'malformed_data': 123456789}
        )

        self.db.update_user.assert_not_called()
        self.assertEqual(expected_result, result)
        self.assertEqual(400, code)

    def test_reset_user_delta(self):
        self.db.reset_user_delta.return_value = expected_result = {
            'uuid': '668e2987956a4943a9e6a2c77e56dc17',
            'delta': 0
        }
        result, code = self.server.reset_user(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.db.reset_user_delta.assert_called_with(
            uuid='668e2987956a4943a9e6a2c77e56dc17'
        )
        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_reset_user_not_exists(self):
        self.db.reset_user_delta.return_value = expected_result = None
        result, code = self.server.reset_user(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.db.reset_user_delta.assert_called_with(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.assertEqual(expected_result, result)
        self.assertEqual(404, code)

    def test_find_all_waste_bins_successfully(self):
        self.db.find_all_waste_bins.return_value = expected_result = [
            {'uuid': '668e2987956a4943a9e6a2c77e56dc17'},
            {'uuid': '86c822ee6f9a4f69b2f57a9c8702e4a2'},
            {'uuid': '94565bc0210546f6990bce590d94be39'}
        ]
        result, code = self.server.find_all_waste_bins()

        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_find_waste_bin_successfully(self):
        self.db.find_waste_bin.return_value = expected_result = {
            'uuid': '668e2987956a4943a9e6a2c77e56dc17'
        }
        result, code = self.server.find_waste_bin(uuid='668e2987956a4943a9e6a2c77e56dc17')

        self.db.find_waste_bin.assert_called_with(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_find_waste_bin_not_exists(self):
        self.db.find_waste_bin.return_value = expected_result = None
        result, code = self.server.find_waste_bin(uuid='668e2987956a4943a9e6a2c77e56dc17')

        self.db.find_waste_bin.assert_called_with(uuid='668e2987956a4943a9e6a2c77e56dc17')
        self.assertEqual(expected_result, result)
        self.assertEqual(404, code)

    def test_update_waste_bin_successfully(self):
        self.db.update_waste_bin.return_value = expected_result = {
            'uuid': '668e2987956a4943a9e6a2c77e56dc17',
            'fill_level': 50
        }
        result, code = self.server.update_waste_bin(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'fill_level': 50}
        )

        self.db.update_waste_bin.assert_called_with(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            fill_level=50
        )
        self.assertEqual(expected_result, result)
        self.assertEqual(200, code)

    def test_update_waste_bin_not_exists(self):
        self.db.update_waste_bin.return_value = expected_result = None
        result, code = self.server.update_waste_bin(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'fill_level': 50}
        )

        self.db.update_waste_bin.assert_called_with(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            fill_level=50
        )
        self.assertEqual(expected_result, result)
        self.assertEqual(404, code)

    def test_update_waste_bin_malformed_data(self):
        self.db.update_waste_bin.return_value = expected_result = None
        result, code = self.server.update_waste_bin(
            uuid='668e2987956a4943a9e6a2c77e56dc17',
            data={'malformed_data': 123456789}
        )

        self.db.update_waste_bin.assert_not_called()
        self.assertEqual(expected_result, result)
        self.assertEqual(400, code)


if __name__ == '__main__':
    unittest.main()
