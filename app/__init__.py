from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from .auth.routes import auth
# from flask_moment import Moment
from .api import api #coming from the init file , so just api

# for CORS
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

cors = CORS()
cors.init_app(app)
db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
# moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = 'login_page'

#register blueprint
app.register_blueprint(auth)
app.register_blueprint(api)


from . import routes
from . import models