from app import handlers
from flask import Blueprint

blueprint = Blueprint(
    'handlers',
    __name__,
)

add = blueprint.add_url_rule

add('/', view_func=handlers.IndexHandler.as_view('index'))
add('/admin', view_func=handlers.AdminHandler.as_view('admin'))
add('/user', view_func=handlers.UserHandler.as_view('user'))
