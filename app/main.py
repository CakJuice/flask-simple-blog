from app import app
import views

if __name__ == '__main__':
	app.run()

"""
We do not call app.run(debug=True) because we have already instructed Flask
to run our app in the debug mode in the Configuration object.
"""