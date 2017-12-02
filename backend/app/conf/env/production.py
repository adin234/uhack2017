# Declare development config here
class Production(object):
    # Mongo db config
    MONGO_URI = '127.0.0.1'
    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_CONNECT_TIMEOUT_MS = 10000


    # MySQL Config
    # For multiple mysql connections, use object for each config,
    # the db driver will read and parse it as needed

    APP_DB = {
        'host': 'localhost',
        'db': 'sample_auth',
        'user': 'root',
        'password': 'useruser',
        'port': 3306
    }

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        APP_DB['user'], APP_DB['password'], APP_DB['host'], APP_DB['db'])

    # AWS Configuration
    AWS = {
        'COGNITO': {
            'USER_POOL_ID': '',
            'APP_CLIENT_ID': '',
            'AWS_REGION': '',
            'SERVICE_NAME': ''
        },
        'S3': {},
        'EC2': {}
    }

    LOGGING = {
        'LEVEL': 'INFO',
        'FORMAT': '[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s'
    }
