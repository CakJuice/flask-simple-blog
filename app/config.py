class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	DEBUG = True
	
	"""
	The SQLALCHEMY_DATABASE_URI comprises the following parts:
	dialect+driver://username:password@host:port/database
	example -> postgresql://postgres:secretpassword@localhost:5432/blog_db
	"""
	SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/blog.db'.format(APPLICATION_DIR)