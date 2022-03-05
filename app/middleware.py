import logging
from flask import redirect, request


class Redirects(object):
    """
    Holds logic for redirecting requests when needed
    """
    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):
        app.before_request(self._domain_redirect)

    def _domain_redirect(self):
        """Logic for redirect"""
        # hydrate new_url here
        new_url=''
        return redirect(new_url, code=301)


class Logger(object):
    """Logs all needed information about a request/response call
    """
    def __init__(self, app, log_response=False):
        self.init_app(app)
        self._log_response = log_response

    def init_app(self, app):
        app.before_request(self._request_logger)
        app.after_request(self._response_logger)

    def _request_logger(self):
        req_data = {}
        req_data['cookies'] = request.cookies
        req_data['headers'] = dict(request.headers)
        req_data['headers'].pop('Cookie', None)
        logging.info(req_data)

    def _response_logger(self, response):
        resp_data = {}
        resp_data['headers'] = dict(response.headers)
        logging.info(resp_data)
        return response
