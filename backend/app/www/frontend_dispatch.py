import os

# Import flask dependencies
from flask import Blueprint, render_template, current_app, send_from_directory

# Define the blueprint: 'auth', set its url prefix: app.url/user
mod_frontend = Blueprint('frontend', __name__)


# You can declare all the frontend routes here
@mod_frontend.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'app/www/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')