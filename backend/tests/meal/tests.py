# -*- coding: utf-8 -*-
#
from flask_testing import TestCase
import json

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def test_meal_history(self):
        _params = {
            'date': '2016-12-12T00:00:00Z'
        }
        resp = self.client.get('/api/meals/history', query_string=_params,
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('menu' in resp_body['data']['breakfast']['menus'])
        self.assertTrue('own_menu' in resp_body['data']['breakfast']['menus'])

        self.assertTrue('menu' in resp_body['data']['lunch']['menus'])
        self.assertTrue('own_menu' in resp_body['data']['lunch']['menus'])

        self.assertTrue('breakfast' in resp_body['data'])
        self.assertTrue('morning_snack' in resp_body['data'])
        self.assertTrue('lunch' in resp_body['data'])
        self.assertTrue('afternoon_snack' in resp_body['data'])
        self.assertTrue('dinner' in resp_body['data'])
        self.assertTrue('night_snack' in resp_body['data'])







