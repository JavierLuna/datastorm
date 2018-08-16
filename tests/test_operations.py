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
        result = self.TestEntity1.query.filter(FilterField("int_field") == 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_eq_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=1.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") == 1.0).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_eq_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") == "foo").filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") < 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") < 1.0).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_lt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") < "foe").filter(FilterField("uuid") == uuid).first()
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
        result = self.TestEntity1.query.filter(FilterField("float_field") < 2.0).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_str_filter_lt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") < "fop").filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_int_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=1, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") > 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_float_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=1.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") > 1.0).filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)

    def test_query_get_str_filter_gt_no_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foo", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") > "foo").filter(FilterField("uuid") == uuid).first()
        self.assertIsNone(result)


    def test_query_get_int_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, int_field=2, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("int_field") > 1).filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)

    def test_query_get_float_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, float_field=2.0, uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("float_field") > 1.0).filter(FilterField("uuid") == uuid).first()
        results = list(self.TestEntity1.query.all())
        self.assertIsNotNone(result)

    def test_query_get_str_filter_gt_result(self):
        uuid = str(uuid4())
        self.TestEntity1(uuid, str_field="foe", uuid=uuid).save()
        result = self.TestEntity1.query.filter(FilterField("str_field") > "foa").filter(FilterField("uuid") == uuid).first()
        self.assertIsNotNone(result)