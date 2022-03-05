from os import path
from flask import Flask
from app import util, routes
from app.user_api import router as user
from app.admin_api import router as admin
from app.public_api import router as public


templates = path.join(path.abspath(path.dirname(__file__)), 'templates')


app = Flask(__name__, template_folder=templates)
app.register_blueprint(routes.blueprint)
app.register_blueprint(public.app, url_prefix="/api/public")
app.register_blueprint(admin.app, url_prefix="/api/admin")
app.register_blueprint(user.app, url_prefix="/api/user")

if __name__ == '__main__':
    app.run(debug=util.is_dev())
