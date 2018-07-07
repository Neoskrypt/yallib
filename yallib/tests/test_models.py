import unittest
from yallib.models import Author


class AuthorModelTest(unittest.TestCase):

        @classmethod
        def setUpTestClass(cls):
            # Set up non-modified objects used by all test methods
            Author.objects.create(first_name="Bor", last_name="Gen")

        def setUp(self):
            # Run once for every test method to setup clean data
            pass

        def test_first_name_label(self):
            author = Author.objects.filter(id=1)
            field_label = author.order_by("first_name").first()
            self.assertTrue(field_label == "Bor")

        def test_last_name_label(self):
            author = Author.objects.filter(id=1)
            field_label = author.order_by("last_name").first()
            self.assertEquals(field_label, "Gen")

        def test_first_name_max_lenght(self):
            author = Author.objects.filter(id=1)
            max_length = author.order_by("first_name").first()
            self.assertEqual(max_length, 100)

        def test_last_name_max_lenght(self):
            author = Author.objects.filter(id=1)
            max_length = author.order_by("last_name").first()
            self.assertEqual(max_length, 100)


if __name__ == "__main__":
    unittest.main()
