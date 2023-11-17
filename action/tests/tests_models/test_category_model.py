from django.test import TestCase
from action.tests import utils


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category1_name = "Category1"
        self.category1 = utils.create_category(self.category1_name)

        self.category2_name = "Category2"
        self.category2 = utils.create_category(self.category2_name)

    def test_category_attribute(self):
        self.assertEqual(self.category1.name, self.category1_name)
        self.assertEqual(str(self.category1), self.category1_name)
        self.assertEqual(self.category2.name, self.category2_name)
        self.assertEqual(str(self.category2), self.category2_name)