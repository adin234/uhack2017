# -*- coding: utf-8 -*-
#
from flask_testing import TestCase
import json

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app


    def test_add_member(self):
        resp = self.client.post('/api/member', data=json.dumps({
            'anonymous_id': 'ap-northeast-1:5e29caa8-3fee-44fb-a66d-9ef632d0738e',
        }), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        self.assertEqual('ap-northeast-1:5e29caa8-3fee-44fb-a66d-9ef632d0738e', resp_body['data']['anonymous_id'])


    def test_add_member_device(self):
        resp = self.client.post('/api/member/devices', data=json.dumps({
            'token': '2acc5939d77473e3ac8ba18824ace087b42a72d60406818afb4126788ffe893f',
            'platform': 'apple'
        }), headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        self.assertTrue(resp_body['data']['enabled'])
        self.assertEqual('2acc5939d77473e3ac8ba18824ace087b42a72d60406818afb4126788ffe893f', resp_body['data']['token'])

    def test_get_member_profile(self):
        resp = self.client.get('/api/member/profile',
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEquals(200, resp.status_code)
        res_body = json.loads(str(resp.get_data(), 'utf-8'))
        # Check for all crucial data
        self.assertTrue('language' in res_body['data'])
        self.assertTrue('time_zone' in res_body['data'])
        self.assertTrue('birthday' in res_body['data'])
        self.assertTrue('gender' in res_body['data'])
        self.assertTrue('height' in res_body['data'])
        self.assertTrue('weight' in res_body['data'])
        self.assertTrue('eer' in res_body['data'])
        self.assertTrue('physical_activity_level' in res_body['data'])
        self.assertTrue('service_id' in res_body['data'])

    def test_get_member_notification(self):
        resp = self.client.get('/api/member/notification',
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEquals(200, resp.status_code)
        res_body = json.loads(str(resp.get_data(), 'utf-8'))
        # Check for all crucial data
        actual = res_body['data']['settings']
        self.assertEquals(2, len(actual))
        self.assertEquals('instruction', actual[0]['notification_type'])
        self.assertEquals('recommendation', actual[1]['notification_type'])

        resp = self.client.get('/api/member/notification',
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100022'})
        self.assertEquals(404, resp.status_code)

    def test_add_member_notification(self):
        resp = self.client.post('/api/member/notification', data=json.dumps({
            'settings': [
                {'notification_type': 'instruction', 'enabled': False},
                {'notification_type': 'recommendation', 'enabled': True},
            ]
        }), headers={'Content-Type': 'application/json', 'X-Service-ID': '100002'})
        self.assertEqual(200, resp.status_code)

    def test_migrate_member(self):
        # error as the user already has service ID
        resp = self.client.post('/api/member/migrate', data=json.dumps({
            'service_id': '100009'
        }), headers={'Content-Type': 'application/json', 'X-Service-ID': '100002'})
        self.assertEqual(400, resp.status_code)

        # error as the given service ID isn't associated with member ( just issued Service ID )
        resp = self.client.post('/api/member/migrate', data=json.dumps({
            'service_id': '10000'
        }), headers={'Content-Type': 'application/json',
                     'X-Anonymous-ID': 'ap-northeast-1:faf0578f-14fb-4c74-a474-32825215db90'})
        self.assertEqual(400, resp.status_code)

        resp = self.client.post('/api/member/migrate', data=json.dumps({
            'service_id': '100009'
        }), headers={'Content-Type': 'application/json',
                     'X-Anonymous-ID': 'ap-northeast-1:faf0578f-14fb-4c74-a474-32825215db90'})
        self.assertEqual(200, resp.status_code)


    def test_member_subscription(self):

        resp = self.client.get('/api/member/subscription',
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEquals(200, resp.status_code)
        res_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('subscriptions' in res_body['data'])
        self.assertEquals(len(res_body['data']['subscriptions']), 1)
