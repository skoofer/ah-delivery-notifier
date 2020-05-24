import json
from unittest import TestCase, mock
from ah_delivery_notifier.ah_delivery_notifier import notify_available_slots


class AHDeliveryNotifier(TestCase):
    @mock.patch('ah_delivery_notifier.ah_delivery_notifier.send_email')
    @mock.patch('ah_delivery_notifier.ah_delivery_notifier.get_ah_data')
    def test_integration_with_availability(self, get_ah_data_mock, send_email_mock):
        email_address = 'test@test.com'
        post_code = '1000XX'
        date_start = '2020-05-24'
        date_end = '2020-05-27'

        with open('resources/test_with_availability.json') as f:
            ah_mock_data = json.load(f)

        get_ah_data_mock.return_value = ah_mock_data

        expected_email_data = {
            'to': 'test@test.com',
            'subject': 'New available Spots for 1000XX for AH Bezorgservice!',
            'body': '''Hi,

There are new openings for you on AH Bezorgservice:
2020-05-24: between 07:00 and 08:00 for 6.95 EUR
2020-05-24: between 08:00 and 10:00 for 7.95 EUR
2020-05-27: between 14:00 and 21:00 for 2.95 EUR

Good luck!'''
        }

        notify_available_slots(email_address, post_code, date_start, date_end)

        send_email_mock.assert_called_with(expected_email_data)
