# Import global context
from flask import request, g

# Import Users model
from .database import db
from .error_handler import FailedRequest

## NOTE This will get the member id from the service id
## and attatch them both in the request context
def get_user_id(app):
    @app.before_request
    def before():
        user_id = request.headers.get('X-User-ID')

        if not user_id:
            g.current_user = None
            return

        con = db.session.connection()

        q = '''
            SELECT * FROM user
            WHERE user_id = {} LIMIT 1;
        '''.format(user_id)
        try:
            user = con.execute(q).fetchone()

            if len(user) == 0:
                raise FailedRequest('No existing user record for given id!', status_code=404,
                                    payload='Cannot find user record for given id!')
        finally:
            db.session.close()

        g.current_user = {
            'user_id': user[0],
            'email': user[1],
            'name': user[3]
        }
