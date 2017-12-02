# -*- coding: utf-8 -*-

import json
from unittest.mock import patch

from flask_testing import TestCase
from app import db

# from ..start_test import app
from app import init_app

app = init_app()
app.config['TESTING'] = True

class APITest(TestCase):
    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()

    @patch('app.api.auth.dispatch.AWSUserPoolManager.get_user')
    def test_check_serviceid(self, get_user):
        resp = self.client.post('/api/auth/check_serviceid', data=json.dumps({
            'service_id': 'notexists'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(404, resp.status_code)

        get_user.return_value = {
            'Enabled': False,
            'UserStatus': 'Confirmed'
        }

        resp = self.client.post('/api/auth/check_serviceid', data=json.dumps({
            'service_id': '100001'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        self.assertFalse(resp_body['data']['enabled'])

        get_user.assert_called_with('100001')

    def test_pre_signup(self):
        resp = self.client.post('/api/auth/pre_signup', data=json.dumps({
            'service_id': 'notexists'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(404, resp.status_code)

        resp = self.client.post('/api/auth/pre_signup', data=json.dumps({
            'service_id': '100001'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(400, resp.status_code)

        resp = self.client.post('/api/auth/pre_signup', data=json.dumps({
            'service_id': '100007'
        }), headers={'Content-Type': 'application/json'})
        # self.assertEqual(200, resp.status_code)

    def test_post_confirm(self):
        resp = self.client.post('/api/auth/post_confirm', data=json.dumps({
            'service_id': 'notexists'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(404, resp.status_code)

        # do nothing for existing member
        resp = self.client.post('/api/auth/post_confirm', data=json.dumps({
            'service_id': '100001'
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, resp.status_code)

        resp = self.client.post('/api/auth/post_confirm', data=json.dumps({
            'service_id': '100008'
        }), headers={'Content-Type': 'application/json'})
        # self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
