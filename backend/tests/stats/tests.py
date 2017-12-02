# -*- coding: utf-8 -*-
#
import json

from flask_testing import TestCase
from app import db

from ..start_test import app


class APITest(TestCase):
    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()

    def test_get_weight_history(self):
        params = {
            'page': 1,
            'limit': 4
        }
        resp = self.client.get('/api/stats/weight/history', query_string=params,
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertEquals(len(resp_body['data']), 4)
        self.assertEquals(resp_body['data'][0]['recorded_at'], '2016-12-16')
        self.assertEquals(resp_body['data'][1]['recorded_at'], '2016-12-14')
        self.assertEquals(resp_body['data'][2]['recorded_at'], '2016-12-13')
        self.assertEquals(resp_body['data'][3]['recorded_at'], '2016-12-12')

    def test_get_bp_history(self):
        params = {
            'page': 1,
            'limit': 4
        }
        resp = self.client.get('/api/stats/blood_pressure/history', query_string=params,
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('data' in resp_body)
        self.assertTrue('systolic' in resp_body['data'][0])
        self.assertTrue('diastolic' in resp_body['data'][0])
        self.assertTrue('pulse' in resp_body['data'][0])

    def test_post_weight_history(self):
        weight_data = {
            'weight': 30,
            'recorded_at': '2015-01-01T01:23:00Z'
        }

        resp = self.client.post('/api/stats/weight', data=json.dumps(weight_data),
                                headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('weight_history_id' in resp_body['data'])

    def test_post_step_history(self):
        step_data = {
            'step': 4000,
            'recorded_at': '2015-01-01T01:23:00Z'
        }

        resp = self.client.post('/api/stats/step', data=json.dumps(step_data),
                                headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('step_history_id' in resp_body['data'])

    def test_post_blood_pressure_history(self):
        bp_data = {
            'pulse': 30,
            'systolic': 80,
            'diastolic': 40,
            'recorded_at': '2015-02-22T00:22:00Z',
            'taken_at': 'others',
            'notes': 'This is a note',
            'healthkit_uuid': 'AAAAAAA',
            'healthkit_source': 'BBBB'
        }

        resp = self.client.post('/api/stats/blood_pressure', data=json.dumps(bp_data),
                                headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('blood_pressure_history_id' in resp_body['data'])
        self.assertEquals(resp_body['data']['notes'], 'This is a note')

    def test_post_blood_sugar_history(self):
        bs_data = {
            'amount': 300,
            'recorded_at': '2015-02-22T00:22:00Z',
            'taken_at': 'before_meal',
            'meal_type': 'breakfast',
            'healthkit_uuid': 'ABCDE',  # This will just update instead of post
            'healthkit_source': 'New Source'
        }

        resp = self.client.post('/api/stats/blood_sugar', data=json.dumps(bs_data),
                                headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))

        self.assertTrue('blood_sugar_history_id' in resp_body['data'])
        self.assertEquals(resp_body['data']['meal_type'], 'breakfast')
        self.assertEquals(resp_body['data']['healthkit_source'], 'New Source')
        self.assertEquals(resp_body['data']['blood_sugar_history_id'], 10004)

    def test_delete_blood_sugar_history(self):
        bs_data = {
            'healthkit_uuids': ['ABCDE']
        }

        resp = self.client.delete('/api/stats/blood_sugar/healthkit', data=json.dumps(bs_data),
                                  headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)

        # the following assert will change once test runs
        # resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        # self.assertEqual(resp_body['data']['count'], 1)
