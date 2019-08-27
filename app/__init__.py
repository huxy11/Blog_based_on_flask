from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection ='strong'
#the view is a 'auth' blueprint so the login_view should be auth.login
login_manager.login_view = 'auth.login'


#cfg = dev, tst, prd, dft
def create_app(cfg):
    app = Flask(__name__)
    app.config.from_object(config[cfg])
    config[cfg].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app
