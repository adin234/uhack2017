# System import
import os

# Import flask
from flask import Flask
from flask_cors import CORS

from .conf import config as Config
from .conf import constants as CONST
from .conf.env import get_env

from .lib import get_user_id, db, mod_err, create_logger

# import *
__all__ = ['init_app']


def init_app(config=None):
    """ App initialization """

    # Declare app
    app = Flask(Config.BaseConfig.APP_NAME,
                instance_path=CONST.INSTANCE_FOLDER_PATH,
                instance_relative_config=True,
                template_folder=Config.BaseConfig.BASE_DIR + CONST.TEMPLATE_FOLDER)

    load_config(app, config)
    load_lib(app)
    load_middlewares(app)
    load_blueprints(app)

    if app.debug:
        check_routes(app)

    return app


def load_config(app, config=None):
    """ Load the base config and env config """

    app.config.from_object(Config.DefaultConfig)
    print(' * Loading base default config')

    # Loads config file if there are any config included
    if config:
        app.config.from_object(config)
        print(' * Loading custom config')
        return

    env = Config.BaseConfig.APP_ENV

    # checks available environment
    if os.environ.get('NMI_ENV') is not None:
        env = os.environ.get('NMI_ENV').lower()

    app.config.from_object(get_env(env))


def load_lib(app):
    """ lib for application """

    # Database SQLAlchemy
    # If you want to use raw engine creation
    # Use create_engine from .lib.database
    db.init_app(app)

    # Initializes the logger class
    create_logger(app)


def load_middlewares(app):
    """ Loads necessary middle wares for the app """

    # Error handlers
    app.register_blueprint(mod_err)

    # Handles the service id checking
    get_user_id(app)

    # CORS
    CORS(app, allow_headers=app.config['ALLOWED_HEADERS'],
         origins=app.config['ALLOWED_ORIGINS'],
         methods=app.config['ALLOWED_METHODS'])


def load_blueprints(app):

    # Add a ping route
    @app.route('/api')
    def index():
        return 'ok'

    """ Loads blueprints for the app """
    from .www.frontend_dispatch import mod_frontend
    from .api.auth.dispatch import mod_auth
    from .api.transactions.dispatch import mod_transaction

    app.register_blueprint(mod_frontend)
    app.register_blueprint(mod_auth, url_prefix='/api/auth')
    app.register_blueprint(mod_transaction, url_prefix='/api/transaction')


def check_routes(app):
    """
    I've added this function
    for the sake of checking
    and debugging the available routes
    upon registration to the blueprint

    :param app:
    :return None:
    """

    print(' * Checking all available routes. . . ')
    _public_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for rule in app.url_map.iter_rules():
        for _method in rule.methods:
            if _method in _public_methods:
                print('\t[x] {:>8}\t {}'.format(_method, rule))
    print('\n\n')
