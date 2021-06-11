import unittest
from datetime import datetime

from server.src.telemetry import *


class TestTelemetry(unittest.TestCase):

    def test_format_user_payload_successfully(self):
        user = {
            'uuid': '8ca208ced569457cb7d93acb95d8cc45',
            'delta': 10,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        expected_result = {
            f"user_{user.get('uuid')}": [
                {
                    'ts': user.get('updated_at').timestamp() * 1000,
                    'values': {
                        'delta': user.get('delta')
                    }
                }
            ]
        }
        result = format_user_payload_thingsboard(user)
        self.assertEqual(expected_result, result)

    def test_format_waste_bin_payload_successfully(self):
        waste_bin = {
            'uuid': '8ca208ced569457cb7d93acb95d8cc45',
            'fill_level': 10,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        expected_result = {
            f"wb_{waste_bin.get('uuid')}": [
                {
                    'ts': waste_bin.get('updated_at').timestamp() * 1000,
                    'values': {
                        'fill_level': waste_bin.get('fill_level')
                    }
                }
            ]
        }
        result = format_waste_bin_payload_thingsboard(waste_bin)
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
