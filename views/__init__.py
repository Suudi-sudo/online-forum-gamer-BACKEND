from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
post_bp = Blueprint('post', __name__)
team_bp = Blueprint('team', __name__)
message_bp = Blueprint('message', __name__)

from . import auth, post, team, message
