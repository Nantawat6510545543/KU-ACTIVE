from action.tests.utils import Tester


class TagTestCase(Tester):
    def setUp(self):
        super().setUp()
        self.tag1_name = "Tag1"
        self.tag1 = self.create_tag(self.tag1_name)

        self.tag2_name = "Tag2"
        self.tag2 = self.create_tag(self.tag2_name)

    def test_tag_attribute(self):
        self.assertEqual(self.tag1.name, self.tag1_name)
        self.assertEqual(self.tag2.name, self.tag2_name)

