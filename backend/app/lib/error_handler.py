"""
    Error handling module designed to
    catch general errors and specif errors during request
"""
import logging
import coloredlogs

from logging.handlers import RotatingFileHandler

# Import global context
from flask import jsonify, make_response, request, current_app, g

# Import flask dependencies
from flask import Blueprint


class FailedRequest(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(code=self.status_code,
                  message=self.message,
                  data=self.payload)
        return rv


# Blueprint declaration
mod_err = Blueprint('mod_err', __name__)


# Builds the error object based on the error code
# and message
def build_error_object(error, title, code):
    e_obj = {
        'errors': {
            'status': code,
            'source': {'pointer': request.url},
            'title': title,
            'detail': error
        }
    }

    return make_response(jsonify(e_obj), code)


def create_logger(app):
    """ Creates a logger and attaches it to app
        Access it by current_app.logger
    """
    logging_config = app.config['LOGGING']

    coloredlogs.install()

    logging.addLevelName(logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    _level = logging.DEBUG

    if 'LEVEL' in logging_config:
        _level = getattr(logging, logging_config['LEVEL'])

    app.logger.setLevel(_level)

    _format = '[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s'
    if 'FORMAT' in logging_config:
        _format = logging_config['FORMAT']

    _formatter = logging.Formatter(_format)
    _file_logger = RotatingFileHandler(app.config['LOG_PATH'],
                                       maxBytes=10000,
                                       backupCount=1)

    _file_logger.setLevel(_level)
    _file_logger.setFormatter(_formatter)

    app.logger.addHandler(_file_logger)
    return


# Declare necessary error handlers
@mod_err.app_errorhandler(404)
def not_found(error):
    current_app.logger.warning(error)
    return build_error_object(error.description, 'The Monkey Ninja cannot find your request', 404)


@mod_err.app_errorhandler(405)
def not_found(error):
    current_app.logger.warning(error)
    return build_error_object(error.description, 'Our pet Dragon cannot resolve your command. Try another method', 405)


@mod_err.app_errorhandler(500)
def not_found(error):
    current_app.logger.error(error)
    return build_error_object(error.description, 'The Monkey Ninja is starving and have failed internally', 500)


@mod_err.app_errorhandler(FailedRequest)
def exception_encountered(error):
    error = error.to_dict()
    current_app.logger.error(error)
    return build_error_object(error['data'], error['message'], error['code'])


# @mod_err.app_errorhandler(Exception)
# def exception_encountered(error):
#     return build_error_object(str(error), 'Something exploded insde of me. Let the fireman deal with this', 500)
