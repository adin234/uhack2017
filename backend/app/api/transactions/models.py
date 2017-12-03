from ...lib import db, Serializer


class UserTransaction(db.Model, Serializer):
    __tablename__ = 'user_transactions'

    user_transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    closed = db.Column(db.Boolean(), nullable=False)
    amount = db.Column(db.DECIMAL(18, 6), nullable=False)
    currency = db.Column(db.String(32), nullable=False)
    exchange_currency = db.Column(db.String(32), nullable=False)
    depart_date = db.Column(db.DateTime, nullable=False)
    arrive_date = db.Column(db.DateTime, nullable=False)
    depart_from = db.Column(db.String(128), nullable=False)
    arrive_to = db.Column(db.String(128), nullable=False)

    def __init__(self, trans_obj):
        self.user_transaction_id = trans_obj['user_transaction_id']
        self.user_id = trans_obj['user_id']
        self.closed = trans_obj['closed']
        self.amount = trans_obj['amount']
        self.currency = trans_obj['currency']
        self.exchange_currency = trans_obj['exchange_currency']
        self.depart_date = trans_obj['depart_date']
        self.arrive_date = trans_obj['arrive_date']
        self.depart_from = trans_obj['depart_from']
        self.arrive_to = trans_obj['arrive_to']


class Airport(db.Model, Serializer):
    __tablename__ = 'airports'

    code = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.Text, nullable=False)


class TransactionConfirmation(db.Model, Serializer):
    __tablename__ = 'transaction_confirmation'

    transaction_confirmation_id = db.Column(db.Integer, primary_key=True)
    base_transaction_id = db.Column(db.Integer, nullable=False)
    secondary_transaction_id = db.Column(db.Integer, nullable=False)
    base_confirmation = db.Column(db.Boolean(), nullable=False)
    secondary_confirmation = db.Column(db.Boolean(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False)

    def __init__(self, trans_obj):
        self.transaction_confirmation_id = trans_obj['transaction_confirmation_id']
        self.base_transaction_id = trans_obj['base_transaction_id']
        self.secondary_transaction_id = trans_obj['secondary_transaction_id']
        self.base_confirmation = trans_obj['base_confirmation']
        self.secondary_confirmation = trans_obj['secondary_confirmation']
        self.completed = trans_obj['completed']
