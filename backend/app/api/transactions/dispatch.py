import datetime

# Import global context
from flask import request, current_app, g

# Import flask dependencies
from flask import Blueprint

from ...util import utils
from ...lib import FailedRequest
from ...lib import db, make_response, auth_required
from sqlalchemy import and_, or_, between

from .models import UserTransaction
from ..auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/user
mod_transaction = Blueprint('transaction', __name__)


@mod_transaction.route('', methods=['POST'])
@auth_required
@make_response
def create_transaction(res):

    params = utils.get_data(
        ['amount', 'currency', 'exchange_currency',
         'depart_date', 'arrive_date', 'depart_from', 'arrive_to'],
        [],
        request.get_json(silent=True))

    params['user_id'] = g.current_user['user_id']
    params['user_transaction_id'] = None
    params['closed'] = False

    try:
        params['depart_date'] = datetime.datetime.strptime(params['depart_date'], '%Y-%m-%d %H:%M:%S')
        params['arrive_date'] = datetime.datetime.strptime(params['arrive_date'], '%Y-%m-%d %H:%M:%S')

    except Exception as error:
        raise FailedRequest('Error: {}'.format(error), status_code=500)

    user_transaction = UserTransaction(params)
    db.session.add(user_transaction)
    db.session.commit()

    return res.send(user_transaction.serialize())


@mod_transaction.route('/user_transaction', methods=['GET'])
@auth_required
@make_response
def get_user_transactions(res):

    transactions = db.session.query(UserTransaction)\
        .filter(UserTransaction.user_id == g.current_user['user_id'])\
        .order_by(UserTransaction.closed)\
        .all()

    transactions = list(map(lambda x: x.serialize(), transactions))
    return res.send(transactions)


@mod_transaction.route('/search_match', methods=['GET'])
@auth_required
@make_response
def search_matching_transaction(res):

    def format_result(data):
        for row in data:
            item = row.UserTransaction
            yield {
                'user_transaction_id': item.user_transaction_id,
                'amount': float(str(item.amount)),
                'currency': item.currency,
                'exchange_currency': item.exchange_currency,
                'depart_date': item.depart_date,
                'arrive_date': item.arrive_date,
                'depart_from': item.depart_from,
                'arrive_to': item.arrive_to,
                'name': row.name,
                'email': row.email
            }

    params = utils.get_data(['transaction_id'], [], request.args)

    base = db.session.query(UserTransaction)\
        .filter(UserTransaction.user_transaction_id == params['transaction_id']).first()

    base_arrive = base.arrive_to
    base_depart = base.depart_from
    # Set 12 hours as grace period/waiting time
    base_arrive_date_start = base.arrive_date + datetime.timedelta(hours=3)
    base_arrive_date_end = base.arrive_date + datetime.timedelta(hours=15)

    base_depart_date_start = base.depart_date - datetime.timedelta(hours=15)
    base_depart_date_end = base.depart_date - datetime.timedelta(hours=3)

    if not base:
        raise FailedRequest('Cannot find transaction!', status_code=404)

    transactions = db.session.query(UserTransaction, User.name, User.email)\
        .join(User, User.user_id == UserTransaction.user_id)\
        .filter(UserTransaction.closed == False)\
        .filter(UserTransaction.user_id != g.current_user['user_id'])\
        .filter(UserTransaction.exchange_currency == base.currency)\
        .filter(
            or_(
                and_(UserTransaction.depart_from == base_arrive,
                     between(UserTransaction.depart_date, base_arrive_date_start, base_arrive_date_end)),
                and_(UserTransaction.arrive_to == base_depart,
                     between(UserTransaction.arrive_date, base_depart_date_start, base_depart_date_end))
            )
        ).all()

    return res.send(list(format_result(transactions)))
