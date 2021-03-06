import wtforms
from wtforms import validators
from models import Entry, Tag

class TagField(wtforms.StringField):
	# Override
	def _value(self):
		if self.data:
			# Display tags as a comma-separated list.
			return ", ".join([tag.name for tag in self.data])
		return ""

	def get_tags_from_string(self, tag_string):
		raw_tags = tag_string.split(',')

		# Filter out any empty tag names.
		tag_names = [name.strip() for name in raw_tags if name.strip()]

		# Query the database and retrieve any tags we have already saved.
		existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

		# Determine which tag names are new.
		new_names = set(tag_names) - set([tag.name for tag in existing_tags])

		# Create a list of unsaved Tag instances for the new tags.
		new_tags = [Tag(name=name) for name in new_names]

		# Return all the existing tags + all the new, unsaved tags.
		return list(existing_tags) + new_tags

	def process_formdata(self, valuelist):
		if valuelist:
			self.data = self.get_tags_from_string(valuelist[0])
		else:
			self.data = []

class ImageForm(wtforms.Form):
	file = wtforms.FileField('Image File')

class EntryForm(wtforms.Form):
	title = wtforms.StringField('Title', validators=[validators.DataRequired()])
	body = wtforms.TextAreaField('Body', validators=[validators.DataRequired()])
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
	tags = TagField('Tags', description="Separate multiple tags with commas.")

	def save_entry(self, entry):
		self.populate_obj(entry)
		entry.generate_slug()
		return entry

class CommentForm(wtforms.Form):
	name = wtforms.StringField('Name',
		validators=[validators.DataRequired()])
	email = wtforms.StringField('Email',
		validators=[validators.DataRequired(), validators.Email()])
	url = wtforms.StringField('URL',
		validators=[validators.Optional(), validators.URL()])
	body = wtforms.TextAreaField('Comment',
		validators=[validators.DataRequired(), validators.Length(min=10, max=3000)])
	entry_id = wtforms.HiddenField(validators=[validators.DataRequired()])

	def validate(self):
		if not super(CommentForm, self).validate():
			return False

		# Ensure that entry_id maps to a public Entry.
		entry = Entry.query.filter(
			(Entry.status == Entry.STATUS_PUBLIC) &
			(Entry.id == self.entry_id.data)).first()

		if not entry:
			return False

		return True