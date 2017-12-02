# -*- coding: utf-8 -*-
#
import json

from flask_testing import TestCase
from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def test_get_instructions(self):
        resp = self.client.get('/api/instructions?date=2016-12-12T00:00:00Z', headers={'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        actual = resp_body['data']
        self.assertEquals(1, len(actual))
        self.assertEquals(10002, actual[0]['meal_id'])

        # This is the instruction for the next day
        resp = self.client.get('/api/instructions?date=2016-12-13T00:00:00Z', headers={'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        actual = resp_body['data']
        self.assertEquals(1, len(actual))
        self.assertEquals(10003, actual[0]['meal_id'])
