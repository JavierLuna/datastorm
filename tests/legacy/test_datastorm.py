from uuid import uuid4
from tests.legacy.test_base import TestBase

class TestDatastorm(TestBase):

    def test_create_entity_str_key_ok(self):
        key = str(uuid4())
        test_entity = self.TestEntity1(key)
        test_entity.save()

    def test_create_entity_Key_key_ok(self):
        key = self.datastorm.generate_key(self.TestEntity1.__kind__, str(uuid4()))
        test_entity = self.TestEntity1(key)
        test_entity.save()

    def test_create_entity_parent_key_ok(self):
        parent_key = self.datastorm.generate_key(self.TestEntity1.__kind__, str(uuid4()))
        key = self.datastorm.generate_key(self.TestEntity1.__kind__, str(uuid4()), parent_key=parent_key)
        test_entity = self.TestEntity1(key)
        test_entity.save()

    def test_create_entity_no_kind_ko(self):
        class TestEntity2(self.datastorm.DSEntity):
            pass

        with self.assertRaises(ValueError):
            test_entity = TestEntity2(str(uuid4()))
            test_entity.save()

    def test_save_multi_ok(self):
        entity_batch = [self.TestEntity1(str(uuid4())) for _ in range(100)]
        self.datastorm.save_multi(entity_batch)

