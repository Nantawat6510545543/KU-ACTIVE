from django.test import TestCase
from action.models import Tag


class TagTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_name(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")
