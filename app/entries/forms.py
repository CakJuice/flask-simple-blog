import wtforms
from wtforms.validators import DataRequired
from models import Entry

class EntryForm(wtforms.Form):
	title = wtforms.StringField('Title', validators=[DataRequired()])
	body = wtforms.TextAreaField('Body', validators=[DataRequired()])
	status = wtforms.SelectField(
		'Entry Status',
		choices = (
			(Entry.STATUS_PUBLIC, "Public"),
			(Entry.STATUS_DRAFT, "Draft")),
		coerce=int)
	"""
	coerce, will convert the value from the form to an integer (by default, it
	would be treated as a string, which we do not want).
	"""

	def save_entry(self, entry):
		self.populate_obj(entry)
		entry.generate_slug()
		return entry