# -*- coding: utf-8 -*-
#
import json
import datetime

from flask_testing import TestCase
from app import db
from app.api.dashboard.dispatch import get_meals
from app.api.member.model import MemberProfile
from app.api.recommendation.model import Recommendation

from ..start_test import app


class UnitTest(TestCase):
    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()

    def assert_meal(self, energy, actual):
        self.assertEqual(energy, actual['energy'])

    def test_get_meals(self):
        target_date = datetime.datetime.strptime('2016-12-12', '%Y-%m-%d')
        actual = get_meals(target_date, 10001, 'Asia/Tokyo')
        total = actual['total']

        # check total values
        self.assertEqual(1516.3181, total['energy'])
        self.assertEqual(45.8397, total['yellow'])
        self.assertEqual(35.7471, total['red'])
        self.assertEqual(65.2794, total['green'])

        # check meal values
        self.assert_meal(277.23, actual['breakfast'])
        self.assert_meal(0, actual['morning_snack'])
        self.assert_meal(1239.0881, actual['lunch'])
        self.assert_meal(0, actual['afternoon_snack'])
        self.assert_meal(0, actual['dinner'])
        self.assert_meal(0, actual['night_snack'])

    def test_get_recommendation(self):
        target_date = datetime.datetime.strptime('2016-12-12', '%Y-%m-%d')
        member = MemberProfile({
            'member_id': 10001,
            'birthday': None,
            'time_zone': 'Asia/Tokyo',
            'language': 'ja',
            'gender': None,
            'height': None,
            'weight': None,
            'eer': None,
            'basal_metabolism': None,
            'physical_activity_level': None,
            'purpose_of_use': None,
            'purpose_text': None,
            'target_weight': None,
            'last_meal_eaten_date': None,
        })
        actual = Recommendation.get_member_recommendations(member, target_date).first()
        self.assertEqual(10001, actual.recommendation_id)
        self.assertEqual('Recommended Recipe', actual.section_title)


class APITest(TestCase):
    def create_app(self):
        return app

    def tearDown(self):
        db.session.remove()

    def test_dashboard_stat_data(self):
        params = {
            'date': '2016-12-12T00:00:00Z'
        }
        resp = self.client.get('/api/dashboard', query_string=params,
                               headers={'Content-Type': 'application/json', 'X-Service-ID': '100001'})

        self.assertEqual(200, resp.status_code)
        resp_body = json.loads(str(resp.get_data(), 'utf-8'))
        print(resp_body)
        return
        self.assertTrue('blood_pressure' in resp_body['data']['stats'])
        self.assertTrue('blood_sugar' in resp_body['data']['stats'])
        self.assertTrue('weight' in resp_body['data']['stats'])
        self.assertTrue('step' in resp_body['data']['stats'])

        self.assertTrue(resp_body['data']['stats']['blood_sugar'] is None)
        self.assertTrue('hacarus' in resp_body['data']['stats']['weight'])
        self.assertTrue('healthkit' in resp_body['data']['stats']['weight'])
        self.assertEquals(len(resp_body['data']['stats']['blood_pressure']['healthkit']), 3)
