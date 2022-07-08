import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionaltest(AuthorsBaseFunctionalTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form')

    def test_empty_field_message(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        name_field = self.input_by_placeholder(form, 'Ex.: John')
        name_field.send_keys(Keys.ENTER)

        form = self.get_form()
        self.assertIn('This field is required', form.text)

    def test_register_correct_data(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.input_by_placeholder(form, 'Ex.: John').send_keys('Felipe')
        self.input_by_placeholder(form, 'Ex.: Doe').send_keys('Alberto')
        self.input_by_placeholder(
            form, 'Type your username here').send_keys('felipealberto')
        self.input_by_placeholder(
            form, 'Your e-mail').send_keys('valid@mail.com')
        self.input_by_placeholder(
            form, 'Type your password here').send_keys('Pa55word')
        self.input_by_placeholder(
            form, 'Repeat your password').send_keys('Pa55word')
        form.submit()
        self.assertIn('Author created',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

        ...
