import wtforms
from wtforms import validators
from flask_wtf import FlaskForm
from app import app
from models import User

class LoginForm(FlaskForm):
	email = wtforms.StringField("Email", validators=[validators.DataRequired()])
	password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])
	remember_me = wtforms.BooleanField("Remember me?", default=True)

	# Override
	def validate(self):
		if not super(LoginForm, self).validate():
			return False

		self.user = User.authenticate(self.email.data, self.password.data)
		if not self.user:
			self.email.errors.append("Invalid email or password")
			return False

		return True