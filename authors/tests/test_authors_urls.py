from django.test import TestCase
from django.urls import reverse


class AuthorsUrlsTest(TestCase):
    def test_register_url_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register')
