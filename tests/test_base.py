import unittest

from datastorm import DataStorm


class TestBase(unittest.TestCase):
    TEST_PROJECT_ID = "datastorm-test"

    def setUp(self):
        from datastorm import fields
        self.datastorm = DataStorm(TestBase.TEST_PROJECT_ID)

        class TestEntity1(self.datastorm.DSEntity):
            __kind__ = "TestEntity1"

            dict_field = fields.DictField()
            list_field = fields.ListField()
            int_field = fields.IntField()

        self.TestEntity1 = TestEntity1

    def tearDown(self):
        [entity.delete() for entity in self.TestEntity1.query.all()]
