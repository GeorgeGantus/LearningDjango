from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


class AuthorsLoginTest(AuthorsBaseFunctionalTest):

    def get_login_fields(self):
        user_field = self.input_by_placeholder(
            self.browser, 'Type your username here!')
        password_field = self.input_by_placeholder(
            self.browser, 'Type your password')
        return user_field, password_field

    def test_user_valid_data_can_login_successfully(self):
        password_needed = 'pass'
        user = User.objects.create_user(
            username='my_user', password=password_needed)
        self.browser.get(self.live_server_url + reverse('authors:login'))

        user_field, password_field = self.get_login_fields()
        user_field.send_keys(user.username)
        password_field.send_keys(password_needed)
        password_field.send_keys(Keys.ENTER)

        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_action'))
        self.assertIn('Not Found', self.browser.find_element(
            By.TAG_NAME, 'body').text)

    def test_form_login_invalid_message(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        user_field, password_field = self.get_login_fields()
        user_field.send_keys(' ')
        password_field.send_keys(' ')
        password_field.send_keys(Keys.ENTER)
        self.assertIn('Invalid username or password',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_invalid_credentials_message(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        user_field, password_field = self.get_login_fields()
        user_field.send_keys('invalid_user')
        password_field.send_keys('invalid_credentials')
        password_field.send_keys(Keys.ENTER)
        self.assertIn('Invalid credentials.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
