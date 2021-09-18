"""webapp/tests/tests.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/18
python version  : 3.7.3
"""
import unittest

from app import app


class AppTestCase(unittest.TestCase):
    """AppTestCase
    """

    def test_root_text(self):
        """test_root_text
        """
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.data, b'Hello world!')


if __name__ == '__main__':
    unittest.main()
