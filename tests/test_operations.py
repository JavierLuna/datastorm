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

    def test_update_projection(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, float_field=1.2).save()
        result = self.TestEntity1.query.only('int_field').first()
        self.assertFalse(hasattr(result, 'float_field'))
        result.int_field = 2
        result.save()
        result = self.TestEntity1.query.first()
        self.assertFalse(hasattr(result, 'float_field'))
        self.assertEqual(result.int_field, 2)