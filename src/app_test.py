import unittest
from unittest import mock
import app


class MyTestCase(unittest.TestCase):

    def test_On_get_user_details_Should_return_422_When_user_name_is_not_provided(self):
        m = mock.MagicMock()
        m.json = {}
        with mock.patch("app.request", m):
            result = app.get_user_details()
            self.assertEqual(result.status_code, 422)

    def test_On_get_user_details_Should_return_422_When_user_name_is_empty_string(self):
        m = mock.MagicMock()
        m.json = {"user_name": ""}
        with mock.patch("app.request", m):
            result = app.get_user_details()
            self.assertEqual(result.status_code, 422)

    def test_On_get_user_details_Should_return_422_When_user_name_is_blank_string(self):
        m = mock.MagicMock()
        m.json = {"user_name": "     "}
        with mock.patch("app.request", m):
            result = app.get_user_details()
            self.assertEqual(result.status_code, 422)


if __name__ == '__main__':
    unittest.main()
