import os


class BaseConfig(object):
    # App name
    APP_NAME = "UHACK BACKEND"

    # Get app root path, also can use flask.root_path.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/../'

    DEBUG = False
    TESTING = False
    THREADS_PER_PAGE = 2

    AUTHOR = ['dev@hacarus.com']

    APP_ENV = 'development'


class DefaultConfig(BaseConfig):
    # Statement for enabling the development environment
    DEBUG = True

    LOG_PATH = '/tmp/flask_server.log'

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'jUZts0meR@nd0mK3yz'
    SECRET_KEY = 'jUZts0meR@nd0mK3yz'

    PAGE_LIMIT = 20

    # CORS
    ALLOWED_HEADERS = ['Access-Token', 'Content-Type', 'referrer']
    ALLOWED_ORIGINS = '*'
    ALLOWED_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']

    ERROR = {
        'no_results': 'No results found',
        'permission': 'You do not have permission to do this action'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    UB_BASE_URL = 'https://api-uat.unionbankph.com/partners/sb'
    UB_CLIENT_ID = '0bd3e5bb-6acd-4212-889b-e0d98529ed6f'
    UB_CLIENT_SECRET = 'H4fF2cI5jF8rM5oH0qQ5cX6vB8xE2jK7lU1yA5pL1iX4uR7uJ1'
