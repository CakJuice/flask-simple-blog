from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# import our configuration data.
from config import Configuration

app = Flask(__name__)

# use values from our Configuration object.
app.config.from_object(Configuration)
db = SQLAlchemy(app)