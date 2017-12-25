import datetime, re
from app import db, login_manager, bcrypt

def slugify(s):
	return re.sub('[^\w]+', '-', s).lower()

entry_tags = db.Table('entry_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class Entry(db.Model):
	STATUS_PUBLIC = 0
	STATUS_DRAFT = 1
	STATUS_DELETED = 2

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	slug = db.Column(db.String(100), unique=True)
	body = db.Column(db.Text)
	status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
	created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
	modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	tags = db.relationship('Tag', secondary=entry_tags, backref=db.backref('entries', lazy='dynamic'))

	def __init__(self, *args, **kwargs):
		# call parent constructor
		super(Entry, self).__init__(*args, **kwargs)
		self.generate_slug()

	def generate_slug(self):
		self.slug = ''
		if self.title:
			self.slug = slugify(self.title)

	def __repr__(self):
		return '<Entry: {0}>'.format(self.title)

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

	def __repr__(self):
		return '<Tag: {0}>'.format(self.name)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(255))
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)
	active = db.Column(db.Boolean, default=True)
	created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.generate_slug()

	def __repr__(self):
		return '<User: {0}>'.format(self.name)

	def generate_slug(self):
		if self.name:
			self.slug = slugify(self.name)

	# Flask-Login interface..
	def get_id(self):
		return str(self.id)

	def is_authenticated(self):
		return True

	def is_active(self):
		return self.active

	def is_anonymous(self):
		return False

	@staticmethod
	def make_password(plaintext):
		return bcrypt.generate_password_hash(plaintext)

	def check_password(self, raw_password):
		return bcrypt.check_password_hash(self.password_hash, raw_password)

	@classmethod
	def create(cls, email, password, **kwargs):
		return User(email=email, password_hash=User.make_password(password), **kwargs)

	@staticmethod
	def authenticate(email, password):
		user = User.query.filter(User.email == email).first()
		if user and user.check_password(password):
			return user
		return False

@login_manager.user_loader
def _user_loader(user_id):
	return User.query.get(int(user_id))