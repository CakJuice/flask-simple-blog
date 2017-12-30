import os, sys
sys.path.append(os.path.realpath(os.pardir))
import unittest
from main import app

class FlaskLoginMixin():
	LOGIN_URL = '/login/'
	LOGOUT_URL = '/logout/'

	def login(self, email, password):
		return self.app.post(self.LOGIN_URL, data={
			'email': email,
			'password': password
		}, follow_redirects=True)

	def logout(self):
		return self.app.get(self.LOGOUT_URL, follow_redirects=True)

class AppTest(unittest.TestCase, FlaskLoginMixin):
	def setUp(self):
		self.app = app.test_client()

	def test_homepage_works(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

	def test_login_logout(self):
		response_login = self.login("cakjuice@test.com", "cakjuice")
		self.assertEqual(response_login.status_code, 200)
		self.assertTrue("Success" in str(response_login.data))
		response_logout = self.logout()
		self.assertEqual(response_logout.status_code, 200)
		self.assertTrue("logged out" in str(response_logout.data))

	def test_failed_login_logout(self):
		response_login = self.login("admin", "password")
		self.assertEqual(response_login.status_code, 200)
		self.assertTrue("Invalid" in str(response_login.data))
		response_logout = self.logout()
		self.assertEqual(response_logout.status_code, 200)
		self.assertTrue("not logged in" in str(response_logout.data))

if __name__ == '__main__':
	unittest.main()