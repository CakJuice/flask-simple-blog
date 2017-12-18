from flask import Flask

# import our configuration data.
from config import Configuration

app = Flask(__name__)

# use values from our Configuration object.
app.config.from_object(Configuration)