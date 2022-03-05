
import json
from flask.views import MethodView
from .util import generate_auth_token
from flask import render_template, make_response


class BaseHandler(MethodView):
    """ Base view for Flask. """
    def render(self, _template, context=None, status_code=200):
        """
        Renders a template and writes the result to the response.
        """
        generic_context = {}

        if context:
            generic_context.update(context)
        rv = render_template(_template, **generic_context)
        response = make_response(rv, status_code)
        return response


class IndexHandler(BaseHandler):
    def get(self):
        ctx = {
            'is_admin': json.dumps(False),
            'is_user': json.dumps(False),
        }
        return self.render('index.html', ctx)

class AdminHandler(BaseHandler):
    def get(self):
        ctx = {
            'is_admin': json.dumps(True),
            'is_user': json.dumps(False),
        }
        resp = self.render('admin.html', ctx)
        admin_access_token = generate_auth_token("test_admin", expires=False)
        resp.set_cookie('admin_auth_token', admin_access_token)
        return resp

class UserHandler(BaseHandler):
    def get(self):
        ctx = {
            'is_admin': json.dumps(False),
            'is_user': json.dumps(True),
        }
        resp = self.render('user.html', ctx)
        user_access_token = generate_auth_token("test_user", expires=False)
        resp.set_cookie('user_auth_token', user_access_token)
        return resp
