from django.test import TestCase
from action.tests import utils


class CategoryTestCase(TestCase):
    """Test case for the Category model."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Set the name for Category1 and create a category instance.
        2. Set the name for Category2 and create another category instance.
        """
        self.category1_name = "Category1"
        self.category1 = utils.create_category(self.category1_name)

        self.category2_name = "Category2"
        self.category2 = utils.create_category(self.category2_name)

    def test_category_attribute(self):
        """Test the attributes of the Category model."""
        self.assertEqual(self.category1.name, self.category1_name)
        self.assertEqual(str(self.category1), self.category1_name)
        self.assertEqual(self.category2.name, self.category2_name)
        self.assertEqual(str(self.category2), self.category2_name)
