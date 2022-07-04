from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username here'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password here'),
        ('password_confirm', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', ('Required. 150 characters or fewer. '
                      'Letters, digits and @/./+/-/_ only.')),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'The password must have at least one uppercase letter,'
            'one lowercase letter and one number. The length should be at'
            'least 8 characters'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'Email address'),
        ('password', 'Password'),
        ('password_confirm', 'Password verification'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirm': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        field_errors = response.context['form'].errors.get(field)
        self.assertIn(msg, field_errors)

    def test_if_last_name_forbiden_name_validation_is_correct(self):
        self.form_data['last_name'] = 'Gantus'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        last_name_error = response.context['form'].errors.get('last_name')
        msg = 'Last name could not be Gantus'
        self.assertIn(msg, last_name_error)

        self.form_data['last_name'] = 'Pines'
        response = self.client.post(url, data=self.form_data, follow=True)
        last_name_error = response.context['form'].errors.get('last_name', [])
        self.assertNotIn(msg, last_name_error)

    def test_if_password_validation_is_correct(self):
        self.form_data['password'] = 'notavalidpassword'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        password_error = response.context['form'].errors.get('password', [])
        msg = ('Password must have at least one uppercase letter,'
               ' one lowercase letter and one number. The length should'
               ' be at least 8 characters.')
        self.assertIn(msg, password_error)

        self.form_data['password'] = 'Avalidpassword1'
        response = self.client.post(url, data=self.form_data, follow=True)
        password_error = response.context['form'].errors.get('password', [])
        self.assertNotIn(msg, password_error)

    def test_if_password_and_password_confirm_validation_is_correct(self):
        self.form_data['password'] = 'Pa55word'
        self.form_data['password_confirm'] = 'Pa55word'
        msg = 'Password and Password verification must be equal'
        url = reverse('authors:create')

        response = self.client.post(url, data=self.form_data, follow=True)
        password_error = response.context['form'].errors.get('password', [])
        self.assertNotIn(msg, password_error)

        self.form_data['password'] = 'Pa55wordDiff'
        response = self.client.post(url, data=self.form_data, follow=True)
        password_error = response.context['form'].errors.get('password', [])
        self.assertIn(msg, password_error)
