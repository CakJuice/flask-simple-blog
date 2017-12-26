from flask import render_template, request, flash, redirect, url_for, g
from flask_login import login_user, logout_user
from app import app, login_manager
from forms import LoginForm

@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if g.user.is_authenticated:
		flash("You still logged in!", 'info')
		return redirect(url_for('homepage'))
	else:
		if request.method == 'POST':
			form = LoginForm(request.form)
			if form.validate():
				login_user(form.user, remember=form.remember_me.data)
				flash("Successfully logged in as {0}.".format(form.user.email, 'success'))
				return redirect(request.args.get('next') or url_for('homepage'))
		else:
			form = LoginForm()
		return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
	if g.user.is_authenticated:
		logout_user()
		flash("You have been logged out.", 'success')
		return redirect(request.args.get('next') or url_for('homepage'))
	else:
		flash("You're not logged in!", 'info')
		return redirect(url_for('homepage'))