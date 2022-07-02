from authors import views
from django.test import TestCase
from django.urls import resolve, reverse


class RegisterViewTest(TestCase):
    def test_authors_register_view_func_is_correct(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register_view)

    def test_authors_register_view_return_status_code_200(self):
        response = self.client.get(reverse('authors:register'))
        self.assertEqual(response.status_code, 200)

    def test_authors_register_loads_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/register.html')
