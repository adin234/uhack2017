import datetime

# Import global context
from flask import request, current_app

# Import flask dependencies
from flask import Blueprint

from ...util import utils
from ...lib import FailedRequest
from ...lib import db, make_response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from .models import User

# Define the blueprint: 'auth', set its url prefix: app.url/user
mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/user', methods=['GET'])
@make_response
def get_user(res):
    params = utils.get_data(['email'], [], request.get_json(silent=True))

    res.send({})


@mod_auth.route('/user', methods=['POST'])
@make_response
def create_user(res):
    params = utils.get_data(['email', 'name'], [], request.get_json(silent=True))

    params['user_id'] = None
    params['password'] = None
    params['enabled'] = 1
    params['timezone'] = None
    params['language'] = None
    params['image_url'] = None

    user = User(params)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as error:
        if isinstance(error, IntegrityError):
            db.session.rollback()
            look_up = db.session.query(User).filter(User.email == params['email']).first()
            return res.send(look_up.serialize())

        else:
            raise FailedRequest('An error occured: {}'.format(error), status_code=500)

    return res.send(user.serialize())


@mod_auth.route('/redirect_uri', methods=['GET'])
@make_response
def redirect_uri(res):
    params = utils.get_data(['code'], [], request.args)

    res.send({})
