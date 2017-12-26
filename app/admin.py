from wtforms.fields import SelectField, PasswordField
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import Entry, Tag, User

class BaseModelView(ModelView):
	pass

class SlugModelView(ModelView):
	# Override
	def on_model_change(self, form, model, is_created):
		model.generate_slug()
		return super(SlugModelView, self).on_model_change(form, model, is_created)

class EntryModelView(SlugModelView):
	# Customizing List View
	_choices = [
		(Entry.STATUS_PUBLIC, "Public"),
		(Entry.STATUS_DRAFT, "Draft"),
		(Entry.STATUS_DELETED, "Deleted"),
	]

	_status_choices = [(choice, label) for choice, label in _choices]

	column_choices = {
		'status': _status_choices
	}

	column_filters = ['status', User.name, User.email, 'created_timestamp']
	column_list = [
		'title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp'
	]

	column_searchable_list = ['title', 'body']
	column_select_related_list = ['author'] # Efficiently SELECT the author

	# Customizing Form View
	form_args = {
		'status': {'choices': _status_choices, 'coerce': int}
	}
	form_columns = ['title', 'body', 'status', 'author', 'tags']
	form_overrides = {'status': SelectField}
	form_ajax_refs = {
		'author': {
			'fields': (User.name, User.email)
		}
	}

class UserModelView(SlugModelView):
	column_filters = ['email', 'name', 'active']
	column_list = ['email', 'name', 'active', 'created_timestamp']
	column_searchable_list = ['email', 'name']

	form_columns = ['email', 'password', 'name', 'active']
	form_extra_fields = {
		'password': PasswordField("New Password")
	}

	# Override
	def on_model_change(self, form, model, is_created):
		if form.password.data:
			model.password_hash = User.make_password(form.password.data)
			return super(UserModelView, self).on_model_change(form, model, is_created)

admin = Admin(app, 'Blog Admin')
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))