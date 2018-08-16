from uuid import uuid4

from datastorm.objects import FilterField
from tests.test_base import TestBase


class TestQuery(TestBase):

    def test_query_get_no_filter_no_result(self):
        result = self.TestEntity1.query.get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_no_filter_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid).save()
        result = self.TestEntity1.query.get(uuid)
        self.assertIsNotNone(result)

    def test_query_get_int_filter_eq_no_result(self):
        result = self.TestEntity1.query.filter(FilterField("int_field") == 1).get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_float_filter_eq_no_result(self):
        result = self.TestEntity1.query.filter(FilterField("float_field") == 1.0).get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_str_filter_eq_no_result(self):
        result = self.TestEntity1.query.filter(FilterField("str_field") == "foo").get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_dict_filter_eq_no_result(self):
        result = self.TestEntity1.query.filter(self.TestEntity1.dict_field == {}).get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_list_filter_eq_no_result(self):
        result = self.TestEntity1.query.filter(self.TestEntity1.list_field == []).get(str(uuid4()))
        self.assertIsNone(result)

    def test_query_get_int_filter_eq_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") == 1).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_eq_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=1.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") == 1.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_eq_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") == "foo").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") < 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") < 1.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") < "foe").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_int_filter_lt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") < 2).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_lt_result(self):
        uuid = str(uuid4())
        a = self.TestEntity1(uuid, float_field=1.0, uuid=uuid)
        a.save()
        result = self.TestEntity1.query.filter(FilterField("float_field") < 2.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_lt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") < "fop").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") > 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=1.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") > 1.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") > "foo").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_int_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") > 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") > 1.0).filter(
            FilterField("uuid") == uuid).first()
        results = list(self.TestEntity1.query.all())
        self.assertIsNotNone(result)

    def test_query_get_str_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foe", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") > "foa").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_le_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") <= 0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_le_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=1.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") <= 0.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_le_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") <= "foa").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_int_filter_le_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") <= 2).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_le_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") <= 2.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_le_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foe", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") <= "foe").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_ge_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") >= 1).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_ge_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=0.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") >= 1.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_ge_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foa", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") >= "foo").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_int_filter_ge_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") >= 2).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_ge_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") >= 2.0).filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_ge_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foe", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") >= "foe").filter(
            FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_ordered_ascendent_results(self):
        uuid1, uuid2 = str(uuid4()), str(uuid4())
        self.TestEntity1(uuid1, int_field=1, uuid=uuid1).save()
        self.TestEntity1(uuid2, int_field=2, uuid=uuid2).save()
        results = list(self.TestEntity1.query.order(self.TestEntity1.int_field).all())
        self.assertEqual(len(results), 2)
        self.assertEqual(uuid1, results[0].uuid)
        self.assertEqual(uuid2, results[1].uuid)

    def test_query_ordered_descendent_results(self):
        uuid1, uuid2 = str(uuid4()), str(uuid4())
        self.TestEntity1(uuid1, int_field=1, uuid=uuid1).save()
        self.TestEntity1(uuid2, int_field=2, uuid=uuid2).save()
        results = list(self.TestEntity1.query.order(self.TestEntity1.int_field, inverted=True).all())
        self.assertEqual(len(results), 2)
        self.assertEqual(uuid2, results[0].uuid)
        self.assertEqual(uuid1, results[1].uuid)

    def test_query_parent_key(self):
        parent_uuid, descendant_uuid = str(uuid4()), str(uuid4())

        class TestEntity2(self.datastorm.DSEntity):
            __kind__ = "TestEntity2"

        parent = TestEntity2(parent_uuid, int_field=1, uuid=parent_uuid)
        parent.save()
        b = self.TestEntity1(
            self.datastorm.generate_key(self.TestEntity1.__kind__, descendant_uuid, parent_key=parent.key),
            int_field=2, uuid=descendant_uuid).save()

        result = list(self.TestEntity1.query.all(parent_key=parent.key))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].uuid, descendant_uuid)

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