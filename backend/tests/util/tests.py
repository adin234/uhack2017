# -*- coding: utf-8 -*-
#
from unittest import TestCase

from app.util.utils import get_eer, get_basal_metabolism, validate_anonymous_id


class UnitTest(TestCase):
    def test_get_eer(self):
        # low = basel_metabolism * 1.5
        actual = get_eer(1432, 1)
        self.assertEqual(2148, actual)

        # middle = basel_metabolism * 1.75
        actual = get_eer(1432, 2)
        self.assertEqual(2506, actual)

        # high = basel_metabolism * 2.0
        actual = get_eer(1432, 3)
        self.assertEqual(2864, actual)

    def test_get_eer_invalid_level(self):
        with self.assertRaises(IndexError):
            get_eer(1432, 4)

        # should be error
        get_eer(1432, 0)

    def test_get_basal_metabolism(self):
        actual = get_basal_metabolism(84.5, 179, 24, 'male')
        self.assertEqual(1791.2924032489252, actual)

    def test_validate_anonymous_id(self):
        # True
        self.assertTrue(validate_anonymous_id('ap-northeast-1:f4e7a523-857b-4414-834c-50cee455f969'))

        # False
        # short
        self.assertFalse(validate_anonymous_id('ap-northeast-1:f4e7a523-857b-4414-834c-50'))
        # long
        self.assertFalse(validate_anonymous_id('ap-northeast-1:f4e7a523-857b-4414-834c-50cee455f96933'))
        # wrong alphabet
        self.assertFalse(validate_anonymous_id('ap-northeast-1:f4e7a523-857b-4414-834c-50zzzz455f969'))
        self.assertFalse(validate_anonymous_id(''))
        self.assertFalse(validate_anonymous_id(None))
