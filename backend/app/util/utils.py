"""
    Utility functions for most commonly used
    stuff.
"""
import re
import hashlib

import requests

# Import core libraries
from ..lib.error_handler import FailedRequest
from ..conf.config import DefaultConfig


def custom_hash(string):
    return hashlib.sha1(str(string).encode('utf-8')).hexdigest()


def clean_string(string, delimiter=' '):
    return delimiter.join(string.split())


def get_data(reqd, optional, body):
    ret = {}

    i = len(reqd) - 1
    while i >= 0:
        temp = reqd[i]

        if temp not in body or type(body[temp]) == object:
            raise FailedRequest('Missing required parameter: {}'.format(temp), status_code=400,
                                payload='Required parameters must be in the request body or payload.')

        ret[temp] = body[temp]

        if isinstance(ret[temp], str):
            ret[temp] = clean_string(ret[temp])

            if ret[temp] == '':
                raise FailedRequest('Missing required parameter: {}'.format(temp), status_code=400,
                                    payload='Required parameters must be in the request body or payload.')

        i -= 1

    i = len(optional) - 1
    while i >= 0:
        temp = optional[i]

        if temp not in body or type(body[temp]) == object:
            ret[temp] = None

        else:
            ret[temp] = body[temp]

        if isinstance(ret[temp], str):
            ret[temp] = clean_string(ret[temp])

            if ret[temp] == '':
                ret[temp] = None

        i -= 1

    return ret


def validate_anonymous_id(anonymous_id):
    if not anonymous_id:
        return False

    pattern = re.compile(DefaultConfig.ANONYMOUS_ID_PATTERN)
    match = pattern.match(anonymous_id)
    return match is not None


def encode_params(params):
    params_encoded = []

    for key in params.keys():
        params_encoded.append(quote(key, safe='~()*!.\'')
                              + '=' + quote(params.get(key), safe='~()*!.\''))

    return '&'.join(params_encoded)
