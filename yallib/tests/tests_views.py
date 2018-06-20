import unittest
import datetime
from django.utils import timezone
from yallib.models.library import Author, Book, Genre, Publication
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class AuthorsView(unittest.TestCase):
    @classmethod
    def setUpTestClass(cls):
        number_of_authors = 3
        for i in range(number_of_authors):
            Author.objects.create(first_name="Guido van", last_name="Rossum")

    def test_url_exists_location(self):
        resp = self.client.get('/login/authors/')  # проверяет заданный url
        self.assertEqual(resp.status_code, 200)  # status code successful

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))  # генерит адресс
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'login/authors.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)  # to check template reseive all info
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['author_list']) == 3)


class AuthorLoginUserLIstView(LoginRequiredMixin):

    model = Author
    template_name = 'login/authors.html'
    paginate_by = 3

    def get_queryset(self):
        return Author.objects.filter(a=self.request.user).\
            filter(ORDER_STATUS="1")


class BookByUserListViewTest(unittest.TestCase):

    def setUp(self):
        User = get_user_model()
        # create two Users
        self.test_user1 = User.objects.create_superuser(
            email="GenBor@ukr.net",
            password="4569",
            )
        test_user1.save()

        self.test_user2 = User.objects.create_superuser(
            email="Gen@ukr.net",
            password="4311",
            )
        test_user2.save()
        # create book

        test_author = Author.objects.create(first_name='Gen', last_name='Bor')
        test_genre = Genre.objects.create(name='Scienty')
        test_publication = Publication.objects.create(name='Ukraine')
        test_book = Book.objects.create(
            publication=test_publication,
            author=test_author)
        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre = genre_objects_for_book
        test_book.save()

        number_of_book_copies = 5
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = '0'
            Book.objects.create(
                book = test_book, imprint='gfd',
                due_back=return_date,
                borrower=the_borrower,
                status=status
                )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        # если пользователь незалогирован
        self.assertRedirects(resp, '/login/?next=/login/authors/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='4311')
        resp = self.client.get(reverse('my-borrowed'))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, '/authors.html')

    def test_only_borrowed_books(self):
        login = self.client.login(username='test_user1', password='4569')
        resp = self.client.get(reverse("my-borrowed"))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        # Проверка, что изначально у нас нет книг в списке
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(len(resp.context['book_list']), 0)


if __name__ == "__main__":
    unittest.main()
