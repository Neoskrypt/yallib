from django.test import SimpleTestCase
import unittest
from yallib.models.library import Author
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.test import Client
from django.template.loader import render_to_string
import pytest


class AuthorsView(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        # number_of_authors = 3
        cls.client = Client()

        Author.objects.create(
            created='2018-06-06 06:42:07+03:00',
            changed='2018-06-06 06:42:30.296614+03:00',
            first_name="Gen",
            last_name="Bor",
            date_birth="1995-02-14",
                )

    def test_url_exists_location(self):
        resp = self.client.get('/login/authors/')  # проверяет заданный url
        self.assertEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))  # генерит адресс
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 302)  # перенапр на друг стр
        with self.assertTemplateUsed(resp, template_name='/authors.html'):
                render_to_string('authors.html')

    def test_pagination_is_ten(self):

        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 302)
        # self.assertTrue(resp.context[pag])
        self.assertTrue(len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        pag = 'is_paginated'
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(pag in resp.context)
        self.assertTrue(resp.Context[pag])
        self.assertTrue(len(resp.context['author_list']) == 10)


class AuthorLoginUserLIstView(LoginRequiredMixin):

    model = Author
    template_name = 'login/authors.html'
    paginate_by = 3

    def get_queryset(self):
        return Author.objects.filter(a=self.request.user).\
            filter(ORDER_STATUS="1")


"""
class BookByUserListViewTest(unittest.TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        email, password = "GenBor@ukr.net", '4569'

        test_user1 = (email, password)
        # self.test_user1.save()
        email1, password1 = "Gen@ukr.net", '4311'
        test_user2 = (
            email1,
            password1,
            )

        test_genre = Genre.objects.create(
            name='Scienty',
            created='2018-06-06 06:42:07+03:00',
            changed='2018-06-06 06:42:30.296614+03:00',
            )

        genre_objects_for_book = Genre.objects.all()

        number_of_book_copies = 5
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = '0'
            Book.objects.create(
                created='2018-06-06 06:42:07+03:00',
                changed='2018-06-06 06:42:30.296614+03:00',
                caption="gf"
                )


class Booktest(SimpleTestCase):
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('login'))
        # если пользователь незалогирован
        self.assertRedirects(resp, '/login/?next=/login/authors/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='4311')
        resp = self.client.get(reverse('login'))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, '/authors.html')

    def test_only_borrowed_books(self):
        login = self.client.login(username='test_user1', password='4569')
        resp = self.client.get(reverse("login"))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        # Проверка, что изначально у нас нет книг в списке
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(len(resp.context['book_list']), 0)
"""

if __name__ == "__main__":
    unittest.main()
