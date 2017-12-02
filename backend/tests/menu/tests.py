# -*- coding: utf-8 -*-
#
from flask_testing import TestCase
import json

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def test_menu_history(self):
        resp = self.client.get('/api/menus/history', headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        actual = resp_body['data']
        self.assertEqual(7, len(actual))








