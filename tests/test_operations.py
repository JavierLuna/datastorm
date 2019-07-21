from uuid import uuid4

from tests.test_base import TestBase


class TestOperations(TestBase):

    def test_create_ok(self):
        uuid = str(uuid4())
        self.assertIsNone(self.TestEntity1.query.get(uuid))
        self.TestEntity1(uuid, uuid=uuid).save()
        result = self.TestEntity1.query.get(uuid)
        self.assertIsNotNone(result)
        self.assertEqual(result.uuid, uuid)

    def test_update_ok(self):
        uuid = str(uuid4())
        self.assertIsNone(self.TestEntity1.query.get(uuid))
        a = self.TestEntity1(uuid, uuid=uuid, int_field=1)
        a.save()
        result = self.TestEntity1.query.get(uuid)
        self.assertIsNotNone(result)
        self.assertEqual(result.uuid, uuid)
        self.assertEqual(result.int_field, 1)

        a.int_field = 2
        a.save()

        result = self.TestEntity1.query.get(uuid)
        self.assertIsNotNone(result)
        self.assertEqual(result.uuid, uuid)
        self.assertEqual(result.int_field, 2)

    def test_delete_ok(self):
        uuid = str(uuid4())
        self.assertIsNone(self.TestEntity1.query.get(uuid))
        a = self.TestEntity1(uuid, uuid=uuid)
        a.save()
        result = self.TestEntity1.query.get(uuid)
        self.assertIsNotNone(result)
        self.assertEqual(result.uuid, uuid)

        a.delete()

        result = self.TestEntity1.query.get(uuid)
        self.assertIsNone(result)
