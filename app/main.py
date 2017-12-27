from app import app, db
import models
import views
import admin

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
	app.run()

"""
We do not call app.run(debug=True) because we have already instructed Flask
to run our app in the debug mode in the Configuration object.
"""