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
	ADMIN_URL = '/admin/'
	
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

	def test_admin_can_get_admin_page(self):
		self.login("cakjuice@test.com", "cakjuice")
		response = self.app.get(self.ADMIN_URL)
		self.assertEqual(response.status_code, 200)
		self.assertTrue("Hello" in str(response.data))

	def test_non_logged_in_user_can_get_to_admin_page(self):
		response = self.app.get(self.ADMIN_URL)
		self.assertEqual(response.status_code, 302)
		self.assertTrue("redirected" in str(response.data))

	def test_non_admin_user_cannot_get_to_admin_page(self):
		self.login("test@test.com", "test")
		response = self.app.get(self.ADMIN_URL)
		self.assertEqual(response.status_code, 302)
		self.assertTrue("redirected" in str(response.data))

	def test_logging_out_prevents_access_to_admin_page(self):
		self.login("cakjuice@test.com", "cakjuice")
		self.logout()
		response = self.app.get(self.ADMIN_URL)
		self.assertEqual(response.status_code, 302)
		self.assertTrue("redirected" in str(response.data))

if __name__ == '__main__':
	unittest.main()