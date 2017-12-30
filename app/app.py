from flask import Flask, g
from flask_restless import APIManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# import our configuration data.
from config import Configuration

app = Flask(__name__)

# use values from our Configuration object.
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = APIManager(app, flask_sqlalchemy_db=db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.before_request
def _before_request():
	g.user = current_user

bcrypt = Bcrypt(app)

csrf = CSRFProtect(app)

"""set logging"""
# from logging.handlers import RotatingFileHandler
# file_handler = RotatingFileHandler('blog.log')
# app.logger.addHandler(file_handler)

# to add log file just add script -> app.logger.info("Homepage has been accessed.")