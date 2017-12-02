import json
import argparse

from app import init_app


def load_custom_config(file_path):
    """
    Accepts a json file
    and builds a custom config object from it.

    :param file_path:
    :return:
    """
    _json_data = None

    # CustomConfig Class handler
    class CustomConfigTemplate(object):
        def __init__(self, j_obj):
            self.__dict__ = json.loads(j_obj)

            self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'\
                .format(self.APP_DB['user'], self.APP_DB['password'],
                        self.APP_DB['host'], self.APP_DB['db'])


    with open(file_path) as json_file:
        _json_data = json_file.read()

    return CustomConfigTemplate(_json_data)

def get_arguments():
    """
    Gets the commandline arguments passes
    :return:
    """
    parser = argparse.ArgumentParser(description='Gets argument to set for app in development/staging environment.')

    parser.add_argument('-p', '--port', dest='port', type=int, default=3000,
                        help='Port to run the application')
    parser.add_argument('-r', '--use-reloader', dest='reloader',
                        type=int, default=1, help='Boolean, will use reloader if true')
    parser.add_argument('-d', '--use-debugger', dest='debugger',
                        type=int, default=1, help='Boolean, will enable debugger if true')
    parser.add_argument('-ht', '--host', dest='host',type=str,
                        default='0.0.0.0', help='Host you want to use for deployment')
    parser.add_argument('-c', '--config', dest='config_path',
                        type=str, default=None, help='Custom config you want to load')

    return parser.parse_args()


if __name__ == '__main__':

    args = get_arguments()

    custom_config = None
    # Loads custom config based on file path of the config.json file
    if args.config_path:
        custom_config = load_custom_config(args.config_path)

    app = init_app(custom_config)

    app.run(host=args.host, port=args.port,
            use_reloader=bool(args.reloader),
            threaded=True, debug=bool(args.debugger))
