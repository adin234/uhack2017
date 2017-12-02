# -*- coding: utf-8 -*-
#
from flask_testing import TestCase
import json

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def test_activity(self):

        # create activity
        resp = self.client.post('/api/activities', data=json.dumps({
            'exercise_id': 1,
            'worked_at': '2017-01-27T09:00:00Z',
            'energy': 210,
            'work_time': 60,
        }), headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        self.assertEqual(1, resp_body['data']['exercise_id'])
        self.assertEqual(210, resp_body['data']['energy'])
        self.assertEqual(60, resp_body['data']['work_time'])
        self.assertIsNone(resp_body['data']['amount'])

        # update activity
        activity_id = resp_body['data']['activity_id']
        resp = self.client.patch('/api/activities/{0}'.format(activity_id), data=json.dumps({
            'energy': 10,
            'work_time': 30,
            'amount': 40,
        }), headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        self.assertEqual(1, resp_body['data']['exercise_id'])
        self.assertEqual(10, resp_body['data']['energy'])
        self.assertEqual(30, resp_body['data']['work_time'])
        self.assertEqual(40, resp_body['data']['amount'])

        # delete activity
        resp = self.client.delete('/api/activities/{0}'.format(activity_id),
                                  headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})
        self.assertEqual(200, resp.status_code)
