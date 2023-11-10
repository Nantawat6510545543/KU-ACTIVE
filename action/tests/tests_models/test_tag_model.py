from django.test import TestCase
from action.tests import utils


class TagTestCase(TestCase):
    def setUp(self):
        self.tag1_name = "Tag1"
        self.tag1 = utils.create_tag(self.tag1_name)

        self.tag2_name = "Tag2"
        self.tag2 = utils.create_tag(self.tag2_name)

    def test_tag_attribute(self):
        self.assertEqual(self.tag1.name, self.tag1_name)
        self.assertEqual(str(self.tag1), self.tag1_name)
        self.assertEqual(self.tag2.name, self.tag2_name)
        self.assertEqual(str(self.tag2), self.tag2_name)
