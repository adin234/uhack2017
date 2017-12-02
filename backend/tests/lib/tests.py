# -*- coding: utf-8 -*-

from flask_testing import TestCase
from app import db
from app.lib.session_handling import _retrieve_member

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()

    def test_retrieve_member(self):
        # exists
        actual = _retrieve_member(user_pool_id='100001')
        self.assertEqual(1, len(actual))
        self.assertEqual(10001, actual[0][0])

        actual = _retrieve_member(anonymous_id='ap-northeast-1:faf0578f-14fb-4c74-a474-32825215db90')
        self.assertEqual(1, len(actual))
        self.assertEqual(10010, actual[0][0])

        # service_id will be used as preferred id
        actual = _retrieve_member(user_pool_id='100001',
                                  anonymous_id='ap-northeast-1:faf0578f-14fb-4c74-a474-32825215db90')
        self.assertEqual(1, len(actual))
        self.assertEqual(10001, actual[0][0])

        # empty string will be ignored
        actual = _retrieve_member(user_pool_id='', anonymous_id='ap-northeast-1:faf0578f-14fb-4c74-a474-32825215db90')
        self.assertEqual(1, len(actual))
        self.assertEqual(10010, actual[0][0])

        # not exists
        actual = _retrieve_member(user_pool_id='-10000')
        self.assertEqual(0, len(actual))

        actual = _retrieve_member()
        self.assertEqual(0, len(actual))
